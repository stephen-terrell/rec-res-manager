import json
import os
from unittest import TestCase
from unittest.mock import patch, MagicMock

import pytest

from src.provider.user_config_provider import UserConfigProvider


@patch.dict(os.environ, {'USER_CONFIG_BUCKET_NAME': 'us-west-2'})
class TestUserConfigProvider:

    @pytest.fixture
    def user_config(self):
        return {'here': 'is a value'}

    @pytest.fixture
    def s3_proxy_mock(self, user_config):
        with patch('src.provider.user_config_provider.S3Proxy') as proxy_mock:
            body_mock = MagicMock()
            body_mock.read.return_value.decode.return_value = json.dumps(user_config)
            get_response = {
                'Body': body_mock
            }
            get_object_mock = MagicMock()
            get_object_mock.return_value = get_response
            proxy_mock.return_value = MagicMock(get_object=get_object_mock)

            yield proxy_mock

    def test_get_user_config_v2(self, s3_proxy_mock, user_config):
        under_test = UserConfigProvider()

        result = under_test.get_user_configs_v2()

        TestCase().assertDictEqual(result, user_config)

    def test_get_user_config_v2_not_found(self, s3_proxy_mock):
        s3_proxy_mock.return_value.get_object.return_value = None

        under_test = UserConfigProvider()

        result = under_test.get_user_configs_v2()

        TestCase().assertDictEqual(result, {})

    def test_get_user_config_empty_string(self, s3_proxy_mock):
        s3_proxy_mock.return_value.get_object.return_value['Body'].read.return_value.decode.return_value = ''

        under_test = UserConfigProvider()

        result = under_test.get_user_configs_v2()

        TestCase().assertDictEqual(result, {})

    def test_get_user_config_empty_config(self, s3_proxy_mock):
        s3_proxy_mock.return_value.get_object.return_value['Body'].read.return_value.decode.return_value = '{}'

        under_test = UserConfigProvider()

        result = under_test.get_user_configs_v2()

        TestCase().assertDictEqual(result, {})
