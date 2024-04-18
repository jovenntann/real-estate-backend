from datetime import datetime
from django.utils import timezone
from typing import List

# Models
from domain.system.models.Company import Company
from domain.lead.models.Status import Status
from domain.lead.models.MessageStatus import MessageStatus
from domain.lead.models.NextAction import NextAction
from domain.lead.models.Lead import Lead

import logging
logger = logging.getLogger(__name__)


def get_leads() -> List[Lead]:
    leads = Lead.objects.all().order_by('id')
    logger.info(f"{leads} fetched")
    return leads


def get_leads_sorted_by_last_message_at() -> List[Lead]:
    leads = Lead.objects.filter(last_message_at__isnull=False).order_by('-last_message_at')
    logger.info(f"{len(leads)} leads fetched")
    return leads


def get_lead_by_id(lead_id: int) -> Lead:
    lead = Lead.objects.filter(id=lead_id).first()
    logger.info(f"{lead} fetched")
    return lead


def delete_lead(lead: Lead) -> Lead:
    lead.delete()
    logger.info(f"{lead} has been deleted.")
    return lead


def create_lead(
        first_name: str, 
        last_name: str, 
        email: str, 
        phone_number: str, 
        company: Company, 
        status: Status,  
        facebook_id: str = None, 
        facebook_profile_pic: str = None, 
        message_status: MessageStatus = None,
        next_action: NextAction = None,
    ) -> Lead:
    
    lead = Lead.objects.create(
        first_name=first_name, 
        last_name=last_name, 
        email=email, 
        phone_number=phone_number, 
        company=company, 
        status=status, 
        next_action=next_action, 
        facebook_id=facebook_id, 
        facebook_profile_pic=facebook_profile_pic, 
        message_status=message_status
    )
    logger.info(f"\"{lead}\" has been created.")
    return lead

def update_lead(
        lead: Lead,
        new_first_name: str = None,
        new_last_name: str = None,
        new_email: str = None,
        new_phone_number: str = None,
        new_company: Company = None,
        new_status: Status = None,
        new_facebook_id: str = None,
        new_last_message_at: datetime = None,
        new_message_status: MessageStatus = None,
        new_next_action: NextAction = None
    ) -> Lead:
    
    lead_fields = {
        'first_name': new_first_name,
        'last_name': new_last_name,
        'email': new_email,
        'phone_number': new_phone_number,
        'company': new_company,
        'status': new_status,
        'next_action': new_next_action,
        'facebook_id': new_facebook_id,
        'last_message_at': new_last_message_at,
        'message_status': new_message_status
    }

    for field, value in lead_fields.items():
        if value is not None:
            setattr(lead, field, value)

    lead.updated_at = timezone.now()
    lead.save()
    logger.info(f"\"{lead}\" has been updated.")
    return lead


def get_lead_by_facebook_id(facebook_id: str) -> Lead:
    lead = Lead.objects.filter(facebook_id=facebook_id).first()
    logger.info(f"{lead} fetched")
    return lead


def update_lead_last_message_at(lead: Lead, last_message_at: datetime) -> Lead:
    lead.last_message_at = last_message_at
    lead.updated_at = timezone.now()
    lead.save()
    logger.info(f"\"{lead}\" last message at has been updated.")
    return lead
