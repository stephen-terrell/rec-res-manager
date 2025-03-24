import requests
import time
from datetime import datetime, timedelta
from typing import List

from src.model.campsite_availability import CampsiteAvailability
from src.model.enum.campsite_type import CampsiteType


class RecreationProxy:
    __headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/134.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate",
        "pragma": "no-cache",
        "Host": "www.recreation.gov",
    }

    def get_campground_availability(self, campground_id: str, start_date: datetime, end_date: datetime) -> dict:
        availability = self.__get_campground_availability(campground_id=campground_id, start_date=start_date)

        if start_date.month != end_date.month:
            next_month_availability = self.__get_campground_availability(
                campground_id=campground_id, start_date=end_date
            )

            # TODO: update to .keys()
            for campsite_id, _ in availability["campsites"].items():
                if campsite_id in next_month_availability["campsites"]:
                    availability["campsites"][campsite_id]["availabilities"] = {
                        **availability["campsites"][campsite_id]["availabilities"],
                        **next_month_availability["campsites"][campsite_id]["availabilities"],
                    }

        return availability

    def get_available_campsites(
        self, campground_id: str, check_in_date: datetime, check_out_date: datetime
    ) -> List[CampsiteAvailability]:
        end_date = check_out_date - timedelta(days=1)
        campground_availability = self.get_campground_availability(campground_id, check_in_date, end_date)

        campsites = [
            CampsiteAvailability(
                campsite_id=campsite_id,
                campsite_type=CampsiteType(campsite_data["campsite_type"]),
                site=campsite_data["site"],
                availabilities={
                    datetime.strptime(date, "%Y-%m-%dT00:00:00Z").strftime("%Y-%m-%d"): status
                    for date, status in campsite_data["availabilities"].items()
                    if check_in_date <= datetime.strptime(date, "%Y-%m-%dT00:00:00Z") <= end_date
                },
            )
            for campsite_id, campsite_data in campground_availability["campsites"].items()
        ]

        return [campsite for campsite in campsites if campsite.is_partially_available()]

    def get_campground_name(self, campground_id: str) -> dict:
        time.sleep(0.1)
        url_pattern = "https://www.recreation.gov/api/camps/campgrounds/{campground_id}"

        result = requests.get(url_pattern.format(campground_id=campground_id), headers=self.__headers, timeout=5).json()

        return {
            "facility_name": result.get("campground").get("facility_name"),
            "alternate_names": result.get("campground").get("alternate_names"),
        }

    def __get_campground_availability(self, campground_id: str, start_date) -> dict:
        time.sleep(0.1)
        url_pattern = "https://www.recreation.gov/api/camps/availability/campground/{campground_id}/month"

        params = {"start_date": start_date.strftime("%Y-%m-01T00:00:00.000Z")}

        get_request = requests.get(
            url_pattern.format(campground_id=campground_id),
            params=params,
            headers=self.__headers,
            timeout=5,
        )

        if not get_request.ok:
            print("===== Error getting data from recreation api =====")
            print(f"Status code: {get_request.status_code}")
            print(f'Reason: "{get_request.reason}"')

            return {}

        return get_request.json()
