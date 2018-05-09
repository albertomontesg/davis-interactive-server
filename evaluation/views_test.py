import json
from unittest.mock import MagicMock, patch

from django.test import TestCase

from davisinteractive.dataset import Davis
from davisinteractive.evaluation import EvaluationService
from evaluation.models import ResultEntry, Session
from registration.models import Participant


class HealthViewTestCase(TestCase):

    def test_health(self):
        response = self.client.get('/api/healthcheck')
        self.assertEqual(response.status_code, 200)
        r_json = response.json()
        self.assertEqual(r_json.get('health'), 'OK')
        self.assertEqual(r_json.get('name'), 'DAVIS Interactive Server')
        self.assertEqual(r_json.get('magic'), 23)


class GetDatasetDataTestCase(TestCase):

    @patch.object(
        EvaluationService,
        'get_samples',
        return_value=[('test', 1), ('test', 2)])
    def test_get_samples(self, mock_service):

        self.assertEqual(mock_service.call_count, 0)

        response = self.client.get('/api/dataset/samples')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_service.call_count, 1)

        self.assertEqual(response.json(), [['test', 1], ['test', 2]])

    @patch.object(
        EvaluationService,
        'get_samples',
        side_effect=FileNotFoundError('test exception'))
    def test_get_samples_invalid(self, mock_service):

        self.assertEqual(mock_service.call_count, 0)

        response = self.client.get('/api/dataset/samples')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(mock_service.call_count, 1)

        self.assertEqual(response.json(), {
            'error': 'FileNotFoundError',
            'message': ['test exception']
        })

    @patch.object(
        EvaluationService,
        'get_scribble',
        return_value={
            'sequence': 'aerobatics',
            'scribbles': [[], []]
        })
    def test_get_scribble(self, mock_service):

        self.assertEqual(mock_service.call_count, 0)

        response = self.client.get('/api/dataset/scribbles/aerobatics/01')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_service.call_count, 1)

        self.assertEqual(response.json(), {
            'sequence': 'aerobatics',
            'scribbles': [[], []]
        })

    def test_get_scribble_bad(self):
        r = self.client.get('/api/dataset/scribbles/bear/3')
        self.assertEqual(r.status_code, 400)

        r = self.client.get('/api/dataset/scribbles/aerobatics/200')
        self.assertEqual(r.status_code, 400)


class EvaluationTestCase(TestCase):

    def setUp(self):
        self.body = {
            "sequence": "orchid",
            "scribble_idx": 3,
            "pred_masks": {
                "size": [57, 480, 854],
                "frames": [[{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }], [{
                    "object_id":
                    1,
                    "counts":
                    "b_g0T3l;00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000^nY:"
                }]]
            },
            "timing": 0.055110931396484375,
            "interaction": 1
        }
        self.data = json.dumps(self.body)
        participant = Participant.objects.create(
            user_id='1234',
            name='John Doe',
            organization='Company SA',
            email='john@example')
        self.participant = participant

    def test_post_no_participant(self):
        headers = {
            'HTTP_USER_KEY': 'incorrect',
            'HTTP_SESSION_KEY': 'session1234'
        }
        r = self.client.post(
            '/api/evaluation/interaction',
            data=self.data,
            content_type='application/json',
            **headers)

        self.assertEqual(r.status_code, 401)

    @patch.object(
        EvaluationService,
        'post_predicted_masks',
        return_value={
            'sequence': 'orchid',
            'scribbles': [[], []]
        })
    def test_post_participant(self, mock_service):
        self.assertEqual(mock_service.call_count, 0)
        self.assertEqual(Session.objects.count(), 0)
        headers = {'HTTP_USER_KEY': '1234', 'HTTP_SESSION_KEY': 'session1234'}
        r = self.client.post(
            '/api/evaluation/interaction',
            data=self.data,
            content_type='application/json',
            **headers)
        self.assertEqual(mock_service.call_count, 1)

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['sequence'], 'orchid')


class ReportTestCase(TestCase):

    def setUp(self):
        participant = Participant.objects.create(
            user_id='1234',
            name='John Doe',
            organization='Company SA',
            email='john@example')
        self.participant = participant
        session = Session.objects.create(
            session_id='session1234', participant=participant)
        ResultEntry.objects.create(
            session=session,
            sequence='orchid',
            scribble_idx=1,
            interaction=1,
            object_id=1,
            frame=1,
            jaccard=.1,
            timing=1.)
        ResultEntry.objects.create(
            session=session,
            sequence='orchid',
            scribble_idx=1,
            interaction=1,
            object_id=1,
            frame=2,
            jaccard=.15,
            timing=1.)
        ResultEntry.objects.create(
            session=session,
            sequence='orchid',
            scribble_idx=1,
            interaction=1,
            object_id=2,
            frame=1,
            jaccard=.3,
            timing=1.)
        ResultEntry.objects.create(
            session=session,
            sequence='orchid',
            scribble_idx=1,
            interaction=1,
            object_id=2,
            frame=1,
            jaccard=.4,
            timing=1.)

    def test_no_participant(self):
        headers = {
            'HTTP_USER_KEY': 'incorrect',
            'HTTP_SESSION_KEY': 'session1234'
        }
        r = self.client.get(
            '/api/evaluation/report',
            content_type='application/json',
            **headers)

        self.assertEqual(r.status_code, 401)

    def test_participant(self):
        headers = {'HTTP_USER_KEY': '1234', 'HTTP_SESSION_KEY': 'session1234'}
        r = self.client.get(
            '/api/evaluation/report',
            content_type='application/json',
            **headers)

        self.assertEqual(r.status_code, 200)
        self.assertEqual(
            r.json(), {
                'sequence': {
                    '0': 'orchid',
                    '1': 'orchid'
                },
                'session_id': {
                    '0': 'session1234',
                    '1': 'session1234'
                },
                'scribble_idx': {
                    '0': 1,
                    '1': 1
                },
                'interaction': {
                    '0': 1,
                    '1': 1
                },
                'object_id': {
                    '0': 1,
                    '1': 2
                },
                'timing': {
                    '0': 1.,
                    '1': 1.
                },
                'jaccard': {
                    '0': .125,
                    '1': .35
                }
            })
