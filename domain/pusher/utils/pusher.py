import os
import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

import logging
from pusher import Pusher

logger = logging.getLogger(__name__)

pusher = Pusher(
    app_id=os.getenv('PUSHER_APP_ID'),
    key=os.getenv('PUSHER_KEY'),
    secret=os.getenv('PUSHER_SECRET'),
    cluster=os.getenv('PUSHER_CLUSTER'),
    ssl=True
)

def send_pusher_notification(channel: str, event: str, data: Dict[str, Any]) -> None:
    logger.info(f"Sending pusher notification to channel: {channel}, event: {event}")
    pusher.trigger(channel, event, data)
    logger.info("Successfully sent pusher notification")

def get_pusher_channels() -> List[str]:
    logger.info("Getting all pusher channels")
    channels = pusher.channels_info()['channels']
    logger.info("Successfully received all pusher channels")
    return list(channels.keys())

def get_pusher_channel_users(channel: str) -> List[str]:
    logger.info(f"Getting all users in pusher channel: {channel}")
    users = pusher.channel_users(channel)['users']
    logger.info("Successfully received all users in pusher channel")
    return [user['id'] for user in users]
