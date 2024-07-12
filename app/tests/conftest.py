import pytest
from ..models import Base
from .db_test import db_session
from ..translation import Translation


@pytest.fixture()
def tranlation_task_db_mock():
    return [{
            'id': 6,
            'text': 'Good morning',
            'languages': ['japanese', 'filipino', 'spanish', 'english'],
            'status': 'completed',
            'translation': [
                {'japanese': 'おはよう'},
                {'filipino': 'Magandang umaga'},
                {'spanish': 'Buen día'}
            ]
            }]


@pytest.fixture()
def save_translation():
    args = {
        'text': "Good morning!",
        'languages': ['filipino', 'korean'],
    }
    translator = Translation(db_session, args)
    return translator.save_translation()


def pytest_sessionfinish():
    meta = Base.metadata
    for table in reversed(meta.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()
