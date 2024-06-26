from django.utils import timezone
from typing import List

# Models
from domain.system.models.Gender import Gender

import logging
logger = logging.getLogger(__name__)


def get_genders() -> List[Gender]:
    genders = Gender.objects.all().order_by('id')
    logger.info(f"{genders} fetched")
    return genders


def get_gender_by_id(gender_id: int) -> Gender:
    gender = Gender.objects.filter(id=gender_id).first()
    logger.info(f"{gender} fetched")
    return gender


def delete_gender(gender: Gender) -> Gender:
    gender.delete()
    logger.info(f"{gender} has been deleted.")
    return gender


def create_gender(gender_name: str) -> Gender:
    gender = Gender.objects.create(gender=gender_name)
    logger.info(f"\"{gender}\" has been created.")
    return gender


def update_gender(
        gender: Gender,
        new_gender_name: str
    ) -> Gender:
    gender.gender = new_gender_name
    gender.updated_at = timezone.now()
    gender.save()
    logger.info(f"\"{gender}\" has been updated.")
    return gender
