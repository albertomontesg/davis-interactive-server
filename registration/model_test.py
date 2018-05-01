from django.test import TestCase

from registration.models import Participant


class ParticipantTestCase(TestCase):

    def setUp(self):
        participant = Participant(
            name='Test name',
            organization='Test Organization',
            email='name@example.com')
        participant.generate_key()
        participant.save()

    def test_str(self):
        p = Participant.objects.get(email='name@example.com')
        self.assertEqual(str(p), 'Test name (Test Organization)')
