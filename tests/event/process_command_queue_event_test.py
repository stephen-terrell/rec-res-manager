import json
import pytest
from unittest.mock import patch, MagicMock

from src.event.process_command_queue_event import ProcessCommandQueueEvent


class TestProcessCommandQueueEvent:

    @pytest.fixture
    def user_config(self):
        return {
            'a': 'user config',
        }

    @pytest.fixture
    def user_config_provider_mock(self, user_config):
        with patch('src.event.process_command_queue_event.UserConfigProvider') as user_config_provider_mock:
            user_config_provider_mock.return_value.get_v2_user_config.return_value = user_config

            yield user_config_provider_mock

    @pytest.fixture
    def update_side_effect(self):
        def update(config, _):
            return config

        return update

    @pytest.fixture
    def create_alert_mock(self, update_side_effect):
        with patch('src.event.process_command_queue_event.CreateAlert') as create_alert_mock:
            create_alert_mock.handle_command = MagicMock(side_effect=update_side_effect)

            yield create_alert_mock

    @pytest.fixture
    def delete_alert_mock(self, update_side_effect):
        with patch('src.event.process_command_queue_event.DeleteAlert') as delete_alert_mock:
            delete_alert_mock.handle_command = MagicMock(side_effect=update_side_effect)

            yield delete_alert_mock

    @pytest.fixture
    def update_alert_mock(self, update_side_effect):
        with patch('src.event.process_command_queue_event.UpdateAlert') as update_alert_mock:
            update_alert_mock.handle_command = MagicMock(side_effect=update_side_effect)

            yield update_alert_mock

    @pytest.fixture
    def sqs_proxy_mock(self):
        with patch('src.event.process_command_queue_event.SqsProxy') as sqs_proxy:
            yield sqs_proxy

    @pytest.fixture
    def create_alert_command(self):
        return {
            'commandName': 'CREATE_ALERT',
            'data': 'lskdfjosdif',
        }

    @pytest.fixture
    def delete_alert_command(self):
        return {
            'commandName': 'DELETE_ALERT',
            'data': 'lfsdkmfnowiecw',
        }

    @pytest.fixture
    def update_alert_command(self):
        return {
            'commandName': 'UPDATE_ALERT',
            'data': 'sdfedervbd',
        }

    @pytest.fixture
    def three_receipt_handles(self):
        return [
            'handle-1',
            'handle-2',
            'handle-3',
        ]

    def test_alert_commands(self,
                            create_alert_mock,
                            delete_alert_mock,
                            update_alert_mock,
                            sqs_proxy_mock,
                            user_config_provider_mock,
                            create_alert_command,
                            delete_alert_command,
                            update_alert_command,
                            user_config,
                            three_receipt_handles
                            ):
        under_test = ProcessCommandQueueEvent({
            'Records': [{
                'body': json.dumps(create_alert_command),
                'receiptHandle': three_receipt_handles[0],
            }, {
                'body': json.dumps(delete_alert_command),
                'receiptHandle': three_receipt_handles[1],
            }, {
                'body': json.dumps(update_alert_command),
                'receiptHandle': three_receipt_handles[2],
            }]
        }, {})

        under_test.handle()

        create_alert_mock.handle_command.assert_called_once_with(user_config, create_alert_command['data'])
        delete_alert_mock.handle_command.assert_called_once_with(user_config, delete_alert_command['data'])
        update_alert_mock.handle_command.assert_called_once_with(user_config, update_alert_command['data'])

        user_config_provider_mock.return_value.update_v2_user_config.assert_called_once_with(user_config)

        sqs_proxy_mock.return_value.delete_api_command_messages.assert_called_once_with(three_receipt_handles)

    def test_unknown_command(self,
                             sqs_proxy_mock,
                             user_config_provider_mock,
                             create_alert_mock,
                             delete_alert_mock,
                             update_alert_mock,
                             ):
        under_test = ProcessCommandQueueEvent({
            'Records': [{
                'body': json.dumps({'commandName': 'unknown'}),
                'receiptHandle': 'asdf',
            }]
        }, {})

        under_test.handle()

        create_alert_mock.return_value.handle_command.assert_not_called()
        delete_alert_mock.return_value.handle_command.assert_not_called()
        update_alert_mock.return_value.handle_command.assert_not_called()
