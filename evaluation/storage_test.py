import random
from itertools import product

import numpy as np
from davisinteractive.dataset import Davis
from django.conf import settings
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
            jaccard=[.1, .2, .3, .4],
            contour=[.1, .2, .3, .4])
        self.assertEqual(
            Session.objects.filter(session_id='session1234').count(), 1)
        self.assertEqual(
            ResultEntry.objects.filter(
                session__session_id='session1234').count(), 4)

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
                jaccard=[.1, .2, .3, .4],
                contour=[.1, .2, .3, .4])

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
                jaccard=[.1, .2, .3, .4],
                contour=[.1, .2, .3, .4])
        self.assertEqual(
            Session.objects.filter(session_id='session1234').count(), 1)
        self.assertEqual(
            ResultEntry.objects.filter(
                session__session_id='session1234').count(), 0)

    def test_complete_session(self):
        self.assertEqual(
            Session.objects.filter(session_id='session1234').count(), 0)

        subset = settings.EVALUATION_SUBSET
        num_interactions = settings.EVALUATION_MAX_INTERACTIONS
        sequences = Davis.sets[subset]

        Session.get_or_create_session(self.participant.user_id, 'session1234')

        for seq in sequences:
            num_frames = Davis.dataset[seq]['num_frames']
            num_objects = Davis.dataset[seq]['num_objects']
            num_scribbles = Davis.dataset[seq]['num_scribbles']

            session = Session.objects.get(session_id='session1234')
            assert not session.completed

            for scribble_idx in range(1, num_scribbles + 1):

                for i in range(num_interactions):
                    it = i + 1

                    objects_idx = [
                        x + 1 for x, _ in product(
                            range(num_objects), range(num_frames))
                    ]
                    frames = [
                        x for _, x in product(
                            range(num_objects), range(num_frames))
                    ]
                    metric = [
                        random.random() for _ in range(num_frames * num_objects)
                    ]

                    DBStorage.store_interactions_results(
                        user_id=self.participant.user_id,
                        session_id='session1234',
                        sequence=seq,
                        scribble_idx=scribble_idx,
                        interaction=it,
                        timing=1.,
                        objects_idx=objects_idx,
                        frames=frames,
                        jaccard=metric,
                        contour=metric)

        headers = {
            'HTTP_USER_KEY': self.participant.user_id,
            'HTTP_SESSION_KEY': 'session1234'
        }
        r = self.client.post(
            '/api/evaluation/finish',
            data={},
            content_type='application/json',
            **headers)
        self.assertEqual(r.status_code, 200)
        session = Session.objects.get(session_id='session1234')
        self.assertTrue(session.completed)

    def test_annotated_frames(self):
        sequence = 'bmx-trees'
        scribble_idx = 1

        session = Session.get_or_create_session(self.participant.user_id,
                                                'session1234')

        storage = DBStorage
        storage.store_annotated_frame(session.session_id, sequence,
                                      scribble_idx, 1, False)
        annotated_frames = storage.get_annotated_frames(session.session_id,
                                                        sequence, scribble_idx)
        self.assertEqual(annotated_frames, (1,))

    def test_annotated_frames_full(self):
        sequence = 'bmx-trees'
        scribble_idx = 1
        nb_frames = 80

        session = Session.get_or_create_session(self.participant.user_id,
                                                'session1234')

        storage = DBStorage
        for i in range(nb_frames):
            storage.store_annotated_frame(session.session_id, sequence,
                                          scribble_idx, i, False)
        annotated_frames = storage.get_annotated_frames(session.session_id,
                                                        sequence, scribble_idx)
        self.assertEqual(annotated_frames, tuple())
