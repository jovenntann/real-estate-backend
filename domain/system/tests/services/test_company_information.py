from django.test import TestCase
from ...services.company import (
    get_companies, 
    get_company_by_id,
    delete_company, 
    create_company, 
    update_company
)
from domain.system.models.Company import Company


def create_test_company() -> Company:
    company = Company.objects.create(
        company_name="test_company",
        address="test_address",
        phone_number="1234567890",
        company_size=100,
        industry="test_industry"
    )
    return company


class TestServiceCompanyGetCompanies(TestCase):

    def test_get_all_companies(self):
        """Should return all companies"""
        company = create_test_company()
        companies = get_companies()
        self.assertIn(company, companies)


class TestServiceCompanyGetCompanyById(TestCase):

    def test_get_company_by_id(self):
        """Should be able to get company object by id"""
        company = create_test_company()
        company = get_company_by_id(company.pk)
        self.assertTrue(company)

    def test_return_none_if_company_id_not_exist(self):
        """Should return None if company id do not exist"""
        create_test_company()
        not_existing_company_id = 0
        company = get_company_by_id(not_existing_company_id)
        self.assertIsNone(company)


class TestServiceCompanyDeleteCompany(TestCase):

    def test_delete_company(self):
        """Should be able to delete company by object"""
        company = create_test_company()
        deleted_company_object = delete_company(company)
        self.assertEqual(company, deleted_company_object)


class TestServiceCompanyCreateCompany(TestCase):

    def test_create_company(self):
        """Should be able to create a company"""
        company = create_company(
            'test_company',
            'test_address',
            '1234567890',
            100,
            'test_industry'
        )
        self.assertEqual({
            'company_name': 'test_company',
            'address': 'test_address',
            'phone_number': '1234567890',
            'company_size': 100,
            'industry': 'test_industry'
        }, {
            'company_name': company.company_name,
            'address': company.address,
            'phone_number': company.phone_number,
            'company_size': company.company_size,
            'industry': company.industry,
        })


class TestServiceCompanyUpdateCompany(TestCase):

    def test_update_company(self):
        """Should be able to update a company"""
        company = create_test_company()
        updated_company = update_company(
            company,
            'updated_company',
            'updated_address',
            '0987654321',
            200,
            'updated_industry'
        )
        self.assertEqual({
            'company_name': 'updated_company',
            'address': 'updated_address',
            'phone_number': '0987654321',
            'company_size': 200,
            'industry': 'updated_industry'
        }, {
            'company_name': updated_company.company_name,
            'address': updated_company.address,
            'phone_number': updated_company.phone_number,
            'company_size': updated_company.company_size,
            'industry': updated_company.industry,
        })
