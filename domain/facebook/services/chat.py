from typing import List

# Models
from domain.facebook.models.Page import Page
from domain.facebook.models.Chat import Chat
from domain.lead.models.Lead import Lead

import logging
logger = logging.getLogger(__name__)


def get_chats() -> List[Chat]:
    chats = Chat.objects.all().order_by('id')
    logger.info(f"{chats} fetched")
    return chats


def get_chat_by_message_id(message_id: str) -> Chat:
    chat = Chat.objects.filter(message_id=message_id).first()
    logger.info(f"{chat} fetched")
    return chat


def delete_chat(chat: Chat) -> Chat:
    chat.delete()
    logger.info(f"{chat} has been deleted.")
    return chat


def create_chat(message_id: str, sender: str, page: Page, lead: Lead, message: str, timestamp, attachments) -> Chat:
    chat = Chat.objects.create(
        message_id=message_id,
        sender=sender,
        page=page,
        lead=lead,
        message=message,
        timestamp=timestamp,
        attachments=attachments
    )
    logger.info(f"\"{chat}\" has been created.")
    return chat
