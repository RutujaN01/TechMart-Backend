from bson import ObjectId
from django.test import TestCase
from django.contrib.auth.hashers import check_password

from users.models import User


class UserModelTest(TestCase):

    def setUp(self):
        if User.objects.filter(username='testuser').count() > 0:
            User.objects.get(username='testuser').delete()
        self.user_id = ObjectId()
        self.user = User(
            id=self.user_id,
            username='testuser',
            password='ToughPassword123!@#',
            email='testuser@example.com',
            roles=['user']
        )

        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_create_user(self):
        if User.objects.filter(username='newuser').count() > 0:
            User.objects.get(username='newuser').delete()
        user = User(
            id=ObjectId(),
            username='newuser',
            password='ToughPassword123!@#',
            email='newuser@example.com',
            roles=['user']
        )
        user.save()

        found_user = User.objects.get(id=user.id)

        self.assertEqual(found_user.username, 'newuser')
        self.assertEqual(found_user.email, 'newuser@example.com')
        self.assertIn('user', user.roles)

        user.delete()

    def test_create_user_with_invalid_email(self):
        with self.assertRaises(Exception):
            user = User(
                id=ObjectId(),
                username='newuser',
                email='newuser',
                roles=['user']
            )
            user.save()

    def test_create_user_with_invalid_role(self):
        with self.assertRaises(Exception):
            user = User(
                id=ObjectId(),
                username='newuser',
                email='newuser@gmail.com',
                roles=['invalid']
            )
            user.save()

    def test_retrieve_user(self):
        user = User.objects.get(id=self.user_id)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')

    def test_update_user_username(self):
        user = User.objects.get(id=self.user_id)
        user.username = 'updateduser'
        user.save()
        updated_user = User.objects.get(id=self.user_id)
        self.assertEqual(updated_user.username, 'updateduser')

    def test_update_user_email(self):
        user = User.objects.get(id=self.user_id)
        user.email = 'newemail@gmail.com'
        user.save()
        updated_user = User.objects.get(id=self.user_id)
        self.assertEqual(updated_user.email, 'newemail@gmail.com')

    def test_update_user_password(self):
        user = User.objects.get(id=self.user_id)
        user.password = 'NewPassword'
        user.save()

        updated_user = User.objects.get(id=self.user_id)

        # Ensure the password is hashed
        self.assertNotEqual(updated_user.password, 'NewPassword')

        # Ensure the password is verified
        self.assertTrue(check_password('NewPassword', updated_user.password))

    def test_delete_user(self):
        user = User.objects.get(id=self.user_id)
        user.delete()
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.user_id)

    def test_user_roles(self):
        user = User.objects.get(id=self.user_id)
        self.assertIn('user', user.roles)
        user.roles.append('admin')
        user.save()
        updated_user = User.objects.get(id=self.user_id)
        self.assertIn('admin', updated_user.roles)
        user.roles.remove('admin')
