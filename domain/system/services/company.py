from django.utils import timezone
from typing import List

# Models
from domain.system.models.Company import Company

import logging
logger = logging.getLogger(__name__)


def get_companies() -> List[Company]:
    companies = Company.objects.all().order_by('id')
    logger.info(f"{companies} fetched")
    return companies


def get_company_by_id(id: int) -> Company:
    company = Company.objects.filter(id=id).first()
    logger.info(f"{company} fetched")
    return company


def delete_company(company: Company) -> Company:
    company.delete()
    logger.info(f"{company} has been deleted.")
    return company


def create_company(company_name: str, address: str, phone_number: str, company_size: int, industry: str) -> Company:
    company = Company.objects.create(company_name=company_name, address=address, phone_number=phone_number, company_size=company_size, industry=industry)
    logger.info(f"\"{company}\" has been created.")
    return company


def update_company(
        company: Company,
        new_company_name: str,
        new_address: str,
        new_phone_number: str,
        new_company_size: int,
        new_industry: str
    ) -> Company:
    company.company_name = new_company_name
    company.address = new_address
    company.phone_number = new_phone_number
    company.company_size = new_company_size
    company.industry = new_industry
    company.updated_at = timezone.now()
    company.save()
    logger.info(f"\"{company}\" has been updated.")
    return company
