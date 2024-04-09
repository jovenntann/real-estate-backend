from django.test import TestCase
from ...services.lead import (
    get_leads, 
    get_lead_by_id,
    delete_lead, 
    update_lead,
    get_lead_by_facebook_id
)
from domain.lead.models.Lead import Lead
from domain.system.models.Company import Company
from domain.lead.models.Status import Status


def create_test_lead() -> Lead:
    company = Company.objects.create(
        company_name="test_company",
        address="test_address",
        phone_number="1234567890",
        company_size=100,
        industry="test_industry"
    )
    status = Status.objects.create(
        status="test_status"
    )
    lead = Lead.objects.create(
        first_name="test_first_name",
        last_name="test_last_name",
        email="test_email",
        phone_number="1234567890",
        company=company,
        status=status
    )
    return lead


class TestServiceLeadGetLeads(TestCase):

    def test_get_all_leads(self):
        """Should return all leads"""
        lead = create_test_lead()
        leads = get_leads()
        self.assertIn(lead, leads)


class TestServiceLeadGetLeadById(TestCase):

    def test_get_lead_by_id(self):
        """Should be able to get lead object by id"""
        lead = create_test_lead()
        lead = get_lead_by_id(lead.pk)
        self.assertTrue(lead)

    def test_return_none_if_lead_id_not_exist(self):
        """Should return None if lead id do not exist"""
        create_test_lead()
        not_existing_lead_id = 0
        lead = get_lead_by_id(not_existing_lead_id)
        self.assertIsNone(lead)


class TestServiceLeadDeleteLead(TestCase):

    def test_delete_lead(self):
        """Should be able to delete lead by object"""
        lead = create_test_lead()
        deleted_lead_object = delete_lead(lead)
        self.assertEqual(lead, deleted_lead_object)


class TestServiceLeadCreateLead(TestCase):

    def test_create_lead(self):
        """Should be able to create a lead"""
        lead = create_test_lead()
        self.assertEqual({
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'email': 'test_email',
            'phone_number': '1234567890',
            'company': lead.company,
            'status': lead.status,
        }, {
            'first_name': lead.first_name,
            'last_name': lead.last_name,
            'email': lead.email,
            'phone_number': lead.phone_number,
            'company': lead.company,
            'status': lead.status,
        })


class TestServiceLeadUpdateLead(TestCase):

    def test_update_lead(self):
        """Should be able to update a lead"""
        lead = create_test_lead()
        updated_lead = update_lead(
            lead,
            'updated_first_name',
            'updated_last_name',
            'updated_email',
            '0987654321',
            lead.company,
            lead.status.pk
        )
        self.assertEqual({
            'first_name': 'updated_first_name',
            'last_name': 'updated_last_name',
            'email': 'updated_email',
            'phone_number': '0987654321',
            'company': updated_lead.company,
            'status': updated_lead.status,
        }, {
            'first_name': updated_lead.first_name,
            'last_name': updated_lead.last_name,
            'email': updated_lead.email,
            'phone_number': updated_lead.phone_number,
            'company': updated_lead.company,
            'status': updated_lead.status,
        })


class TestServiceLeadGetByFacebookId(TestCase):

    def test_get_lead_by_facebook_id(self):
        """Should be able to get a lead by facebook id"""
        lead = create_test_lead()
        fetched_lead = get_lead_by_facebook_id(lead.facebook_id)
        self.assertEqual({
            'first_name': lead.first_name,
            'last_name': lead.last_name,
            'email': lead.email,
            'phone_number': lead.phone_number,
            'company': lead.company,
            'status': lead.status,
            'facebook_id': lead.facebook_id
        }, {
            'first_name': fetched_lead.first_name,
            'last_name': fetched_lead.last_name,
            'email': fetched_lead.email,
            'phone_number': fetched_lead.phone_number,
            'company': fetched_lead.company,
            'status': fetched_lead.status,
            'facebook_id': fetched_lead.facebook_id
        })
