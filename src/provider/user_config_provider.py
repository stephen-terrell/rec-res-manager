import json
import os
from typing import List

from src.factory.reservation_config_factory import ReservationConfigFactory
from src.model.reservation_config import ReservationConfigV1
from src.proxy.s3_proxy import S3Proxy


class UserConfigProvider:
    reservation_config_factory: ReservationConfigFactory
    s3_proxy: S3Proxy
    __user_config_bucket_name: str
    __user_config_key_name: str

    def __init__(self):
        self.reservation_config_factory = ReservationConfigFactory()
        self.s3_proxy = S3Proxy()
        self.__user_config_bucket_name = os.environ['USER_CONFIG_BUCKET_NAME']
        self.__user_config_key_name = 'user-config-v2.json'

    def get_user_configs(self) -> List[ReservationConfigV1]:
        result = []

        for config in camp_configs:
            result.append(self.reservation_config_factory.get_reservation_config(user_config=config))

        return result

    def get_user_configs_v2(self) -> dict:
        get_object_result = self.s3_proxy.get_object(self.__user_config_bucket_name, self.__user_config_key_name)

        if get_object_result is None or 'Body' not in get_object_result:
            return {}

        decoded_result = get_object_result['Body'].read().decode('utf-8')

        if decoded_result == '' or decoded_result == '{}':
            return {}

        return json.loads(decoded_result)

camp_configs = [
    {
        'owner': 'carly-stephen',
        'version': 1,
        'subscribers': [
            'something@gmail.com',
        ],
        'autoBookCredentials': {
            'enc': '',
        },
        'campgrounds': [
            {
                'campgroundId': '251906',  # Olympic - Sol Duc
                'checkInDate': '08/15/2022',
                'checkOutDate': '08/17/2022',
                'allowRvLikeSites': True,
                'notificationPreferences': {
                    'notificationsEnabled': True,
                    'notificationSensitivityLevel': 'ANY_DAYS_AVAILABLE',
                },
                'autoBookPreferences': {
                    'attemptAutoBook': True,
                    'autoBookSensitivityLevel': 'ALL_DAYS_AVAILABLE',
                },
            }
        ],
        'permits': [
            {
                'coming': 'soon',
            },
        ],
    },
]
