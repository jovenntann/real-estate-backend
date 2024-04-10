from typing import List

# Models
from domain.lead.models.Message import Message
from domain.lead.models.Lead import Lead

import logging
logger = logging.getLogger(__name__)


def get_messages() -> List[Message]:
    messages = Message.objects.all().order_by('id')
    logger.info(f"{messages} fetched")
    return messages


def get_message_by_id(message_id: int) -> Message:
    message = Message.objects.filter(id=message_id).first()
    logger.info(f"{message} fetched")
    return message


def delete_message(message: Message) -> Message:
    message.delete()
    logger.info(f"{message} has been deleted.")
    return message


def create_message(page, lead, source: str, sender: str, message: str, timestamp, messenger_id: str = None) -> Message:
    message = Message.objects.create(
        page=page,
        lead=lead,
        source=source,
        sender=sender,
        message=message,
        messenger_id=messenger_id,
        timestamp=timestamp
    )
    logger.info(f"\"{message}\" has been created.")
    return message


def update_message(
        message: Message,
        new_page,
        new_lead,
        new_source: str,
        new_sender: str,
        new_message: str,
        new_messenger_id: str = None
    ) -> Message:
    message.page = new_page
    message.lead = new_lead
    message.source = new_source
    message.sender = new_sender
    message.message = new_message
    message.messenger_id = new_messenger_id
    message.save()
    logger.info(f"\"{message}\" has been updated.")
    return message


def get_message_by_messenger_id(messenger_id: str) -> Message:
    message = Message.objects.filter(messenger_id=messenger_id).first()
    logger.info(f"{message} fetched")
    return message



def get_all_unique_messages() -> List[Message]:
    unique_messages = Message.objects.order_by('lead', 'timestamp').distinct('lead')
    return unique_messages


def get_messages_by_lead(lead: Lead) -> List[Message]:
    messages = Message.objects.filter(lead=lead).order_by('timestamp')
    logger.info(f"Messages for lead {lead} fetched")
    return messages
