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

    @pytest.fixture
    def receipt_handles(self):
        return [
            'handle1234',
            'handleinyourhand',
        ]

    def test_send_api_command(self, boto3_mock, message):
        under_test = SqsProxy()

        under_test.send_api_command(message)

        boto3_mock.client.return_value.send_message.assert_called_once_with(
            QueueUrl='some-url',
            MessageBody=json.dumps(message),
            MessageGroupId='rec-res-api-commands',
        )

    def test_delete_api_command_messages(self, boto3_mock, receipt_handles):
        under_test = SqsProxy()

        under_test.delete_api_command_messages(receipt_handles)

        boto3_mock.client.return_value.delete_message_batch.assert_called_once_with(
            QueueUrl='some-url',
            Entries=[{'Id': str(index), 'ReceiptHandle': handle}
                     for index, handle in enumerate(receipt_handles)],
        )
