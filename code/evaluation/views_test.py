from django.test import TestCase


class HealthViewTestCase(TestCase):

    def test_health(self):
        response = self.client.get('/api/healthcheck')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'health': 'OK',
            'name': 'DAVIS Interactive Server',
            'magic': 23
        })
