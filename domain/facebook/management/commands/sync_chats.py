from django.core.management.base import BaseCommand
from django.utils import timezone
import logging

# Models
from domain.system.models.Company import Company
from domain.facebook.models.Page import Page
from domain.lead.models.Lead import Lead

# Importing services and utilities
from domain.system.services.company import get_company_by_id
from domain.facebook.services.page import get_page_by_page_id
from domain.lead.services.status import get_status_by_id
from domain.lead.services.lead import create_lead, get_lead_by_facebook_id, update_lead_last_message_at
from domain.lead.services.message import create_message, get_message_by_messenger_id
from domain.facebook.utils.facebook import (
    get_all_conversation, 
    get_all_messages_by_conversation_id, 
    get_message_by_message_id, 
    get_user_profile_by_id
)

# Data Class
from domain.facebook.utils.facebook import ConversationData, MessageDetailData, MessageData


logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Create system sample data'

    def add_arguments(self, parser):
        parser.add_argument('--next_url', type=str, help='Next URL')

    def handle(self, *args, **options):
        next_url = options.get('next_url', None)
        self.sync_chats(next_url)

    def sync_chats(self, next_url: str = None):
        company = get_company_by_id(id=1)
        page = get_page_by_page_id(page_id=113575558420278)
        self.process_conversations(page=page, company=company, next_url=next_url)

    def process_conversations(self, page: Page, company: Company, next_url=None):
        conversations = get_all_conversation(access_token=page.access_token, page_id=page.page_id, next_url=next_url)
        logger.info(conversations)

        if not conversations:
            logger.error("No conversations found.")
            return

        for conversation in conversations.data:
            logger.info(f"Conversation ID: {conversation.id}, Link: {conversation.link}, Updated Time: {conversation.updated_time}")
            self.process_conversation_messages(page=page, company=company, conversation=conversation)

        if conversations.paging.next:
            self.process_conversations(page, company, conversations.paging.next)
            logger.info(f"Next URL: {conversations.paging.next}")

    def process_conversation_messages(self, page: Page, company: Company, conversation: ConversationData, next_url=None):
        messages = get_all_messages_by_conversation_id(access_token=page.access_token, conversation_id=conversation.id, next_url=next_url)
        logger.info(messages)

        for message in messages.data:

            message_details = get_message_by_message_id(page.access_token, message.id)
            if message_details is None:
                logger.error(f"No message details found for message id: {message.id}. Skipping..")
            
            message_record = get_message_by_messenger_id(messenger_id=message_details.data.id)
            if message_record:
                logger.info(f"Message already exists for messenger message id: {message_details.data.id}. Skipping..")
            
            # If Able to Get Message Details and Message Record do not exist yet: Then let's process it.
            if message_details and message_record is None:
                logger.info(f"Processing message id: {message_details.data.id}")
                # Calculated Variables
                sender_type = 'page' if page.page_id == message_details.data.sender.id else 'lead'
                user_id = message_details.data.sender.id if sender_type == 'lead' else message_details.data.recipient.data[0].id

                # TODO: Lead Status and Lead Next Action (Set this value based on Company)
                status_id = 10
                next_action_id = 2
                lead = self.get_or_create_lead(page=page, company=company, user_id=user_id, conversation_id=conversation.id, status_id=status_id, next_action_id=next_action_id)
                if not lead:
                    logger.info(f"No lead found for message id: {message_details.data.id}. Skipping..")
                if lead:
                    self.create_and_log_message(
                        page=page, 
                        lead=lead, 
                        conversation=conversation, 
                        message=message, 
                        message_details=message_details, 
                        sender_type=sender_type
                    )

        if messages.paging.next:
            self.process_conversation_messages(page, company, conversation, messages.paging.next)

    def get_or_create_lead(self, page: Lead, company: Company, user_id: int, conversation_id: str, status_id: int, next_action_id: int):
        lead = get_lead_by_facebook_id(facebook_id=user_id)
        if lead:
            return lead

        user_profile = get_user_profile_by_id(access_token=page.access_token, user_id=user_id)
        if not user_profile:
            logger.info("Unable to get user profile. Skipping lead creation.")
            return None

        return create_lead(
            first_name=user_profile.data.first_name,
            last_name=user_profile.data.last_name,
            email=f"{user_profile.data.id}@facebook.com",
            phone_number='',
            company=company,
            facebook_id=user_profile.data.id,
            facebook_profile_pic=user_profile.data.profile_pic or 'https://cdn.pixabay.com/photo/2013/07/13/10/44/man-157699_640.png',
            facebook_conversation_id=conversation_id,
            status=status_id,
            next_action=next_action_id
        )
    def create_and_log_message(self, page: Page, lead: Lead, conversation: ConversationData, message: MessageData, message_details: MessageDetailData, sender_type: str):
        create_message(
            page=page,
            lead=lead,
            source='messenger',
            sender=sender_type,
            message=message_details.data.message,
            timestamp=message.created_time,
            messenger_id=message_details.data.id,
            messenger_attachments=message_details.data.attachments,
            is_read=False
        )
        update_lead_last_message_at(lead=lead, last_message_at=conversation.updated_time)
        logger.info(f"Message logged: {message_details.data.message}")
