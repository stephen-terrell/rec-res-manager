from datetime import datetime

from src.model.reservation_config import ReservationConfigV1
from src.model.campground_reservation_config import CampgroundReservationConfigV1
from src.model.notification_preference_config import NotificationPreferenceConfig
from src.model.auto_book_preference_config import AutoBookPreferenceConfig
from src.model.enum.sensitivity_level import SensitivityLevel


class ReservationConfigFactory:
    __date_format: str = "%m/%d/%Y"

    def get_reservation_config(self, user_config: dict) -> ReservationConfigV1:
        campgrounds = []
        for campground in user_config["campgrounds"]:
            campgrounds.append(self._get_campground_config(campground))

        result = ReservationConfigV1(
            owner_id=user_config["owner"],
            subscribers=user_config["subscribers"],
            auto_book_credentials="",
            campgrounds=campgrounds,
            permits=[],
        )

        return result

    def _get_campground_config(self, config: dict) -> CampgroundReservationConfigV1:
        result = CampgroundReservationConfigV1(
            campground_id=config["campgroundId"],
            check_in_date=datetime.strptime(config["checkInDate"], self.__date_format),
            check_out_date=datetime.strptime(config["checkOutDate"], self.__date_format),
            allow_rv_like_sites=config["allowRvLikeSites"],
            notification_preferences=self._get_notification_preference(config["notificationPreferences"]),
            auto_book_preferences=self._get_auto_book_preferences(config["autoBookPreferences"]),
        )

        return result

    def _get_notification_preference(self, config: dict) -> NotificationPreferenceConfig:
        result = NotificationPreferenceConfig(
            notifications_enabled=config["notificationsEnabled"],
            notification_sensitivity_level=SensitivityLevel[config["notificationSensitivityLevel"]],
        )

        return result

    def _get_auto_book_preferences(self, config: dict) -> AutoBookPreferenceConfig:
        result = AutoBookPreferenceConfig(
            attempt_auto_book=config["attemptAutoBook"],
            auto_book_sensitivity_level=SensitivityLevel[config["autoBookSensitivityLevel"]],
        )

        return result
