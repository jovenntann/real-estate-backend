from django.utils import timezone
from typing import List

# Models
from domain.system.models.Company import Company
from domain.lead.models.Status import Status
from domain.lead.models.Lead import Lead

import logging
logger = logging.getLogger(__name__)


def get_leads() -> List[Lead]:
    leads = Lead.objects.all().order_by('id')
    logger.info(f"{leads} fetched")
    return leads


def get_lead_by_id(lead_id: int) -> Lead:
    lead = Lead.objects.filter(id=lead_id).first()
    logger.info(f"{lead} fetched")
    return lead


def delete_lead(lead: Lead) -> Lead:
    lead.delete()
    logger.info(f"{lead} has been deleted.")
    return lead


def create_lead(first_name: str, last_name: str, email: str, phone_number: str, company: Company, status: Status) -> Lead:
    lead = Lead.objects.create(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, company=company, status=status)
    logger.info(f"\"{lead}\" has been created.")
    return lead

def update_lead(
        lead: Lead,
        new_first_name: str,
        new_last_name: str,
        new_email: str,
        new_phone_number: str,
        new_company: Company,
        new_status: int
    ) -> Lead:
    lead.first_name = new_first_name
    lead.last_name = new_last_name
    lead.email = new_email
    lead.phone_number = new_phone_number
    lead.company = new_company
    lead.status_id = new_status
    lead.updated_at = timezone.now()
    lead.save()
    logger.info(f"\"{lead}\" has been updated.")
    return lead
