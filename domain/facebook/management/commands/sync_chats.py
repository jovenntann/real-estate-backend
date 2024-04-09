from django.core.management.base import BaseCommand
from django.utils import timezone

import logging
logger = logging.getLogger(__name__)

# Services
from domain.system.services.company import get_company_by_id
from domain.facebook.services.page import get_page_by_page_id
from domain.facebook.services.chat import get_chat_by_message_id, create_chat
from domain.lead.services.status import get_status_by_id
from domain.lead.services.lead import get_or_create_lead, get_lead_by_facebook_id

# Utilities
from domain.facebook.utils.facebook import get_all_conversation, get_all_messages_by_conversation_id, get_message_by_message_id

class Command(BaseCommand):
    help = 'Create system sample data'
 
    def handle(self, *args, **options):
        self.sync_chats()

    def sync_chats(self):
        company = get_company_by_id(id=1)
        page = get_page_by_page_id(page_id=113575558420278)
        
        conversations = get_all_conversation(access_token=page.access_token, page_id=page.page_id)
        if conversations is not None:
            for conversation in conversations.data[:10]:
                logger.info(f"Conversation ID: {conversation.id}, Link: {conversation.link}, Updated Time: {conversation.updated_time}")
                self.process_messages_for_conversation(page, company, conversation)
        else:
            logger.error("No conversations found.")

    def process_messages_for_conversation(self, page, company, conversation):
        messages = get_all_messages_by_conversation_id(access_token=page.access_token, conversation_id=conversation.id)
        logger.info(messages)

        for message in messages.data:
            self.process_message_detail(page, company, message.created_time, message)

    # PROCESS MESSAGE DETAILS

    def get_or_create_lead(self, company, message_detail):
        lead = get_lead_by_facebook_id(facebook_id=message_detail.data.sender.id)
        if lead is None:
            status = get_status_by_id(id=1)
            lead = get_or_create_lead(
                first_name=message_detail.data.sender.name,
                last_name='',
                email=message_detail.data.sender.email,
                phone_number='',
                company=company,
                status=status,
                facebook_id=message_detail.data.sender.id
            )
        return lead

    def get_or_create_chat(self, page, company, created_time, message_detail):
        chat = get_chat_by_message_id(message_id=message_detail.data.id)
        if chat is None:
            if page.page_id == message_detail.data.sender.id:
                sender = 'admin'
                page_sender = page
                lead_sender = None
            else:
                lead_sender = self.get_or_create_lead(company, message_detail)
                sender = 'customer'
                page_sender = None

            chat = create_chat(
                page=page,
                message_id=message_detail.data.id,
                sender=sender,
                page_sender=page_sender,
                lead_sender=lead_sender,
                message=message_detail.data.message,
                timestamp=created_time,
                attachments=None
            )
        return chat
    
    def get_message_detail(self, access_token, message_id):
        return get_message_by_message_id(access_token, message_id)

    def process_message_detail(self, page, company, created_time, message):
        message_detail = self.get_message_detail(page.access_token, message.id)
        if message_detail is not None:
            logger.info(f"Message ID: {message_detail.data.id}, Message: {message_detail.data.message}")
            chat = self.get_or_create_chat(page, company, created_time, message_detail)
        else:
            logger.error(f"No details found for message id: {message.id}")