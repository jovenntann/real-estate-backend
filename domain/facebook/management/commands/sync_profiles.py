from django.core.management.base import BaseCommand

# Importing services and utilities
from domain.lead.services.lead import get_leads, patch_lead
from domain.facebook.services.page import get_page_by_page_id
from domain.facebook.utils.facebook import get_user_profile_by_id

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Create system sample data'
    def handle(self, *args, **options):
        page = get_page_by_page_id(page_id=113575558420278)
        leads = get_leads()
        for lead in leads:
            logger.info(f"Processing lead: {lead}")
            user_profile = get_user_profile_by_id(access_token=page.access_token, user_id=lead.facebook_id)
            logger.info(f"User profile: {user_profile}")

            if user_profile and user_profile.data:
                patch_lead(lead=lead, facebook_profile_pic=user_profile.data.profile_pic or 'https://cdn.pixabay.com/photo/2013/07/13/10/44/man-157699_640.png')
