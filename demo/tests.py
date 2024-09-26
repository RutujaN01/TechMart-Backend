from django.test import TestCase

# Create your tests here.
class DemoTestCase(TestCase):
    def test_demo(self):
        self.assertEqual(1, 1)

    def test_demo_hello_world(self):
        response = self.client.get('/demo/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Hello, world!'})

    def test_demo_hello_user_with_name(self):
        response = self.client.get('/demo/hello/John/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Hello, John!')

    def test_demo_hello_user_with_name_invalid(self):
        response = self.client.get('/demo/hello/')
        self.assertEqual(response.status_code, 404)