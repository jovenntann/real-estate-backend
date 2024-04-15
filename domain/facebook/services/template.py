from typing import List

# Models
from domain.facebook.models.Page import Page
from domain.facebook.models.Template import Template
from domain.facebook.models.Sequence import Sequence

import logging
logger = logging.getLogger(__name__)


def get_templates() -> List[Template]:
    templates = Template.objects.all().order_by('id')
    logger.info(f"{templates} fetched")
    return templates


def get_template_by_id(template_id: int) -> Template:
    template = Template.objects.filter(id=template_id).first()
    logger.info(f"{template} fetched")
    return template


def delete_template(template: Template) -> Template:
    template.delete()
    logger.info(f"{template} has been deleted.")
    return template


def create_template(page: Page, template_name: str, template_type: str, template_content: dict, sequence: Sequence, order: int, delay: int) -> Template:
    template = Template.objects.create(page=page, template_name=template_name, template_type=template_type, template_content=template_content, sequence=sequence, order=order, delay=delay)
    logger.info(f"\"{template}\" has been created.")
    return template

def update_template(
        template: Template,
        new_page: Page,
        new_template_name: str,
        new_template_type: str,
        new_template_content: dict,
        new_sequence: Sequence,
        new_order: int,
        new_delay: int
    ) -> Template:
    template.page = new_page
    template.template_name = new_template_name
    template.template_type = new_template_type
    template.template_content = new_template_content
    template.sequence = new_sequence
    template.order = new_order
    template.delay = new_delay
    template.save()
    logger.info(f"\"{template}\" has been updated.")
    return template

def get_templates_by_sequence_order(sequence: Sequence) -> List[Template]:
    templates = Template.objects.filter(sequence=sequence).order_by('order')
    logger.info(f"{templates} fetched by sequence order")
    return templates
