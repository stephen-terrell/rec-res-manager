import pytest
from unittest.mock import patch

from src.handler.api.notification.handler import handler


class TestHandler:
    @pytest.fixture
    def handle_result(self):
        return "the result"

    @pytest.fixture
    def notification_event_mock(self, handle_result):
        with patch("src.handler.api.notification.handler.NotificationEvent") as notification_event:
            notification_event.return_value.handle.return_value = handle_result
            yield notification_event

    @pytest.fixture
    def event(self):
        return {"an": "event"}

    @pytest.fixture
    def context(self):
        return "asdf"

    def test_handle(self, notification_event_mock, handle_result, event, context):
        result = handler(event, context)

        notification_event_mock.assert_called_once_with(event, context)

        notification_event_mock.return_value.handle.assert_called_once()

        assert result == handle_result
