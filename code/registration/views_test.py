from django.core import mail
from django.test import TestCase

from registration.models import Participant


class RegistrationViewTestCase(TestCase):

    def test_get_form(self):
        response = self.client.get('/registration/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration.html')

    def test_post_invalid_form(self):
        form_data = {
            'name': 'John Doe',
            'organization': 'Company SA',
            'email': 'johnexample.com'
        }
        response = self.client.post('/registration/', form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration.html')
        self.assertTrue(
            'Enter a valid email address' in response.content.decode())

    def test_registration_workflow(self):
        self.assertEqual(Participant.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

        form_data = {
            'name': 'John Doe',
            'organization': 'Company SA',
            'email': 'john@example.com'
        }
        response = self.client.post('/registration/', form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'success.html')

        self.assertEqual(Participant.objects.count(), 1)
        participant = Participant.objects.get(email='john@example.com')
        self.assertEqual(participant.name, 'John Doe')
        self.assertEqual(participant.organization, 'Company SA')

        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.subject, 'DAVIS Challenge Registration')
        self.assertTrue(participant.name in message.body)
        self.assertTrue(participant.user_id in message.body)

        # Repeat post to test repetition
        response = self.client.post('/registration/', form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration.html')
        self.assertTrue('Participant with this Email already exists' in
                        response.content.decode())
