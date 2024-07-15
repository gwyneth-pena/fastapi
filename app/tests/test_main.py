import pytest
from fastapi.testclient import TestClient

from ..main import app


class TestMain():

    def setup_method(self):
        self.__client = TestClient(app)

    def test_index(self):
        response = self.__client.get('/')
        assert response.status_code == 200

    def test_create_and_get_task(self):
        args = {
            'text': "Good morning!",
            'languages': ['filipino', 'korean'],
        }
        response = self.__client.post('/translate', json=args)
        data = response.json()
        assert data.get('task_id', None) is not None
        assert response.status_code == 200

        response = self.__client.get(f'/translate/{data.get("task_id")}')
        data = response.json()
        assert response.status_code == 200

        assert data.get('status', '') == 'completed'
        assert data.get('translation')[0].get('filipino') == 'Magandang umaga!'
        assert data.get('translation')[1].get('korean') == '좋은 아침이에요!'

    def test_get_translate_not_existing(self):
        response = self.__client.get(f'/translate/hello')
        data = response.json()
        assert response.status_code == 200
        assert data == {}

    def teardown_method(self):
        del self.__client
