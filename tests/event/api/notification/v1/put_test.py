import pytest
from unittest.mock import patch

from src.event.api.notification.v1.put import PutNotification


class TestPut:
    @pytest.fixture
    def notification_id_1(self):
        return "notify222222"

    @pytest.fixture
    def user_id_1(self):
        return "user1111111"

    @pytest.fixture
    def endpoint(self):
        return "test@test.com"

    @pytest.fixture
    def make_event(self):
        def _make_event(user_id, endpoint):
            return {
                "headers": {"x-rec-res-user-id": user_id},
                "body": {
                    "protocol": "email",
                    "endpoint": endpoint,
                },
            }

        return _make_event

    @pytest.fixture
    def send_api_command_mock(self):
        with patch("src.event.api.notification.v1.put.SqsProxy") as sqs_proxy:
            yield sqs_proxy.return_value.send_api_command

    @pytest.fixture
    def uuid_mock(self, notification_id_1):
        with patch("src.event.api.notification.v1.put.uuid4") as uuid4:
            uuid4.return_value = notification_id_1
            yield uuid4

    def test_enact(self, user_id_1, notification_id_1, endpoint, make_event, send_api_command_mock, uuid_mock):
        under_test = PutNotification(make_event(user_id_1, endpoint))

        result = under_test.enact()

        data = {"userId": user_id_1, "notificationId": notification_id_1, "protocol": "email", "endpoint": endpoint}

        assert result == data
        send_api_command_mock.assert_called_once_with({"commandName": "CREATE_NOTIFICATION", "data": data})
