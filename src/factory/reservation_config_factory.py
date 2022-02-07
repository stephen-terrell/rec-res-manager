from datetime import datetime

from src.model.reservation_config import ReservationConfigV1
from src.model.campground_reservation_config import CampgroundReservationConfigV1
from src.model.notification_preference_config import NotificationPreferenceConfig
from src.model.auto_book_preference_config import AutoBookPreferenceConfig
from src.model.enum.sensitivity_level import SensitivityLevel


class ReservationConfigFactory:

    __date_format: str = '%m/%d/%Y'

    def get_reservation_config(self, user_config: dict) -> ReservationConfigV1:
        campgrounds = []
        for campground in user_config['campgrounds']:
            campgrounds.append(self._get_campground_config(campground))

        result = ReservationConfigV1(
            owner_id=user_config.get('owner'),
            subscribers=user_config.get('subscribers'),
            auto_book_credentials='',
            campgrounds=campgrounds,
            permits=[]
        )

        return result

    def _get_campground_config(self, config: dict) -> CampgroundReservationConfigV1:
        result = CampgroundReservationConfigV1(
            campground_id=config.get('campgroundId'),
            check_in_date=datetime.strptime(config.get('checkInDate'), self.__date_format),
            check_out_date=datetime.strptime(config.get('checkOutDate'), self.__date_format),
            allow_rv_like_sites=config.get('allowRvLikeSites'),
            notification_preferences=self._get_notification_preference(config.get('notificationPreferences')),
            auto_book_preferences=self._get_auto_book_preferences(config.get('autoBookPreferences'))
        )

        return result

    def _get_notification_preference(self, config: dict) -> NotificationPreferenceConfig:
        result = NotificationPreferenceConfig(
            notifications_enabled=config.get('notificationsEnabled'),
            notification_sensitivity_level=SensitivityLevel[config.get('notificationSensitivityLevel')]
        )

        return result

    def _get_auto_book_preferences(self, config: dict) -> AutoBookPreferenceConfig:
        result = AutoBookPreferenceConfig(
            attempt_auto_book=config.get('attemptAutoBook'),
            auto_book_sensitivity_level=SensitivityLevel[config.get('autoBookSensitivityLevel')]
        )

        return result
