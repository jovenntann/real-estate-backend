from django.utils import timezone
from typing import List

# Models
from domain.user.models.User import User
from domain.system.models.Gender import Gender
from domain.user.models.Profile import Profile

import logging
logger = logging.getLogger(__name__)

def get_profiles() -> List[Profile]:
    profiles = Profile.objects.all().order_by('id')
    logger.info(f"{profiles} fetched")
    return profiles

def get_profile_by_id(profile_id: int) -> Profile:
    profile = Profile.objects.filter(id=profile_id).first()
    logger.info(f"{profile} fetched")
    return profile

def delete_profile(profile: Profile) -> Profile:
    profile.delete()
    logger.info(f"{profile} has been deleted.")
    return profile

def create_profile(bio: str, birth_date: str, civil_status: str, gender: Gender, phone_number: str, user: User) -> Profile:
    profile = Profile.objects.create(bio=bio, birth_date=birth_date, civil_status=civil_status, gender=gender, phone_number=phone_number, user=user)
    logger.info(f"\"{profile}\" has been created.")
    return profile

def update_profile(
        profile: Profile,
        new_bio: str,
        new_birth_date: str,
        new_civil_status: str,
        new_gender: Gender,
        new_phone_number: str,
        new_user: User
    ) -> Profile:
    profile.bio = new_bio
    profile.birth_date = new_birth_date
    profile.civil_status = new_civil_status
    profile.gender = new_gender
    profile.phone_number = new_phone_number
    profile.user = new_user
    profile.updated_at = timezone.now()
    profile.save()
    logger.info(f"\"{profile}\" has been updated.")
    return profile
