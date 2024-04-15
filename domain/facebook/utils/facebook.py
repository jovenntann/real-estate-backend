import os
import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

import logging
logger = logging.getLogger(__name__)


# Get All Conversations

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

def get_all_conversation(access_token: str, page_id: str) -> Optional[ConversationResponse]:

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
    url = f'https://graph.facebook.com/v13.0/{page_id}/conversations?access_token={access_token}&limit=499'
    response = requests.get(url)
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
    
# Get All Messages by Conversation ID

@dataclass
class MessageData:
    id: str
    created_time: str

@dataclass
class PagingCursors:
    before: str
    after: str

@dataclass
class Paging:
    cursors: PagingCursors
    next: str

@dataclass
class MessageResponse:
    data: List[MessageData]
    paging: Paging

def get_all_messages_by_conversation_id(access_token: str, conversation_id: str, next_url: str) -> Optional[MessageResponse]:
    logger.info(f"Starting to get all messages for conversation id: {conversation_id}")
    url = next_url if next_url else f'https://graph.facebook.com/v13.0/{conversation_id}/messages?access_token={access_token}'
    response = requests.get(url)
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


# Get Message Details by Message ID

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

def get_message_by_message_id(access_token: str, message_id: str) -> Optional[MessageDetailResponse]:
    logger.info(f"Starting to get message details for message id: {message_id}")
    url = f'https://graph.facebook.com/v13.0/{message_id}?fields=message,from,to,attachments&access_token={access_token}'
    response = requests.get(url)
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


# Get User Profile

@dataclass
class UserProfileData:
    first_name: str
    last_name: str
    profile_pic: str
    id: str

@dataclass
class UserProfileResponse:
    data: UserProfileData

def get_user_profile_by_id(access_token: str, user_id: str) -> Optional[UserProfileResponse]:
    logger.info(f"Starting to get user profile details for user id: {user_id}")
    url = f'https://graph.facebook.com/v13.0/{user_id}?fields=first_name,last_name,profile_pic&access_token={access_token}'
    response = requests.get(url)
    if response.status_code == 200:
        logger.info("Successfully received response")
        response_data = response.json()
        user_profile_data = UserProfileData(**response_data)
        logger.info("Successfully parsed response data")
        return UserProfileResponse(data=user_profile_data)
    else:
        logger.error(f"Failed to get response, status code: {response.status_code}")
        return None

# Send Message

@dataclass
class SendMessageData:
    recipient_id: str
    message_id: str

@dataclass
class SendMessageResponse:
    data: SendMessageData

def send_message(access_token: str, recipient_id: str, message: str, tag: str) -> Optional[SendMessageResponse]:
    logger.info(f"Starting to send message to recipient id: {recipient_id}")
    url = f'https://graph.facebook.com/v13.0/me/messages?access_token={access_token}'
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message
        },
        "tag": tag
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        logger.info("Successfully sent message")
        response_data = response.json()
        send_message_data = SendMessageData(
            recipient_id=response_data.get('recipient_id', ''), 
            message_id=response_data.get('message_id', '')
        )
        logger.info("Successfully parsed response data")
        return SendMessageResponse(data=send_message_data)
    else:
        logger.error(f"Failed to send message, status code: {response.status_code}")
        logger.error(f"Failed to send message, error: {response.json()}")
        return None


def send_template_message(user_id: str, template_content: dict, delay: int, access_token: str) -> Optional[SendMessageResponse]:
    import time

    logger.info(f"Starting to send template message to user id: {user_id}")
    url = f'https://graph.facebook.com/v13.0/me/messages?access_token={access_token}'
    headers = {
        'Content-Type': 'application/json',
    }
    # Replace user_id in template_content
    template_content["recipient"]["id"] = user_id
    data = template_content
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        logger.info("Successfully sent template message")
        response_data = response.json()
        send_message_data = SendMessageData(
            recipient_id=response_data.get('recipient_id', ''), 
            message_id=response_data.get('message_id', '')
        )
        logger.info("Successfully parsed response data")
        logger.info(f"Delaying for {delay} seconds before sending the next message")
        time.sleep(delay)
        return SendMessageResponse(data=send_message_data)
    else:
        logger.error(f"Failed to send template message, status code: {response.status_code}")
        logger.error(f"Failed to send template message, error: {response.json()}")
        return None
