from dataclasses import dataclass


@dataclass
class NotificationPreferenceConfig:
    notifications_enabled: bool
    notification_sensitivity_level: str
