from bson import ObjectId
from django.test import TestCase
from mongoengine import DoesNotExist
from rest_framework.test import APIClient

from items.models import Items
from users.models import User
from wishlists.models import Wishlists


# https://docs.mongoengine.org/guide/querying.html Object


class WishlistModelTest(TestCase):
    def setUp(self):
        if User.objects.filter(username='testuser11').count() > 0:
            User.objects.get(username='testuser11').delete()
        self.user = User(
            google_id='test_google_id',
            username='testuser11',
            password='ToughPassword123!@#',
            email='testuserr@example.com',
            roles=['user']
        )
        self.user.save()

        if Items.objects.filter(name='testitem1').count() > 0:
            Items.objects.get(name='testitem1').delete()
        self.item1 = Items(
            id=ObjectId(),
            name='testitem1',
            price=19.99,
            description='Item 1',
            category='testcategory'
        )
        self.item1.save()

        if Items.objects.filter(name='testitem2').count() > 0:
            Items.objects.get(name='testitem2').delete()
        self.item2 = Items(
            id=ObjectId(),
            name='testitem2',
            price=49.99,
            description='Item 2',
            category='testcategory'
        )
        self.item2.save()

        if Wishlists.objects.filter(name='Holloween').count() > 0:
            Wishlists.objects.get(name='Holloween').delete()
        self.wishlist_id = ObjectId()
        self.wishlist = Wishlists(
            id=self.wishlist_id,
            name='Holloween',
            user=self.user,
            items=[self.item1, self.item2]
        )
        self.wishlist.save()

    def tearDown(self):
        self.wishlist.delete()
        self.item1.delete()
        self.item2.delete()
        self.user.delete()

    # https://docs.mongoengine.org/guide/querying.html 2.5.10. Atomic updates¶
    def test_add_items_to_wishlist(self):
        if Items.objects.filter(name='testitem3').count() > 0:
            Items.objects.get(name='testitem3').delete()
        new_item = Items(
            id=ObjectId(),
            name='testitem3',
            price=119.99,
            description='Item 3',
            category='testcategory'
        )
        self.wishlist.items.append(new_item)
        self.wishlist.save()

        updated_wishlist = Wishlists.objects.get(id=self.wishlist.id)
        self.assertIn(new_item, updated_wishlist.items)

        new_item.delete()

    def test_remove_items_from_wishlist(self):
        self.wishlist.items.remove(self.item1)
        self.wishlist.save()
        self.assertNotIn(self.item1, self.wishlist.items)

    def test_retrieve_wishlist_items(self):
        wishlist_items = self.wishlist.items
        self.assertEqual(len(wishlist_items), 2)  # this makes sure that the 2 items in there
        self.assertIn(self.item1, wishlist_items)
        self.assertIn(self.item2, wishlist_items)

    def test_clear_wishlist(self):
        self.wishlist.items = []
        self.wishlist.save()
        wishlist_items = self.wishlist.items
        self.assertEqual(len(wishlist_items), 0)

    def test_delete_wishlist(self):
        self.wishlist.delete()
        with self.assertRaises(Wishlists.DoesNotExist):
            Wishlists.objects.get(user=self.user)

    def test_delete_user_with_wishlist(self):

        self.assertIsNotNone(User.objects.get(id=self.user.id))
        self.assertIsNotNone(Wishlists.objects.get(user=self.user))

        self.user.delete()
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.user.id)

        with self.assertRaises(Wishlists.DoesNotExist):
            Wishlists.objects.get(user=self.user)


# Self Note:make test create a user delete the user but delete  whishlist with the user ID

class WishlistViewTest(TestCase):
    # Admin will perform CRUD on all wishlists, whether theirs or not
    # Normal users will perform CRUD on their wishlists only
    # Bad actors will attempt to perform CRUD on other users' wishlists
    used_credentials = {"admin": ['testAdmin', 'ToughPassword123!@#'],
                        "wishlist_owner": ['testNormal', 'ToughPassword'],
                        "other_user": ['testOtherUser', 'ToughPassword']
                        }

    def setUp(self):
        self.client = APIClient()
        User.objects.filter(username__in=['testAdmin', 'testNormal', 'testOtherUser']).delete()

        self.admin = User(
            google_id='test_google_id',
            username=self.used_credentials['admin'][0],
            password=self.used_credentials['admin'][1],
            email='admin@gmail.com',
            roles=['admin']
        )
        self.admin.save()
        self.admin_token = self.client.post('/users/login/', {
            'username': self.admin.username,
            'password': self.used_credentials['admin'][1]
        }).data['access']
        # Note that we need to use the raw password because it's immediately hashed when saved, so I'm storing it in the
        # used_credentials dict

        self.wishlist_owner = User(
            google_id='test_google_id',
            username=self.used_credentials['wishlist_owner'][0],
            password=self.used_credentials['wishlist_owner'][1],
            email='normal@gmail.com',
            roles=['user']
        )
        self.wishlist_owner.save()
        self.wishlist_owner_token = self.client.post('/users/login/', {
            'username': self.wishlist_owner.username,
            'password': self.used_credentials['wishlist_owner'][1]
        }).data['access']

        self.other_user = User(
            google_id='test_google_id',
            username=self.used_credentials['other_user'][0],
            password=self.used_credentials['other_user'][1],
            email='other@gmail.com',
            roles=['user']
        )
        self.other_user.save()
        self.other_user_token = self.client.post('/users/login/', {
            'username': self.other_user.username,
            'password': self.used_credentials['other_user'][1]
        }).data['access']

        Items.objects.filter(name__in=['testitem1', 'testitem2']).delete()
        self.item1 = Items(
            id=ObjectId(),
            name='testitem1',
            price=19.99,
            description='Item 1',
            category='testcategory'
        )
        self.item1.save()
        self.item2 = Items(
            id=ObjectId(),
            name='testitem2',
            price=49.99,
            description='Item 2',
            category='testcategory'
        )
        self.item2.save()

        if Wishlists.objects.filter(name='Halloween').count() > 0:
            Wishlists.objects.get(name='Halloween').delete()

        self.wishlist_template = {
            'name': 'Halloween',
            'user': str(self.wishlist_owner.id),
            'items': [str(self.item1.id)]
        }

    def tearDown(self):
        self.admin.delete()
        self.wishlist_owner.delete()
        self.other_user.delete()
        self.item1.delete()
        self.item2.delete()

    def test_create_wishlist(self):
        response = self.client.post('/wishlists/new', {
            'name': 'Halloween',
            'user': str(self.wishlist_owner.id),
            'items': [str(self.item1.id), str(self.item2.id)]
        }, HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(Wishlists.objects.get(name='Halloween'))

    def test_create_wishlist_for_another_user_as_admin(self):
        # This will create a wishlist for the normal user
        response = self.client.post('/wishlists/new', self.wishlist_template,
                                    HTTP_AUTHORIZATION=f'Bearer {self.admin_token}', format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(Wishlists.objects.get(name='Halloween'))
        self.assertEqual(Wishlists.objects.get(name='Halloween').user, self.wishlist_owner)

    def test_create_wishlist_for_non_existent_user(self):
        # This should fail because the user does not exist
        response = self.client.post('/wishlists/new', {
            'name': 'Halloween',
            'user': str(ObjectId()),
            'items': [str(self.item1.id), str(self.item2.id)]
        }, HTTP_AUTHORIZATION=f'Bearer {self.admin_token}', format='json')

        self.assertEqual(response.status_code, 400)
        self.assertRaises(DoesNotExist, Wishlists.objects.get, name='Halloween')

    def test_create_wishlist_for_another_user_as_non_admin(self):
        # This should fail because normal users can only create wishlists for themselves
        response = self.client.post('/wishlists/new', self.wishlist_template,
                                    HTTP_AUTHORIZATION=f'Bearer {self.other_user_token}', format='json')

        self.assertEqual(response.status_code, 403)
        self.assertRaises(DoesNotExist, Wishlists.objects.get, name='Halloween')

    def test_get_all_wishlists_for_current_user(self):
        response = self.client.get('/wishlists/',
                                   HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 0)

        # Create a wishlist for the normal user
        self.client.post('/wishlists/new', self.wishlist_template,
                         HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        response = self.client.get('/wishlists/',
                                   HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 1)

    def test_get_public_wishlist_by_id_as_wishlist_owner(self):
        # Wishlists are public by default
        self.client.post('/wishlists/new', self.wishlist_template,
                         HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        wishlist_id = Wishlists.objects.get(name='Halloween').id

        response = self.client.get(f'/wishlists/get/{wishlist_id}/',
                                   HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['name'], 'Halloween')

    def test_get_public_wishlist_by_id_as_non_owner(self):
        # Wishlists are public by default, make a new wishlist
        self.client.post('/wishlists/new', self.wishlist_template,
                         HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        wishlist_id = Wishlists.objects.get(name='Halloween').id

        # Attempt to access the public wishlist as a different user
        response = self.client.get(f'/wishlists/get/{wishlist_id}/',
                                   HTTP_AUTHORIZATION=f'Bearer {self.other_user_token}', format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['name'], 'Halloween')

    def test_get_private_wishlist_by_id_as_wishlist_owner(self):
        # Make a new private wishlist
        self.wishlist_template['isPublic'] = False
        self.client.post('/wishlists/new', self.wishlist_template,
                         HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        wishlist_id = Wishlists.objects.get(name='Halloween').id

        response = self.client.get(f'/wishlists/get/{wishlist_id}/',
                                   HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['name'], 'Halloween')

    def test_get_private_wishlist_by_id_as_non_owner(self):
        # Make a new private wishlist
        self.wishlist_template['isPublic'] = False
        self.client.post('/wishlists/new', self.wishlist_template,
                         HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        wishlist_id = Wishlists.objects.get(name='Halloween').id

        # Attempt to access the private wishlist as a different user
        response = self.client.get(f'/wishlists/get/{wishlist_id}/',
                                   HTTP_AUTHORIZATION=f'Bearer {self.other_user_token}', format='json')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['error'], 'You do not have permission to view this wishlist')

    def test_update_wishlist_as_wishlist_owner(self):
        # Make a new wishlist
        self.client.post('/wishlists/new', self.wishlist_template,
                         HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        wishlist_id = Wishlists.objects.get(name='Halloween').id

        # Update the wishlist
        response = self.client.patch('/wishlists/update',
                                     {'wishlist_id': str(wishlist_id), 'name': 'Christmas'},
                                     HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Wishlists.objects.get(id=wishlist_id).name, 'Christmas')

    def test_update_wishlist_as_admin(self):
        # Make a new wishlist
        self.client.post('/wishlists/new', self.wishlist_template,
                         HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        wishlist_id = Wishlists.objects.get(name='Halloween').id

        # Update the wishlist as an admin (not the owner)
        response = self.client.patch('/wishlists/update',
                                     {'wishlist_id': str(wishlist_id), 'name': 'Christmas'},
                                     HTTP_AUTHORIZATION=f'Bearer {self.admin_token}', format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Wishlists.objects.get(id=wishlist_id).name, 'Christmas')

    def test_update_wishlist_as_non_owner(self):
        # Make a new wishlist
        self.client.post('/wishlists/new', self.wishlist_template,
                         HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        wishlist_id = Wishlists.objects.get(name='Halloween').id

        # Update the wishlist as a different user
        response = self.client.patch('/wishlists/update',
                                     {'wishlist_id': str(wishlist_id), 'name': 'Christmas'},
                                     HTTP_AUTHORIZATION=f'Bearer {self.other_user_token}', format='json')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['error'], 'You do not have permission to update this wishlist')

    def test_delete_wishlist_as_wishlist_owner(self):
        # Make a new wishlist
        self.client.post('/wishlists/new', self.wishlist_template,
                         HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        wishlist_id = Wishlists.objects.get(name='Halloween').id

        # Delete the wishlist
        response = self.client.delete('/wishlists/delete',
                                      {'wishlist_id': str(wishlist_id)},
                                      HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        self.assertEqual(response.status_code, 200)
        self.assertRaises(DoesNotExist, Wishlists.objects.get, id=wishlist_id)

    def test_delete_wishlist_as_admin(self):
        # Make a new wishlist
        self.client.post('/wishlists/new', self.wishlist_template,
                         HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        wishlist_id = Wishlists.objects.get(name='Halloween').id

        # Delete the wishlist as an admin
        response = self.client.delete('/wishlists/delete',
                                      {'wishlist_id': str(wishlist_id)},
                                      HTTP_AUTHORIZATION=f'Bearer {self.admin_token}', format='json')

        self.assertEqual(response.status_code, 200)
        self.assertRaises(DoesNotExist, Wishlists.objects.get, id=wishlist_id)

    def test_delete_wishlist_as_non_owner(self):
        # Make a new wishlist
        self.client.post('/wishlists/new', self.wishlist_template,
                         HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        wishlist_id = Wishlists.objects.get(name='Halloween').id

        # Delete the wishlist as a different user
        response = self.client.delete('/wishlists/delete',
                                      {'wishlist_id': str(wishlist_id)},
                                      HTTP_AUTHORIZATION=f'Bearer {self.other_user_token}', format='json')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['error'], 'You do not have permission to delete this wishlist')

    def test_add_item_to_wishlist_as_owner(self):
        # Make a new wishlist
        self.client.post('/wishlists/new', self.wishlist_template,
                         HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        wishlist_id = Wishlists.objects.get(name='Halloween').id

        # Add an item to the wishlist
        response = self.client.patch('/wishlists/add-item',
                                     {'wishlist_id': str(wishlist_id), 'item_id': str(self.item2.id)},
                                     HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        self.assertEqual(response.status_code, 200)
        for item in Wishlists.objects.get(id=wishlist_id).items:
            self.assertIn(item, [self.item1, self.item2])

    def test_add_item_to_wishlist_as_admin(self):
        # Make a new wishlist
        self.client.post('/wishlists/new', self.wishlist_template,
                         HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        wishlist_id = Wishlists.objects.get(name='Halloween').id

        # Add an item to the wishlist as an admin
        response = self.client.patch('/wishlists/add-item',
                                     {'wishlist_id': str(wishlist_id), 'item_id': str(self.item2.id)},
                                     HTTP_AUTHORIZATION=f'Bearer {self.admin_token}', format='json')

        self.assertEqual(response.status_code, 200)
        for item in Wishlists.objects.get(id=wishlist_id).items:
            self.assertIn(item, [self.item1, self.item2])

    def test_add_item_to_wishlist_as_non_owner(self):
        # Make a new wishlist
        self.client.post('/wishlists/new', self.wishlist_template,
                         HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        wishlist_id = Wishlists.objects.get(name='Halloween').id

        # Add an item to the wishlist as a different user
        response = self.client.patch('/wishlists/add-item',
                                     {'wishlist_id': str(wishlist_id), 'item_id': str(self.item2.id)},
                                     HTTP_AUTHORIZATION=f'Bearer {self.other_user_token}', format='json')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['error'], 'You do not have permission to update this wishlist')

    def test_add_non_existent_item_to_wishlist(self):
        # Make a new wishlist
        self.client.post('/wishlists/new', self.wishlist_template,
                         HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        wishlist_id = Wishlists.objects.get(name='Halloween').id

        # Add a non-existent item to the wishlist
        response = self.client.patch('/wishlists/add-item',
                                     {'wishlist_id': str(wishlist_id), 'item_id': str(ObjectId())},
                                     HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['error'], 'Item does not exist')

    def test_add_item_to_non_existent_wishlist(self):
        # Add an item to a non-existent wishlist
        response = self.client.patch('/wishlists/add-item',
                                     {'wishlist_id': str(ObjectId()), 'item_id': str(self.item1.id)},
                                     HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['error'], 'Wishlist does not exist')


    def test_add_duplicate_item_to_remove_from_wishlist(self):
        # Make a new wishlist
        self.client.post('/wishlists/new', self.wishlist_template,
                         HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        wishlist_id = Wishlists.objects.get(name='Halloween').id

        # Add an item to the wishlist (note that because the item is already in the wishlist, it should be removed)
        response = self.client.patch('/wishlists/add-item',
                                     {'wishlist_id': str(wishlist_id), 'item_id': str(self.item1.id)},
                                     HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        self.assertEqual(response.status_code, 200)
        # The item should have been removed
        self.assertEqual(len(Wishlists.objects.get(id=wishlist_id).items), 0)

        # Add the same item again
        response = self.client.patch('/wishlists/add-item',
                                     {'wishlist_id': str(wishlist_id), 'item_id': str(self.item1.id)},
                                     HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        self.assertEqual(response.status_code, 200)
        # The item should have been added back
        self.assertEqual(Wishlists.objects.get(id=wishlist_id).items.count(self.item1), 1)

    def test_get_all_items_for_current_user(self):
        # Make a new wishlist
        self.client.post('/wishlists/new', self.wishlist_template,
                         HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        # Get all items for the current user
        response = self.client.get('/wishlists/items',
                                   HTTP_AUTHORIZATION=f'Bearer {self.wishlist_owner_token}', format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.item1.name, [item['name'] for item in response.data['data']])

