from bson import ObjectId
from django.test import TestCase

from decimal import Decimal
from items.models import Items


class ItemModelTest(TestCase):

    def setUp(self):
        if Items.objects.filter(name='testitem').count() > 0:
            Items.objects.get(name='testitem').delete()
        self.item_id = ObjectId()
        self.item = Items(
            id=self.item_id,
            name='testitem',
            price=9.99,
            description='This is test for very important testing that is required',
            category='testcategory',
            url='mytestingsite.com'
        )
        self.item.save()

    def tearDown(self):
        self.item.delete()

    def test_create_item(self):
        if Items.objects.filter(name='galaxyPhone').count() > 0:
            Items.objects.get(name='galaxyPhone').delete()
        item = Items(
            id=ObjectId(),
            name='galaxyPhone',
            price=999.99,
            description='Opposite of Apple phone',
            category='Samsung',
            url='phonesite.com'
        )
        item.save()

        found_item = Items.objects.get(id=item.id)

        self.assertEqual(found_item.name, 'galaxyPhone')
        self.assertEqual(found_item.price, Decimal('999.99'))
        self.assertEqual(found_item.description, 'Opposite of Apple phone')
        self.assertEqual(found_item.category, 'Samsung')

        item.delete()

    def test_create_item_with_invalid_price(self):
        with self.assertRaises(Exception):
            item = Items(
                id=ObjectId(),
                name='Smart Fridge',
                price=-100.99, 
                description='Invalid price item',
                category='Fridge',
                url='fridgesite.com'
            )
            item.save()

    def test_retrieve_item(self):
        item = Items.objects.get(id=self.item_id)
        self.assertEqual(item.name, 'testitem')
        self.assertEqual(item.price,  Decimal('9.99'))
        self.assertEqual(item.description, 'This is test for very important testing that is required')
        self.assertEqual(item.category, 'testcategory')

    def test_update_item_name(self):
        item = Items.objects.get(id=self.item_id)
        item.name = 'updateditem'
        item.save()
        updated_item = Items.objects.get(id=self.item_id)
        self.assertEqual(updated_item.name, 'updateditem')

    def test_update_item_price(self):
        item = Items.objects.get(id=self.item_id)
        item.price = 14.99
        item.save()
        updated_item = Items.objects.get(id=self.item_id)
        self.assertEqual(updated_item.price,  Decimal('14.99'))

    def test_delete_item(self):
        item = Items.objects.get(id=self.item_id)
        item.delete()
        with self.assertRaises(Items.DoesNotExist):
            Items.objects.get(id=self.item_id)