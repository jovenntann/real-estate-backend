from django.test import TestCase
from ...services.gender import (
    get_genders, 
    get_gender_by_id,
    delete_gender, 
    create_gender, 
    update_gender
)
from domain.system.models.Gender import Gender


def create_test_gender() -> Gender:
    gender = Gender.objects.create(gender="test_gender")
    return gender


class TestServiceGenderGetGenders(TestCase):

    def test_get_all_genders(self):
        """Should return all genders"""
        gender = create_test_gender()
        genders = get_genders()
        self.assertIn(gender, genders)


class TestServiceGenderGetGenderById(TestCase):

    def test_get_gender_by_id(self):
        """Should be able to get gender object by id"""
        gender = create_test_gender()
        gender = get_gender_by_id(gender.pk)
        self.assertTrue(gender)

    def test_return_none_if_gender_id_not_exist(self):
        """Should return None if gender id do not exist"""
        create_test_gender()
        not_existing_gender_id = 0
        gender = get_gender_by_id(not_existing_gender_id)
        self.assertIsNone(gender)

class TestServiceGenderDeleteGender(TestCase):

    def test_delete_gender(self):
        """Should be able to delete gender by object"""
        gender = create_test_gender()
        deleted_gender_object = delete_gender(gender)
        self.assertEqual(gender, deleted_gender_object)


class TestServiceGenderCreateGender(TestCase):

    def test_create_gender_already_exist(self):
        """Should not be able to create a gender that already exists"""
        create_gender('female')
        with self.assertRaises(Exception):
            create_gender('female')


class TestServiceGenderUpdateGender(TestCase):

    def test_update_gender(self):
        """Should be able to update a gender"""
        gender = create_test_gender()
        updated_gender = update_gender(gender, 'updated_gender')
        self.assertEqual('updated_gender', updated_gender.gender)
