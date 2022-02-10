import requests
from datetime import datetime


class RecreationProxy:
    __headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.76 Safari/537.36',
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate",
        "pragma": "no-cache"
    }

    def get_campground_availability(self, campground_id: str, start_date: datetime, end_date: datetime) -> dict:
        availability = self.__get_campground_availability(campground_id=campground_id, start_date=start_date)

        if start_date.month != end_date.month:
            next_month_availability = self.__get_campground_availability(
                campground_id=campground_id,
                start_date=end_date
            )

            for campsite_id, campsite_availability in availability.get('campsites').items():
                if campsite_id in next_month_availability.get('campsites'):
                    availability['campsites'][campsite_id]['availabilities'] = {
                        **availability.get('campsites').get(campsite_id).get('availabilities'),
                        **next_month_availability.get('campsites').get(campsite_id).get('availabilities')
                    }

        return availability

    def get_campground_name(self, campground_id: str) -> dict:
        url_pattern = 'https://www.recreation.gov/api/camps/campgrounds/{campground_id}'

        result = requests.get(
            url_pattern.format(campground_id=campground_id),
            headers=self.__headers
        ).json()

        return {
            'facility_name': result.get('campground').get('facility_name'),
            'alternate_names': result.get('campground').get('alternate_names'),
        }

    def __get_campground_availability(self, campground_id: str, start_date) -> dict:
        url_pattern = 'https://www.recreation.gov/api/camps/availability/campground/{campground_id}/month'

        params = {
            'start_date': start_date.strftime('%Y-%m-01T00:00:00.000Z')
        }

        get_request = requests.get(
            url_pattern.format(campground_id=campground_id),
            params=params,
            headers=self.__headers
        )

        if not get_request.ok:
            print('===== Error getting data from recreation api =====')
            print(f'Status code: {get_request.status_code}')
            print(f'Reason: "{get_request.reason}"')

            return None

        return get_request.json()
