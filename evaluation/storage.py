import logging

import numpy as np
import pandas as pd
from davisinteractive.dataset import Davis
from davisinteractive.storage import AbstractStorage
from django.utils import timezone

from .models import AnnotatedFrame, ResultEntry, Session

logger = logging.getLogger(__name__)


class DBStorage(AbstractStorage):
    """ Class to store all evaluation results on a Django DB.
    """

    @staticmethod
    def store_interactions_results(user_id, session_id, sequence, scribble_idx,
                                   interaction, timing, objects_idx, frames,
                                   jaccard, contour):
        """ The information of a single interaction is given and stored.

        # Arguments
            user_id: String. User identifier. As it is in local, this value is
                ignored.
            session_id: String. Session identifier.
            sequence: String. Sequence name.
            scribble_idx: Integer. Scribble index of the sample.
            interaction: Integer. Interaction number.
            timing: Float. Timing in seconds that lasted the interaction.
            objects_idx: List of Integers. List of the objects identifiers that
                match with the jaccard metric.
            frames: List of Integers: List of frame index matching with the
                jaccard metric.
            jaccard: List of Floats: List of jaccard metric.
            contour: List of Floats: List of contour metric.
        """
        session = Session.get_or_create_session(user_id, session_id)

        if ResultEntry.objects.filter(
                session=session,
                sequence=sequence,
                scribble_idx=scribble_idx,
                interaction=interaction).count():
            raise RuntimeError(('For {} and scribble {} already exist a '
                                'result for interaction {}').format(
                                    sequence, scribble_idx, interaction))
        if interaction > 1 and ResultEntry.objects.filter(
                session=session,
                sequence=sequence,
                scribble_idx=scribble_idx,
                interaction=interaction - 1).count() == 0:
            raise RuntimeError(('For {} and scribble {} does not exist a '
                                'result for previous interaction {}').format(
                                    sequence, scribble_idx, interaction - 1))

        # Log information about previous interaction timestamps and current
        # to perform statistics and decide if the some storage of results
        # may be ignored due to fraud
        previous_entries = ResultEntry.objects.filter(session=session)
        if previous_entries.count() > 0:
            last = previous_entries.latest('timestamp')
            prev_timestamp = last.timestamp
            curr_timestamp = timezone.now()
            timedelta = (curr_timestamp - prev_timestamp).total_seconds()
            logger.info(
                f'[Session: {session_id[:8]}] '
                f'Entries timedelta: {timedelta:.3f}s and timing: {timing:.3f}s'
            )
            time_diference = timedelta - timing
            logger.info(f'[Session: {session_id[:8]}] '
                        f'Time diference: {time_diference:.3f}s')
            if interaction > 1 and last.sequence != sequence:
                logger.warning(
                    f'Previous entry (in time) do not match the previous '
                    f'interaction for sequence {sequence}\n'
                    f'Session ID: {session_id}')

        j_and_f = [.5 * j + .5 * f for j, f in zip(jaccard, contour)]

        results = [
            ResultEntry(
                session=session,
                sequence=sequence,
                scribble_idx=scribble_idx,
                interaction=interaction,
                timing=timing,
                object_id=o_id,
                frame=f,
                jaccard=j,
                contour=c,
                j_and_f=j_c) for o_id, f, j, c, j_c in zip(
                    objects_idx, frames, jaccard, contour, j_and_f)
        ]
        ResultEntry.objects.bulk_create(results)
        num_new_entries = len(results)
        session.update_entries(num_new_entries)

    @staticmethod
    def get_report(user_id=None, session_id=None):
        """ Return current report.

        # Arguments
            session_id: String. Session identifier

        # Returns
            Pandas DataFrame. Report in the form of the DataFrame.
        """
        query = ResultEntry.objects.filter(
            session__session_id=session_id).values(*DBStorage.COLUMNS)
        df = pd.DataFrame.from_records(query)
        df = df.sort_index()
        return df

    @staticmethod
    def get_annotated_frames(session_id, sequence, scribble_idx):
        """Get the previous annotated frames for the given iteration.

        # Arguments
            session_id: String. Ignored.
            sequence: String. Sequence name.
            scribble_idx: Integer. Scribble index of the sample.

        # Returns
            List of Integers. List of the frames that have been previously
                annotated in the current iteration.
        """
        session = Session.objects.get(session_id=session_id)
        prev_frames = AnnotatedFrame.objects.filter(
            session=session, sequence=sequence,
            scribble_idx=scribble_idx).values('frame')
        prev_frames = [f['frame'] for f in prev_frames]

        if len(prev_frames) == Davis.dataset[sequence]['num_frames']:
            return tuple()

        return tuple(prev_frames)

    @staticmethod
    def store_annotated_frame(session_id, sequence, scribble_idx,
                              annotated_frame, override):
        """ Get and store the frame to generate the scribble.

        This function will check all the previous generated scribbles frames
        and return the frame with lower metric that the robot hasn't generated
        a scribble.

        # Arguments
            session_id: String. Ignored.
            sequence: String. Sequence name.
            scribble_idx: Integer. Scribble index of the sample.
            annotated_frame: Integer. Index of the frame of the next scribble
                iteration.
            override: Boolean. Whether or not the annotated frame was override
                by the user or not.
        """
        session = Session.objects.get(session_id=session_id)
        AnnotatedFrame.objects.create(
            session=session,
            sequence=sequence,
            scribble_idx=scribble_idx,
            frame=annotated_frame,
            override=override)
