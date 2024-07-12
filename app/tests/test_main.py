import pytest
from fastapi.testclient import TestClient
from ..main import app


class TestMain():
    def setup_method(self, translation_task_db_mock):
        self.__client = TestClient(app)
        self.__db = translation_task_db_mock

    def test_index(self):
        response = self.__client.get('/')
        assert response.status_code == 200

    def teardown_method(self):
        del self.__db
        del self.__client
