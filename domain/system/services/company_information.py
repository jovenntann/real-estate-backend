from django.utils import timezone
from typing import List

# Models
from domain.system.models.CompanyInformation import CompanyInformation

import logging
logger = logging.getLogger(__name__)


def get_companies() -> List[CompanyInformation]:
    companies = CompanyInformation.objects.all().order_by('id')
    logger.info(f"{companies} fetched")
    return companies


def get_company_by_id(company_id: int) -> CompanyInformation:
    company = CompanyInformation.objects.filter(id=company_id).first()
    logger.info(f"{company} fetched")
    return company


def delete_company(company: CompanyInformation) -> CompanyInformation:
    company.delete()
    logger.info(f"{company} has been deleted.")
    return company


def create_company(company_name: str, address: str, phone_number: str, company_size: int, industry: str) -> CompanyInformation:
    company = CompanyInformation.objects.create(company_name=company_name, address=address, phone_number=phone_number, company_size=company_size, industry=industry)
    logger.info(f"\"{company}\" has been created.")
    return company


def update_company(
        company: CompanyInformation,
        new_company_name: str,
        new_address: str,
        new_phone_number: str,
        new_company_size: int,
        new_industry: str
    ) -> CompanyInformation:
    company.company_name = new_company_name
    company.address = new_address
    company.phone_number = new_phone_number
    company.company_size = new_company_size
    company.industry = new_industry
    company.updated_at = timezone.now()
    company.save()
    logger.info(f"\"{company}\" has been updated.")
    return company
