from unittest import mock

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

    @mock.patch('registration.models.send_message')
    def test_send_email(self, mock_email):
        self.assertEqual(mock_email.call_count, 0)
        self.participant.email_participant('Subject Test',
                                           'This is the message')
        self.assertEqual(mock_email.call_count, 1)
        print(mock_email.call_args)
        _, to, subject, message = mock_email.call_args[0]
        self.assertEqual(subject, 'Subject Test')
        self.assertEqual(message, 'This is the message')
        self.assertEqual(to, self.participant.email)


class RegistrationFormTestCase(TestCase):

    def test_valid(self):
        form_data = {
            'name': 'John Doe',
            'organization': 'Company SA',
            'country': 'CH',
            'email': 'john@example.com'
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_one(self):
        form_data = {
            'name': 'John Doe',
            'organization': 'Company SA',
            'country': 'CH',
            'email': 'johnexample.com'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_two(self):
        form_data = {
            'name': 'John Doe',
            'organization': 'C',
            'country': 'CH',
            'email': 'john@example.com'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_three(self):
        form_data = {
            'name': 'John Doe',
            'organization': '',
            'country': 'CH',
            'email': 'john@example.com'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_four(self):
        form_data = {
            'name': 'JD',
            'organization': 'Company',
            'country': 'CH',
            'email': 'john@example.com'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_five(self):
        form_data = {
            'name': '',
            'organization': 'Company',
            'country': 'CH',
            'email': 'john@example.com'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_six(self):
        form_data = {
            'name': 'John Doe',
            'organization': 'Company SA',
            'country': 'XX',
            'email': 'john@example.com'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_seven(self):
        form_data = {'name': '', 'organization': '', 'country': '', 'email': ''}
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
