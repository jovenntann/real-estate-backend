from django.core.management.base import BaseCommand

# System Domain
from domain.system.models.Gender import Gender
from domain.system.models.CompanyInformation import CompanyInformation

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
            CompanyInformation.objects.get_or_create(**company)
            self.stdout.write(self.style.SUCCESS('Successfully created company information "%s"' % company['company_name']))
