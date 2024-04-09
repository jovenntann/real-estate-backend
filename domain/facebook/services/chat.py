from typing import List

# Models
from domain.facebook.models.Chat import Chat

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


def create_chat(page, message_id: str, sender: str, page_sender, lead_sender, message: str, timestamp, attachments) -> Chat:
    chat = Chat.objects.create(
        page=page,
        message_id=message_id,
        sender=sender,
        page_sender=page_sender,
        lead_sender=lead_sender,
        message=message,
        timestamp=timestamp,
        attachments=attachments
    )
    logger.info(f"\"{chat}\" has been created.")
    return chat

def update_chat(
        chat: Chat,
        new_page,
        new_message_id: str,
        new_sender: str,
        new_page_sender,
        new_lead_sender,
        new_message: str,
        new_timestamp,
        new_attachments
    ) -> Chat:
    chat.page = new_page
    chat.message_id = new_message_id
    chat.sender = new_sender
    chat.page_sender = new_page_sender
    chat.lead_sender = new_lead_sender
    chat.message = new_message
    chat.timestamp = new_timestamp
    chat.attachments = new_attachments
    chat.save()
    logger.info(f"\"{chat}\" has been updated.")
    return chat
