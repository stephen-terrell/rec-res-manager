from dataclasses import dataclass
from datetime import datetime

from src.model.notification_preference_config import NotificationPreferenceConfig
from src.model.auto_book_preference_config import AutoBookPreferenceConfig


@dataclass
class CampgroundReservationConfigV1:
    campground_id: str
    check_in_date: datetime
    check_out_date: datetime
    allow_rv_like_sites: bool
    notification_preferences: NotificationPreferenceConfig
    auto_book_preferences: AutoBookPreferenceConfig
