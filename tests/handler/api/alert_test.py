import pytest
from unittest.mock import patch

from src.handler.api.alert import handler


class TestAlert:
    @pytest.fixture
    def handle_result(self):
        return "the result"

    @pytest.fixture
    def alert_event_mock(self, handle_result):
        with patch("src.handler.api.alert.AlertEvent") as alert_event:
            alert_event.return_value.handle.return_value = handle_result
            yield alert_event

    @pytest.fixture
    def event(self):
        return {"an": "event"}

    @pytest.fixture
    def context(self):
        return "asdf"

    def test_handle(self, alert_event_mock, handle_result, event, context):
        result = handler(event, context)

        alert_event_mock.assert_called_once_with(event=event, context=context)

        alert_event_mock.return_value.handle.assert_called_once()

        assert result == handle_result
