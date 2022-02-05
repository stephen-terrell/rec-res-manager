from dataclasses import dataclass, field
import requests

from src.provider.user_config_provider import UserConfigProvider


@dataclass
class CheckReservationsEvent:
    event: dict
    context: dict

    _user_config_provider: UserConfigProvider = field(init=False)

    def __post_init__(self):
        self._user_config_provider = UserConfigProvider()

    def handle(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/56.0.2924.76 Safari/537.36',
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate",
            "pragma": "no-cache"
        }
        url_pattern = 'https://www.recreation.gov/api/camps/availability/campground/{campground_id}/month'

        user_configs = self._user_config_provider.get_user_configs()

        for user_config in user_configs:
            for campground in user_config.campgrounds:
                params = {
                    'start_date': campground.check_in_date.strftime('%Y-%m-01T00:00:00.000Z')
                }

                # print(params.get('start_date'))

                result = requests.get(
                    url_pattern.format(campground_id=campground.campground_id),
                    params=params,
                    headers=headers
                )

                print(result.json())
