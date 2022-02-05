from dataclasses import dataclass
from datetime import datetime

from src.model.notification_preference_config import NotificationPreferenceConfig
from src.model.auto_book_preference_config import AutoBookPreferenceConfig


@dataclass
class CampgroundReservationConfigV1:
    campground_id: int
    check_in_date: datetime
    check_out_date: datetime
    notification_preferences: NotificationPreferenceConfig
    auto_book_preferences: AutoBookPreferenceConfig
