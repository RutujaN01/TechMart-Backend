from bson import ObjectId
from django.test import TestCase


from items.models import Items


class ItemModelTest(TestCase):

    def setUp(self):
        if Items.objects.filter(name='testitem').count() > 0:
            Items.objects.get(name='testitem').delete()
        self.item_id = ObjectId()
        self.item = Item(
            id=self.item_id,
            name='testitem',
            price=9.99,
            description='This is test for very important testing that is required',
            category='testcategory'
        )
        self.item.save()

    def tearDown(self):
        self.item.delete()

    def test_create_item(self):
        if Item.objects.filter(name='galaxyPhone').count() > 0:
            Item.objects.get(name='galaxyPhone').delete()
        item = Item(
            id=ObjectId(),
            # name='newitem',galaxyPhone
            price=999.99,
            description='Opposite of Apple phone',
            category='Samsung'
        )
        item.save()

        found_item = Item.objects.get(id=item.id)

        self.assertEqual(found_item.name, 'galaxyPhone')
        self.assertEqual(found_item.price, 999.99)
        self.assertEqual(found_item.description, 'Opposite of Apple phone')
        self.assertEqual(found_item.category, 'Samsung')

        item.delete()

    def test_create_item_with_invalid_price(self):
        with self.assertRaises(Exception):
            item = Item(
                id=ObjectId(),
                name='Smart Fridge',
                price=-100.99, 
                description='Invalid price item',
                category='Fridge'
            )
            item.save()

    def test_retrieve_item(self):
        item = Item.objects.get(id=self.item_id)
        self.assertEqual(item.name, 'testitem')
        self.assertEqual(item.price, 9.99)
        self.assertEqual(item.description, 'This is test for very important testing that is required')
        self.assertEqual(item.category, 'testcategory')

    def test_update_item_name(self):
        item = Item.objects.get(id=self.item_id)
        item.name = 'updateditem'
        item.save()
        updated_item = Item.objects.get(id=self.item_id)
        self.assertEqual(updated_item.name, 'updateditem')

    def test_update_item_price(self):
        item = Item.objects.get(id=self.item_id)
        item.price = 14.99
        item.save()
        updated_item = Item.objects.get(id=self.item_id)
        self.assertEqual(updated_item.price, 14.99)

    def test_delete_item(self):
        item = Item.objects.get(id=self.item_id)
        item.delete()
        with self.assertRaises(Item.DoesNotExist):
            Item.objects.get(id=self.item_id)