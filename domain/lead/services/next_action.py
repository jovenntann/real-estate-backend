from django.utils import timezone
from typing import List

# Models
from domain.lead.models.NextAction import NextAction

import logging
logger = logging.getLogger(__name__)


def get_next_actions() -> List[NextAction]:
    next_actions = NextAction.objects.all().order_by('id')
    logger.info(f"{next_actions} fetched")
    return next_actions


def get_next_action_by_id(id: int) -> NextAction:
    next_action = NextAction.objects.filter(id=id).first()
    logger.info(f"{next_action} fetched")
    return next_action


def delete_next_action(next_action: NextAction) -> NextAction:
    next_action.delete()
    logger.info(f"{next_action} has been deleted.")
    return next_action

