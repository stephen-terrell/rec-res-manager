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
                'campgroundId': '10101362',  # Great Basin - Lower Lehman Creek
                'checkInDate': '05/30/2022',
                'checkOutDate': '06/02/2022',
                'allowRvLikeSites': False,
                'notificationPreferences': {
                    'notificationsEnabled': True,
                    'notificationSensitivityLevel': 'ANY_DAYS_AVAILABLE',
                },
                'autoBookPreferences': {
                    'attemptAutoBook': True,
                    'autoBookSensitivityLevel': 'ALL_DAYS_AVAILABLE',
                },
            }, {
                'campgroundId': '10101374',  # Great Basin - Upper Lehman Creek
                'checkInDate': '05/30/2022',
                'checkOutDate': '06/02/2022',
                'allowRvLikeSites': False,
                'notificationPreferences': {
                    'notificationsEnabled': True,
                    'notificationSensitivityLevel': 'ANY_DAYS_AVAILABLE',
                },
                'autoBookPreferences': {
                    'attemptAutoBook': True,
                    'autoBookSensitivityLevel': 'ALL_DAYS_AVAILABLE',
                },
            }, {
                'campgroundId': '234039',  # Lassen Volcanic - Manzanita Lake
                'checkInDate': '06/05/2022',
                'checkOutDate': '06/08/2022',
                'allowRvLikeSites': False,
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
