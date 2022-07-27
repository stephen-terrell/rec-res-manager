from typing import List

from src.model.reservation_config import ReservationConfigV1
from src.factory.reservation_config_factory import ReservationConfigFactory


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
                'campgroundId': '258795',  # Glacier - Sprague Creek
                'checkInDate': '08/01/2022',
                'checkOutDate': '08/04/2022',
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
