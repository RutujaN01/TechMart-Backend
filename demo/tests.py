from django.test import TestCase

# Create your tests here.
class DemoTestCase(TestCase):
    def test_demo(self):
        self.assertEqual(1, 1)

    def test_demo_hello_world(self):
        response = self.client.get('/demo/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Hello, world!'})