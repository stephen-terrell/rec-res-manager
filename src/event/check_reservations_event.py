from dataclasses import dataclass, field
from datetime import timedelta
from typing import List

from src.provider.user_config_provider import UserConfigProvider
from src.model.campsite_availability import CampsiteAvailability
from src.model.campground_availability import CampgroundAvailability
from src.model.enum.sensitivity_level import SensitivityLevel
from src.model.enum.campsite_type import CampsiteType
from src.model.notification_preference_config import NotificationPreferenceConfig
from src.proxy.sns_proxy import SnsProxy
from src.format.email_formatter import EmailFormatter
from src.proxy.recreation_prox import RecreationProxy
from src.provider.notification_config_provider import NotificationConfigProvider


@dataclass
class CheckReservationsEvent:
    event: dict
    context: dict

    _user_config_provider: UserConfigProvider = field(init=False)
    _sns_proxy: SnsProxy = field(init=False)
    _email_formatter: EmailFormatter = field(init=False)
    _recreation_proxy: RecreationProxy = field(init=False)
    _notification_config_provider: NotificationConfigProvider = field(init=False)

    __allowed_campsite_types: List = field(init=False)
    __rv_like_campsites: List = field(init=False)

    def __post_init__(self):
        self._user_config_provider = UserConfigProvider()
        self._sns_proxy = SnsProxy()
        self._email_formatter = EmailFormatter()
        self._recreation_proxy = RecreationProxy()
        self._notification_config_provider = NotificationConfigProvider()
        self.__allowed_campsite_types = [
            CampsiteType.STANDARD_NONELECTRIC,
            CampsiteType.TENT_ONLY_NONELECTRIC,
            CampsiteType.STANDARD_ELECTRIC,
            CampsiteType.TENT_ONLY_ELECTRIC,
            CampsiteType.SHELTER_NONELECTRIC,
        ]
        self.__rv_like_campsites = [
            CampsiteType.RV_ELECTRIC,
        ]

    # flake8: noqa: C901
    def handle(self):
        user_configs = self._user_config_provider.get_user_configs()
        notification_config_update = {}

        for user_config in user_configs:
            campground_availabilities: List[CampgroundAvailability] = []
            for campground_config in user_config.campgrounds:
                campground_availability = CampgroundAvailability(campground_id=campground_config.campground_id)

                requested_campground_availability = self._recreation_proxy.get_campground_availability(
                    campground_id=campground_config.campground_id,
                    start_date=campground_config.check_in_date,
                    end_date=campground_config.check_out_date,
                )

                if not requested_campground_availability:
                    print("Probably got an error from recreation api. will retry next go.")

                    continue

                for (
                    campsite_id,
                    campsite_availability,
                ) in requested_campground_availability.get("campsites").items():
                    campsite_type = CampsiteType(campsite_availability.get("campsite_type"))

                    if not self.__campsite_type_match(campground_config.allow_rv_like_sites, campsite_type):
                        continue

                    campsite = CampsiteAvailability(
                        campsite_id=campsite_id,
                        campsite_type=campsite_type,
                        site=campsite_availability.get("site"),
                    )

                    check_date = campground_config.check_in_date
                    while check_date < campground_config.check_out_date:
                        campsite.add_availability(
                            date=check_date.strftime("%Y-%m-%d"),
                            status=campsite_availability.get("availabilities").get(
                                str(check_date.strftime("%Y-%m-%dT00:00:00Z"))
                            ),
                        )
                        check_date += timedelta(days=1)

                    if not self.__availability_match(campsite, campground_config.notification_preferences):
                        continue

                    if not self.__any_non_notified(user_config.owner_id, campground_config.campground_id, campsite):
                        continue

                    campground_availability.add_campsite(campsite)

                if len(campground_availability.get_campsites()) > 0:
                    campground_availabilities.append(campground_availability)
                else:
                    print(
                        "found no availabilities for campground: {campground_id}".format(
                            campground_id=campground_config.campground_id
                        )
                    )

            # we found something we should tell the customer about
            if len(campground_availabilities) > 0:
                self.__notify_found_availabilities(user_config.owner_id, campground_availabilities)

                if user_config.owner_id not in notification_config_update:
                    notification_config_update[user_config.owner_id] = {}

                for ca in campground_availabilities:
                    notification_config_update[user_config.owner_id][ca.campground_id] = {}
                    for cs in ca.get_campsites():
                        notification_config_update[user_config.owner_id][ca.campground_id][
                            cs.campsite_id
                        ] = cs.availabilities

        if len(notification_config_update.items()):
            self._notification_config_provider.update_notification_config(notification_config_update)

    def __notify_found_availabilities(self, owner: str, campground_availabilities: List[CampgroundAvailability]):
        message_string = self._email_formatter.get_formatted_message(campground_availabilities)
        print(message_string)
        self._sns_proxy.send_notification(owner=owner, message=message_string)

    def __availability_match(
        self,
        campsite: CampsiteAvailability,
        notification_preferences: NotificationPreferenceConfig,
    ) -> bool:
        if (
            campsite.is_fully_available()
            and notification_preferences.notification_sensitivity_level == SensitivityLevel.ALL_DAYS_AVAILABLE
        ):
            return True
        if (
            campsite.is_partially_available()
            and notification_preferences.notification_sensitivity_level == SensitivityLevel.ANY_DAYS_AVAILABLE
        ):
            return True

        return False

    def __campsite_type_match(self, allow_rv_like_sites: bool, campsite_type: CampsiteType):
        if allow_rv_like_sites and (
            campsite_type in self.__rv_like_campsites or campsite_type in self.__allowed_campsite_types
        ):
            return True
        if not allow_rv_like_sites and campsite_type in self.__allowed_campsite_types:
            return True

        return False

    def __any_non_notified(
        self,
        owner: str,
        campground_id: str,
        campsite_availability: CampsiteAvailability,
    ) -> bool:
        notification_config = self._notification_config_provider.get_notification_config()
        if (
            owner not in notification_config
            or campground_id not in notification_config[owner]
            or campsite_availability.campsite_id not in notification_config[owner][campground_id]
        ):
            return True

        campsite_config = notification_config[owner][campground_id][campsite_availability.campsite_id]

        for key, value in campsite_availability.availabilities.items():
            if key not in campsite_config or (campsite_config.get(key) != "Available" and value == "Available"):
                return True

        return False
