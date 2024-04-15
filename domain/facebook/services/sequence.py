from typing import List

# Models
from domain.facebook.models.Page import Page
from domain.facebook.models.Sequence import Sequence

import logging
logger = logging.getLogger(__name__)


def get_sequences() -> List[Sequence]:
    sequences = Sequence.objects.all().order_by('id')
    logger.info(f"{sequences} fetched")
    return sequences


def get_sequence_by_id(id: int) -> Sequence:
    sequence = Sequence.objects.filter(id=id).first()
    logger.info(f"{sequence} fetched")
    return sequence


def delete_sequence(sequence: Sequence) -> Sequence:
    sequence.delete()
    logger.info(f"{sequence} has been deleted.")
    return sequence


def create_sequence(page: Page, name: str) -> Sequence:
    sequence = Sequence.objects.create(page=page, name=name)
    logger.info(f"\"{sequence}\" has been created.")
    return sequence

def update_sequence(
        sequence: Sequence,
        new_page: Page,
        new_name: str
    ) -> Sequence:
    sequence.page = new_page
    sequence.name = new_name
    sequence.save()
    logger.info(f"\"{sequence}\" has been updated.")
    return sequence

def get_sequences_by_page(page: Page) -> List[Sequence]:
    sequences = Sequence.objects.filter(page=page).order_by('id')
    logger.info(f"{sequences} fetched by page")
    return sequences
