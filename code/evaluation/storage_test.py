from django.test import TestCase

from evaluation.models import ResultEntry, Session
from evaluation.storage import DBStorage
from registration.models import Participant


class DBStorageTestCase(TestCase):

    def setUp(self):
        self.participant = Participant.objects.create(
            user_id='1234',
            name='John Doe',
            organization='Company SA',
            email='john@example')

    def test_add(self):
        self.assertEqual(
            Session.objects.filter(session_id='session1234').count(), 0)
        DBStorage.store_interactions_results(
            user_id='1234',
            session_id='session1234',
            sequence='aerobatics',
            scribble_idx=1,
            interaction=1,
            timing=2.,
            objects_idx=[1, 2, 1, 2],
            frames=[1, 1, 2, 2],
            jaccard=[.1, .2, .3, .4])
        self.assertEqual(
            Session.objects.filter(session_id='session1234').count(), 1)
        self.assertEqual(
            ResultEntry.objects.filter(
                session__session_id='session1234').count(),
            4)

        with self.assertRaises(RuntimeError):
            DBStorage.store_interactions_results(
                user_id='1234',
                session_id='session1234',
                sequence='aerobatics',
                scribble_idx=1,
                interaction=1,
                timing=2.,
                objects_idx=[1, 2, 1, 2],
                frames=[1, 1, 2, 2],
                jaccard=[.1, .2, .3, .4])

    def test_no_previous(self):
        self.assertEqual(
            Session.objects.filter(session_id='session1234').count(), 0)
        with self.assertRaises(RuntimeError):
            DBStorage.store_interactions_results(
                user_id='1234',
                session_id='session1234',
                sequence='aerobatics',
                scribble_idx=1,
                interaction=2,
                timing=2.,
                objects_idx=[1, 2, 1, 2],
                frames=[1, 1, 2, 2],
                jaccard=[.1, .2, .3, .4])
        self.assertEqual(
            Session.objects.filter(session_id='session1234').count(), 1)
        self.assertEqual(
            ResultEntry.objects.filter(
                session__session_id='session1234').count(),
            0)
