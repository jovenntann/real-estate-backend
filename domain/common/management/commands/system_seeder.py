from django.core.management.base import BaseCommand

# OS
import random

# Library: faker
from faker import Faker
fake = Faker()

# System Domain
from domain.system.models.Gender import Gender
from domain.system.models.Company import Company
from domain.lead.models.Lead import Lead
from domain.system.models.LeadStatus import LeadStatus

class Command(BaseCommand):
    help = 'Create system sample data'

    def handle(self, *args, **options):

        genders = [
            'Male',
            'Female',
        ]

        for gender in genders:
            Gender.objects.get_or_create(gender=gender)
            self.stdout.write(self.style.SUCCESS('Successfully created gender "%s"' % gender))

        company_information = [
            {
                'company_name': 'Tappy Inc.',
                'address': 'BGC, Taguig',
                'phone_number': '+639062131607',
                'company_size': 100,
                'industry': 'Software Development'
            },
        ]

        for company in company_information:
            Company.objects.get_or_create(**company)
            self.stdout.write(self.style.SUCCESS('Successfully created company information "%s"' % company['company_name']))

        lead_statuses = [
            'New',
            'Contacted',
            'Qualified',
            'Lost',
            'Won',
        ]

        for status in lead_statuses:
            LeadStatus.objects.get_or_create(status=status)
            self.stdout.write(self.style.SUCCESS('Successfully created lead status "%s"' % status))

        for i in range(10):
            lead = {
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'email': fake.email(),
                'phone_number': fake.phone_number(),
                'company': Company.objects.get(company_name='Tappy Inc.'),
                'status': LeadStatus.objects.get(status=random.choice(lead_statuses)),
            }

            Lead.objects.get_or_create(**lead)
            self.stdout.write(self.style.SUCCESS('Successfully created lead "%s %s"' % (lead['first_name'], lead['last_name'])))