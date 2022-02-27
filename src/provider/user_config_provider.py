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
                'campgroundId': '272300',  # J-Tree - Jumbo Rocks
                'checkInDate': '04/01/2022',
                'checkOutDate': '04/03/2022',
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
                'campgroundId': '234059',  # Arches - Devils Garden
                'checkInDate': '05/24/2022',
                'checkOutDate': '05/27/2022',
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
                'campgroundId': '272245',  # Capital Reef - Fruita
                'checkInDate': '05/09/2022',
                'checkOutDate': '05/12/2022',
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
                'campgroundId': '233187',  # Rocky Mountain - Aspenglen
                'checkInDate': '06/17/2022',
                'checkOutDate': '06/19/2022',
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
                'campgroundId': '232463',  # Rocky Mountain - Moraine
                'checkInDate': '06/17/2022',
                'checkOutDate': '06/19/2022',
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
                'campgroundId': '232462',  # Rocky Mountain - Glacier Basin
                'checkInDate': '06/17/2022',
                'checkOutDate': '06/19/2022',
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
