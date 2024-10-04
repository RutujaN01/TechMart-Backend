from bson import ObjectId
from django.test import TestCase

from decimal import Decimal

from items.models import Items
from users.models import User
from wishlists.models import Wishlists


# https://docs.mongoengine.org/guide/querying.html Object


class WishlistModelTest(TestCase):
    def setUp(self):
        if User.objects.filter(username='testuser1').count() > 0:
            User.objects.get(username='testuser1').delete()
        self.user = User.objects.create(
            google_id='test_google_id',
            username='testuser1',
            password='ToughPassword123!@#',
            email='testuser@example.com',
            roles=['user']
        )
        self.item1 = Items.objects.create(
            id=ObjectId(),
            name='testitem1',
            price= 19.99,
            description='Item 1',
            category='testcategory'
        )
        self.item2 = Items.objects.create(
            id=ObjectId(),
            name='testitem2',
            price= 49.99,
            description='Item 2',
            category='testcategory'
        )

        if Wishlists.objects.filter(name = 'Holloween').count() > 0:
            Wishlists.objects.get(name = 'Holloween').delete()
        self.wishlist_id = ObjectId()
        self.wishlist = Wishlists(
            id = self.wishlist_id,
            name = 'Holloween',
            userID = self.user,
            item_ids=[self.item1, self.item2]
        )
        self.wishlist.save()

    
    def tearDown(self):
        self.wishlist.delete()
        self.item1.delete()
        self.item2.delete()
        self.user.delete()


    def test_add_items_to_wishlist(self):
        new_item = Items.objects.create(
            id=ObjectId(),
            name='testitem3',
            price=119.99,
            description='Item 3',
            category='testcategory'
        )
        self.wishlist.item_ids.append(new_item)
        self.wishlist.save()

        self.assertIn(new_item, self.wishlist.item_ids)

        new_item.delete()
    


    def test_remove_items_from_wishlist(self):
        self.wishlist.item_ids.remove(self.item1)
        self.wishlist.save()
        self.assertNotIn(self.item1, self.wishlist.item_ids)

    def test_retrieve_wishlist_items(self):
        wishlist_items = self.wishlist.item_ids
        self.assertEqual(len(wishlist_items), 2)#this makes sure that the 2 items in there
        self.assertIn(self.item1, wishlist_items)
        self.assertIn(self.item2, wishlist_items)

    def test_clear_wishlist(self):
        self.wishlist.item_ids = []
        self.wishlist.save()
        wishlist_items = self.wishlist.item_ids
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