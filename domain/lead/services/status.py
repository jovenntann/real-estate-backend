from django.utils import timezone
from typing import List

# Models
from domain.lead.models.Status import Status

import logging
logger = logging.getLogger(__name__)


def get_statuses() -> List[Status]:
    statuses = Status.objects.all().order_by('id')
    logger.info(f"{statuses} fetched")
    return statuses


def get_status_by_id(id: int) -> Status:
    status = Status.objects.filter(id=id).first()
    logger.info(f"{status} fetched")
    return status


def delete_status(status: Status) -> Status:
    status.delete()
    logger.info(f"{status} has been deleted.")
    return status


def create_status(status_name: str) -> Status:
    status = Status.objects.create(status=status_name)
    logger.info(f"\"{status}\" has been created.")
    return status


def update_status(
        status: Status,
        new_status_name: str
    ) -> Status:
    status.status = new_status_name
    status.updated_at = timezone.now()
    status.save()
    logger.info(f"\"{status}\" has been updated.")
    return status
