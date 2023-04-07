import json
import os
import pytest
from unittest.mock import patch, MagicMock
from unittest import TestCase

from src.event.api.alert.v1.list import ListAlerts


class TestList:
    @pytest.fixture
    def user_id_1(self):
        return 'stephen'

    @pytest.fixture
    def user_id_2(self):
        return 'carly'

    @pytest.fixture
    def make_alert_config(self):
        def _make_alert_config(campground_id, check_in_date):
            return {
                'type': 'recreation.gov',
                'campgroundId': campground_id,
                'checkInDate': check_in_date,
                'checkOutDate': '08/17/2023',
                'notificationPreferences': {
                    'notificationsEnabled': True,
                    'notificationSensitivityLevel': 'ANY_DAYS_AVAILABLE'
                }
            }

        return _make_alert_config

    @pytest.fixture
    def alert_config_1(self, make_alert_config):
        return make_alert_config('234059', '08/15/2023')

    @pytest.fixture
    def alert_config_2(self, make_alert_config):
        return make_alert_config('56573', '08/01/2023')

    @pytest.fixture
    def alert_config_3(self, make_alert_config):
        return make_alert_config('55555', '08/01/2024')

    @pytest.fixture
    def alert_id_1(self):
        return '111111111'

    @pytest.fixture
    def alert_id_2(self):
        return '222222222'

    @pytest.fixture
    def alert_id_3(self):
        return '333333333'

    @pytest.fixture
    def user_config(self,
                    user_id_1,
                    user_id_2,
                    alert_config_1,
                    alert_config_2,
                    alert_config_3,
                    alert_id_1,
                    alert_id_2,
                    alert_id_3):
        return {
            'userConfigs': {
                user_id_1: {
                    'version': 1,
                    'alertSubscriptions': [
                        {
                            'endpoint': 'scubastevegcn@gmail.com',
                            'protocol': 'email',
                        }
                    ],
                    'alertConfigs': {
                        alert_id_1: alert_config_1,
                    }
                },
                user_id_2: {
                    'version': 1,
                    'alertSubscriptions': [
                        {
                            'endpoint': 'scubastevegcn@gmail.com',
                            'protocol': 'email',
                        }
                    ],
                    'alertConfigs': {
                        alert_id_2: alert_config_2,
                        alert_id_3: alert_config_3,
                    }
                }
            },
            'version': 1
        }

    @pytest.fixture
    def s3_proxy_mock(self, user_config):
        with patch('src.event.api.alert.v1.list.S3Proxy') as proxy_mock:
            body_mock = MagicMock()
            body_mock.read.return_value.decode.return_value = json.dumps(user_config)
            get_response = {
                'Body': body_mock
            }
            get_object_mock = MagicMock()
            get_object_mock.return_value = get_response
            proxy_mock.return_value = MagicMock(get_object=get_object_mock)

            yield proxy_mock

    @patch.dict(os.environ, {'USER_CONFIG_BUCKET_NAME': 'us-west-2'})
    def test_list_alerts(self, s3_proxy_mock, alert_config_1, user_id_1, alert_id_1):
        under_test = ListAlerts()

        result = under_test.enact({'pathParameters': {'userId': user_id_1}})

        assert len(result) == 1
        TestCase().assertDictEqual(result[0], {
            'userId': user_id_1,
            'alertId': alert_id_1,
            **alert_config_1
        })

    @patch.dict(os.environ, {'USER_CONFIG_BUCKET_NAME': 'us-west-2'})
    def test_list_alerts_multiple(
            self,
            s3_proxy_mock,
            alert_config_2,
            alert_config_3,
            user_id_2,
            alert_id_2,
            alert_id_3
    ):
        under_test = ListAlerts()

        result = under_test.enact({'pathParameters': {'userId': user_id_2}})

        assert len(result) == 2
        TestCase().assertDictEqual(result[0], {
            'userId': user_id_2,
            'alertId': alert_id_2,
            **alert_config_2
        })
        TestCase().assertDictEqual(result[1], {
            'userId': user_id_2,
            'alertId': alert_id_3,
            **alert_config_3
        })
