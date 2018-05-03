from django.core import mail
from django.test import TestCase

from registration.models import Participant, RegistrationForm


class ParticipantTestCase(TestCase):

    def setUp(self):
        participant = Participant(
            name='Test name',
            organization='Test Organization',
            email='name@example.com')
        participant.generate_key()
        participant.save()
        self.participant = participant

    def test_str(self):
        p = Participant.objects.get(email='name@example.com')
        self.assertEqual(str(p), 'Test name (Test Organization)')

    def test_send_email(self):
        self.participant.email_participant('Subject Test',
                                           'This is the message')
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.subject, 'Subject Test')
        self.assertEqual(message.body, 'This is the message')
        self.assertEqual(len(message.to), 1)
        self.assertEqual(message.to[0], self.participant.email)


class RegistrationFormTestCase(TestCase):

    def test_valid(self):
        form_data = {
            'name': 'John Doe',
            'organization': 'Company SA',
            'email': 'john@example.com'
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_one(self):
        form_data = {
            'name': 'John Doe',
            'organization': 'Company SA',
            'email': 'johnexample.com'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_two(self):
        form_data = {
            'name': 'John Doe',
            'organization': 'C',
            'email': 'john@example.com'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_three(self):
        form_data = {
            'name': 'John Doe',
            'organization': '',
            'email': 'john@example.com'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_four(self):
        form_data = {
            'name': 'JD',
            'organization': 'Company',
            'email': 'john@example.com'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_five(self):
        form_data = {
            'name': '',
            'organization': 'Company',
            'email': 'john@example.com'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_six(self):
        form_data = {'name': '', 'organization': '', 'email': ''}
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
