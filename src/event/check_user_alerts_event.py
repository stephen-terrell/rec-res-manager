from datetime import datetime
from typing import List

from src.provider.user_config_provider import UserConfigProvider
from src.proxy.recreation_prox import RecreationProxy
from src.model.campsite_availability import CampsiteAvailability
from src.model.campground_availability import CampgroundAvailability
from src.provider.notification_config_provider import NotificationConfigProvider
from src.model.enum.campsite_type import CampsiteType
from src.format.email_formatter import EmailFormatter
from src.proxy.sns_proxy import SnsProxy


class CheckUserAlertsEvent:
    def __init__(self):
        self._user_config_provider = UserConfigProvider()
        self._recreation_proxy = RecreationProxy()
        self._notification_config_provider = NotificationConfigProvider()
        self._email_formatter = EmailFormatter()
        self._sns_proxy = SnsProxy()

        self._allowed_campsite_types = [
            CampsiteType.STANDARD_NONELECTRIC,
            CampsiteType.TENT_ONLY_NONELECTRIC,
            CampsiteType.STANDARD_ELECTRIC,
            CampsiteType.TENT_ONLY_ELECTRIC,
            CampsiteType.SHELTER_NONELECTRIC,
        ]

        self._date_format = "%m/%d/%Y"

    # TODO: unit tests
    def handle(self):
        user_configs = self._user_config_provider.get_v2_user_config()["userConfigs"]
        campgrounds_to_notify = {}
        for user_id, user_config in user_configs.items():
            for _, alert_config in user_config["alertConfigs"].items():
                campground_id = alert_config["campgroundId"]
                sensitivity_level = alert_config["notificationPreferences"]["notificationSensitivityLevel"]
                available_campsites = [
                    campsite
                    for campsite in self._recreation_proxy.get_available_campsites(
                        campground_id,
                        datetime.strptime(alert_config["checkInDate"], self._date_format),
                        datetime.strptime(alert_config["checkOutDate"], self._date_format),
                    )
                    if self._campsite_availability_match(sensitivity_level, campsite)
                    and self._campsite_type_match(campsite)
                ]

                if len(available_campsites) > 0 and self._any_non_notified(user_id, campground_id, available_campsites):
                    if user_id not in campgrounds_to_notify:
                        campgrounds_to_notify[user_id] = {}
                    campgrounds_to_notify[user_id][campground_id] = available_campsites

        for user_id, user_alerts in campgrounds_to_notify.items():
            # TODO: this is a little clunky, could probably move it to its own component
            campgrounds = []
            for campground_id, available_campsites in user_alerts.items():
                campground_availability = CampgroundAvailability(campground_id)
                campground_availability.add_campsites(available_campsites)
                campgrounds.append(campground_availability)
            message = self._email_formatter.get_formatted_message(campgrounds)
            print(message)
            self._sns_proxy.send_notification(user_id, message)

        if len(campgrounds_to_notify.keys()) > 0:
            self._notification_config_provider.update_v2_notification_config(campgrounds_to_notify)

    # TODO: move this somewhere and inject it
    def _campsite_type_match(self, campsite: CampsiteAvailability):
        return campsite.campsite_type in self._allowed_campsite_types

    # TODO: move this somewhere and inject it
    def _campsite_availability_match(self, sensitivity_level: str, campsite: CampsiteAvailability):
        if sensitivity_level == "ALL_DAYS_AVAILABLE":
            return campsite.is_fully_available()
        if sensitivity_level == "ANY_DAY_AVAILABLE":
            return campsite.is_partially_available()

        return False

    # TODO: probably just update this to do a compare of the two dicts
    # TODO: move this somewhere an inject it
    def _any_non_notified(
        self,
        owner: str,
        campground_id: str,
        campsite_availabilities: List[CampsiteAvailability],
    ) -> bool:
        notification_config = self._notification_config_provider.get_v2_notification_config()
        if owner not in notification_config or campground_id not in notification_config[owner]:
            return True

        for campsite in campsite_availabilities:
            if campsite.campsite_id not in notification_config[owner][campground_id]:
                return True
            campsite_config = notification_config[owner][campground_id][campsite.campsite_id]

            for key, value in campsite.availabilities.items():
                if key not in campsite_config or (campsite_config.get(key) != "Available" and value == "Available"):
                    return True

        return False
