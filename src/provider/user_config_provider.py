from model.reservation_config import ReservationConfigV1
from factory.reservation_config_factory import ReservationConfigFactory
from typing import List


class UserConfigProvider:
    reservation_config_factory: ReservationConfigFactory

    def __init__(self):
        self.reservation_config_factory = ReservationConfigFactory()

    def get_user_configs(self) -> List[ReservationConfigV1]:
        result = []

        for config in camp_configs:
            result.append(self.reservation_config_factory.get_reservation_config(user_config=config))

        return result


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
                'campgroundId': 232445,
                'checkInDate': '04/01/2022',
                'checkOutDate': '04/05/2022',
                'notificationPreferences': {
                    'notificationsEnabled': True,
                    'notificationSensitivityLevel': 'ANY_DAY_AVAILABLE',
                },
                'autoBookPreferences': {
                    'attemptAutoBook': True,
                    'autoBookSensitivityLevel': 'ALL_DAYS_AVAILABLE_NO_RV',
                },
            },
        ],
        'permits': [
            {
                'coming': 'soon',
            },
        ],
    },
]
