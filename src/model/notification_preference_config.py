from dataclasses import dataclass

from src.model.enum.sensitivity_level import SensitivityLevel


@dataclass
class NotificationPreferenceConfig:
    notifications_enabled: bool
    notification_sensitivity_level: SensitivityLevel
