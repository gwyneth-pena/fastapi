import json
import pytest
from ..translation import Translation
from .db_test import db_session


class TestTranslation():

    def setup_method(self):
        self.__translator = {}
        self.__task = {}

    def test_save_translation_and_update_after_translating(self, save_translation):

        task = save_translation

        if task:
            self.__task = task
        else:
            self. __task.id = ''

        assert self.__task.id != ''

        self.__args = {
            'task_id': self.__task.id,
            'text': self.__task.text,
            'languages': self.__task.languages
        }
        self.__translator = Translation(db_session, self.__args)

        task = self.__translator.translate(**self.__args)
        self.__task = task

        assert len(self.__task.translation) == 2
        assert self.__task.translation[0].get('filipino') == 'Magandang umaga!'
        assert self.__task.translation[1].get('korean') == '좋은 아침이에요!'

    def test_get_translation(self, save_translation):
        saved_task = save_translation

        self.__translator = Translation(db_session, {'task_id': saved_task.id})

        task = self.__translator.get_translation()
        assert task == saved_task

    def teardown_method(self):
        del self.__translator
        del self.__task
