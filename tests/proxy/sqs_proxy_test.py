import json
import os
import pytest
from unittest.mock import patch

from src.proxy.sqs_proxy import SqsProxy


@patch.dict(os.environ, {'API_COMMAND_QUEUE_URL': 'some-url'})
class TestSqsProxy:

    @pytest.fixture
    def boto3_mock(self):
        with patch('src.proxy.sqs_proxy.boto3') as boto3_mock:
            yield boto3_mock

    @pytest.fixture
    def message(self):
        return {
            'here': 'is a message'
        }

    def test_init(self, boto3_mock):
        under_test = SqsProxy()

        boto3_mock.resource.return_value.Queue.assert_called_once_with('some-url')

    def test_send_api_command(self, boto3_mock, message):
        under_test = SqsProxy()

        under_test.send_api_command(message)

        boto3_mock.resource.return_value.Queue.return_value.send_message.assert_called_once_with(
            MessageBody=json.dumps(message)
        )
