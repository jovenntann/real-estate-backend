import os
import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

import logging
logger = logging.getLogger(__name__)

@dataclass
class ConversationData:
    id: str
    link: str
    updated_time: str

@dataclass
class PagingCursors:
    before: str
    after: str

@dataclass
class Paging:
    cursors: PagingCursors
    next: str

@dataclass
class ConversationResponse:
    data: List[ConversationData]
    paging: Paging

def get_all_conversation() -> Optional[ConversationResponse]:

    # Sample Response:
    # {
    #     "data": [
    #         {
    #             "id": "t_2133987576966402",
    #             "link": "/113575558420278/inbox/305599682551197/",
    #             "updated_time": "2024-04-07T06:07:04+0000"
    #         },
    #         {
    #             "id": "t_122181828026008887",
    #             "link": "/113575558420278/inbox/306197225824776/",
    #             "updated_time": "2024-04-07T03:41:47+0000"
    #         }
    #    ],
    #     "paging": {
    #         "cursors": {
    #             "before": "QVFIUkc0dFNmMk1laF9NeHRiQXpoMlk4UGtOTjZABVFpmcHFRY0tHc2JRYkY5X0NqaTAySzI0WXNBeDI5OTRmcS1sbXZASS2p2ajd4WmZAHeG91VnZAybVVsZAFhqMVpOLWpYWTVRRXdNa1VPdExsektLQmdDNElWWmxpamd2dFlRb2ZABeHpp",
    #             "after": "QVFIUnJKczlWVFlZATnJNcy1jdVJta3psd2NIX3F2cnpmMEZATOHhLQjRNS21RalNhQ3k4SnN6SmRfNUw4cTFhbTdud2NLRng5YnZAtR3hRTGVPV0V0X0JYVXViU3RUN184TGhBWE9IckpPNEowbUJpOTlYZAEFwcl9zT2EtTE9mY3JGYjRR"
    #         },
    #         "next": "https://graph.facebook.com/v13.0/113575558420278/conversations?access_token="
    #     }
    # }

    logger.info("Starting to get all conversation ids")
    url = f'https://graph.facebook.com/v13.0/113575558420278/conversations?access_token={os.environ['PAGE_TOKEN']}&limit=499'
    headers = {'Cookie': 'ps_l=0; ps_n=0'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        logger.info("Successfully received response")
        response_data = response.json()
        conversation_data = [ConversationData(**data) for data in response_data.get('data', [])]
        paging_cursors = PagingCursors(**response_data.get('paging', {}).get('cursors', {}))
        paging = Paging(cursors=paging_cursors, next=response_data.get('paging', {}).get('next', ''))
        logger.info("Successfully parsed response data")
        return ConversationResponse(data=conversation_data, paging=paging)
    else:
        logger.error(f"Failed to get response, status code: {response.status_code}")
        return None


@dataclass
class MessageData:
    id: str
    created_time: str

@dataclass
class MessageResponse:
    data: List[MessageData]
    paging: Paging

def get_all_messages_by_conversation_id(conversation_id: str) -> Optional[MessageResponse]:
    logger.info(f"Starting to get all messages for conversation id: {conversation_id}")
    url = f'https://graph.facebook.com/v13.0/{conversation_id}/messages?access_token={os.environ['PAGE_TOKEN']}'
    headers = {'Cookie': 'ps_l=0; ps_n=0'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        logger.info("Successfully received response")
        response_data = response.json()
        message_data = [MessageData(**data) for data in response_data.get('data', [])]
        paging_cursors = PagingCursors(**response_data.get('paging', {}).get('cursors', {}))
        paging = Paging(cursors=paging_cursors, next=response_data.get('paging', {}).get('next', ''))
        logger.info("Successfully parsed response data")
        return MessageResponse(data=message_data, paging=paging)
    else:
        logger.error(f"Failed to get response, status code: {response.status_code}")
        return None





@dataclass
class SenderData:
    name: str
    email: str
    id: str

@dataclass
class RecipientData:
    data: List[SenderData]

@dataclass
class MessageDetailData:
    id: str
    message: str
    sender: SenderData
    recipient: RecipientData
    attachments: str

@dataclass
class MessageDetailResponse:
    data: MessageDetailData

def get_message_by_message_id(message_id: str) -> Optional[MessageDetailResponse]:
    logger.info(f"Starting to get message details for message id: {message_id}")
    url = f'https://graph.facebook.com/v13.0/{message_id}?fields=message,from,to,attachments&access_token={os.environ['PAGE_TOKEN']}'
    headers = {'Cookie': 'ps_l=0; ps_n=0'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        logger.info("Successfully received response")
        response_data = response.json()
        sender_data = SenderData(**response_data.get('from', {}))
        recipient_data = RecipientData(data=[SenderData(**data) for data in response_data.get('to', {}).get('data', [])])
        message_detail_data = MessageDetailData(id=response_data.get('id', ''), message=response_data.get('message', ''), sender=sender_data, recipient=recipient_data, attachments=response_data.get('attachments', ''))
        logger.info("Successfully parsed response data")
        return MessageDetailResponse(data=message_detail_data)
    else:
        logger.error(f"Failed to get response, status code: {response.status_code}")
        return None
    