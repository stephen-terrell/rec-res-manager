import os
import pytest
from unittest.mock import patch

from src.event.api.alert.v1.delete import DeleteAlert


class TestDelete:

    @pytest.fixture
    def alert_id_1(self):
        return 'alert111111'

    @pytest.fixture
    def user_id_1(self):
        return 'user1111111'

    @pytest.fixture
    def make_event(self):
        def _make_event(user_id, alert_id):
            return {
                'headers': {'x-rec-res-user-id': user_id},
                'pathParameters': {'alertId': alert_id}
            }

        return _make_event

    @pytest.fixture
    def send_api_command_mock(self):
        with patch('src.event.api.alert.v1.delete.SqsProxy') as sqs_proxy:
            yield sqs_proxy.return_value.send_api_command

    def test_enact(self, user_id_1, alert_id_1, make_event, send_api_command_mock):
        under_test = DeleteAlert(make_event(user_id_1, alert_id_1))

        result = under_test.enact()

        assert result is None
        send_api_command_mock.assert_called_once_with({
            'commandName': 'DELETE_ALERT',
            'data': {
                'userId': user_id_1,
                'alertId': alert_id_1
            }
        })
