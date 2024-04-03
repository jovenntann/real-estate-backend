from django.test import TestCase
from django.contrib.auth.hashers import make_password
from ...services.user import (
    get_users, 
    get_user_by_id,
    get_user_by_email,
    delete_user, 
    create_user, 
    update_user,
    change_password,
    reset_password
)
from domain.user.models.User import User


def create_test_user() -> User:
    user = User.objects.create(
        username="test_user",
        password=make_password('test_password'),
        first_name="Test",
        last_name="User",
        email="test_user@test.com"
    )
    return user


class TestServiceUserGetUsers(TestCase):

    def test_get_all_users(self):
        """Should return all users"""
        user = create_test_user()
        users = get_users()
        self.assertIn(user, users)


class TestServiceUserGetUserById(TestCase):

    def test_get_user_by_id(self):
        """Should be able to get user object by id"""
        user = create_test_user()
        user = get_user_by_id(user.pk)
        self.assertTrue(user)

    def test_return_none_if_user_id_not_exist(self):
        """Should return None if user id do not exist"""
        create_test_user()
        not_existing_user_id = 0
        user = get_user_by_id(not_existing_user_id)
        self.assertIsNone(user)

class TestServiceUserGetUserByEmail(TestCase):

    def test_get_user_by_email(self):
        """Should be able to get user object by email"""
        user = create_test_user()
        user = get_user_by_email(user.email)
        self.assertTrue(user)

    def test_return_none_if_user_email_not_exist(self):
        """Should return None if user email do not exist"""
        create_test_user()
        not_existing_user_email = "not_existing@test.com"
        user = get_user_by_email(not_existing_user_email)
        self.assertIsNone(user)


class TestServiceUserDeleteUser(TestCase):

    def test_delete_user(self):
        """Should be able to delete user by object"""
        user = create_test_user()
        deleted_user_object = delete_user(user)
        self.assertEqual(user, deleted_user_object)


class TestServiceUserCreateUser(TestCase):

    def test_create_user(self):
        """Should be able to create a user"""
        user = create_user(
            'test_user',
            'test_password',
            'Test',
            'User',
            'test_user@test.com'
        )
        self.assertEqual({
            'username': 'test_user',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test_user@test.com'
        }, {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        })

class TestServiceUserUpdateUser(TestCase):

    def test_update_user(self):
        """Should be able to update a user"""
        user = create_test_user()
        updated_user = update_user(
            user,
            'updated_user',
            'updated_password',
            'Updated',
            'User',
            'updated_user@test.com'
        )
        self.assertEqual({
            'username': 'updated_user',
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updated_user@test.com'
        }, {
            'username': updated_user.username,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email,
        })

class TestServiceUserChangePassword(TestCase):

    def test_change_password(self):
        """Should be able to change a user's password"""
        user = create_test_user()
        new_password = 'new_password'
        updated_user = change_password(user, new_password)
        self.assertTrue(updated_user.check_password(new_password))

class TestServiceUserResetPassword(TestCase):

    def test_reset_password(self):
        """Should be able to reset a user's password"""
        user = create_test_user()
        new_password = 'reset_password'
        reset_status = reset_password(user, new_password)
        self.assertTrue(reset_status)
        self.assertTrue(user.check_password(new_password))
