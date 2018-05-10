import logging

import pandas as pd
from django.utils import timezone

from davisinteractive.storage import AbstractStorage

from .models import ResultEntry, Session

logger = logging.getLogger(__name__)


class DBStorage(AbstractStorage):
    """ Class to store all evaluation results on a Django DB.
    """

    @staticmethod
    def store_interactions_results(user_id, session_id, sequence, scribble_idx,
                                   interaction, timing, objects_idx, frames,
                                   jaccard):
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
                f'Entries timedelta: {timedelta:.3f}s and timing: {timing:.3f}s'
            )
            time_diference = timedelta - timing
            logger.info(f'Time diference: {time_diference:.3f}s')
            if interaction > 1 and last.sequence != sequence:
                logger.warning(
                    f'Previous entry (in time) do not match the previous '
                    f'interaction for sequence {sequence}\n'
                    f'Session ID: {session_id}')

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
            ) for o_id, f, j in zip(objects_idx, frames, jaccard)
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
        return df
