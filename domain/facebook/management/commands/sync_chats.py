from django.core.management.base import BaseCommand

import logging
logger = logging.getLogger(__name__)

# System Domain
from domain.facebook.models.Page import Page
from domain.facebook.models.Chat import Chat
from domain.lead.models.Lead import Lead
from domain.lead.models.Message import Message

# Utilities
from domain.facebook.utils.facebook import get_all_conversation, get_all_messages_by_conversation_id, get_message_by_message_id

class Command(BaseCommand):
    help = 'Create system sample data'
 
    def handle(self, *args, **options):
        self.sync_chats()

    def sync_chats(self):
        conversations = get_all_conversation()
        if conversations is not None:
            for conversation in conversations.data[:2]:
                self.log_conversation_info(conversation)
                self.process_messages_for_conversation(conversation)
        else:
            logger.error("No conversations found.")

    def log_conversation_info(self, conversation):
        logger.info(f"Conversation ID: {conversation.id}, Link: {conversation.link}, Updated Time: {conversation.updated_time}")

    def process_messages_for_conversation(self, conversation):
        messages = get_all_messages_by_conversation_id(conversation_id=conversation.id)
        logger.info(messages)

        for message in messages.data:
            self.process_message_detail(message)

    def process_message_detail(self, message):
        message_detail = get_message_by_message_id(message_id=message.id)
        if message_detail is not None:
            logger.info(f"Message ID: {message_detail.data.id}, Message: {message_detail.data.message}")
        else:
            logger.error(f"No details found for message id: {message.id}")
