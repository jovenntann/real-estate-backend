from typing import List

# Models
from domain.facebook.models.Page import Page

import logging
logger = logging.getLogger(__name__)


def get_pages() -> List[Page]:
    pages = Page.objects.all().order_by('id')
    logger.info(f"{pages} fetched")
    return pages


def get_page_by_page_id(page_id: int) -> Page:
    page = Page.objects.filter(page_id=page_id).first()
    logger.info(f"{page} fetched")
    return page


def delete_page(page: Page) -> Page:
    page.delete()
    logger.info(f"{page} has been deleted.")
    return page


def create_page(page_name: str, page_id: str, access_token: str) -> Page:
    page = Page.objects.create(page_name=page_name, page_id=page_id, access_token=access_token)
    logger.info(f"\"{page}\" has been created.")
    return page

def update_page(
        page: Page,
        new_page_name: str,
        new_page_id: str,
        new_access_token: str
    ) -> Page:
    page.page_name = new_page_name
    page.page_id = new_page_id
    page.access_token = new_access_token
    page.save()
    logger.info(f"\"{page}\" has been updated.")
    return page
