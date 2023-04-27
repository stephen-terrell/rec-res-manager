import os
import pytest
from unittest.mock import patch
from unittest import TestCase

from src.event.api.alert.v1.list import ListAlerts


@patch.dict(os.environ, {'USER_CONFIG_BUCKET_NAME': 'us-west-2'})
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
    def user_config_provider(self, user_config):
        with patch('src.event.api.alert.v1.list.UserConfigProvider') as user_config_provider_mock:
            user_config_provider_mock.return_value.get_v2_user_config.return_value = user_config

            yield user_config_provider_mock

    @pytest.fixture
    def make_event(self):
        def _make_event(user_id):
            return {
                'headers': {'x-rec-res-user-id': user_id}
            }

        return _make_event

    def test_enact(self, make_event, user_config_provider, alert_config_1, user_id_1, alert_id_1):
        under_test = ListAlerts(make_event(user_id_1))

        result = under_test.enact()

        assert len(result) == 1
        TestCase().assertDictEqual(result[0], {
            'userId': user_id_1,
            'alertId': alert_id_1,
            **alert_config_1
        })

    def test_enact_multiple(
            self,
            make_event,
            user_config_provider,
            alert_config_2,
            alert_config_3,
            user_id_2,
            alert_id_2,
            alert_id_3
    ):
        under_test = ListAlerts(make_event(user_id_2))

        result = under_test.enact()

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

    def test_enact_unknown_user(self, make_event, user_config_provider):
        under_test = ListAlerts(make_event('who'))

        result = under_test.enact()

        assert len(result) == 0

    def test_enact_no_object(self, make_event, user_config_provider):
        user_config_provider.return_value.get_v2_user_config.return_value = None

        under_test = ListAlerts(make_event('who'))

        result = under_test.enact()

        assert len(result) == 0

    def test_enact_empty_config(self, make_event, user_config_provider):
        user_config_provider.return_value.get_v2_user_config.return_value = {}

        under_test = ListAlerts(make_event('who'))

        result = under_test.enact()

        assert len(result) == 0

    def test_enact_missing_key(self, make_event, user_config_provider):
        user_config_provider.return_value.get_v2_user_config.return_value = {'asdf': '1234'}

        under_test = ListAlerts(make_event('who'))

        result = under_test.enact()

        assert len(result) == 0
