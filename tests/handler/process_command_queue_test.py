import pytest
from unittest.mock import patch

from src.handler.process_command_queue import handler


class TestProcessCommandQueue:
    @pytest.fixture
    def process_event_mock(self):
        with patch("src.handler.process_command_queue.ProcessCommandQueueEvent") as process_event:
            yield process_event

    @pytest.fixture
    def event(self):
        return {"an": "event"}

    @pytest.fixture
    def context(self):
        return "asdf"

    def test_handle(self, process_event_mock, event, context):
        handler(event, context)

        process_event_mock.assert_called_once_with(event, context)

        process_event_mock.return_value.handle.assert_called_once()
