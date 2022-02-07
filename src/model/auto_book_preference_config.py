from dataclasses import dataclass

from src.model.enum.sensitivity_level import SensitivityLevel


@dataclass
class AutoBookPreferenceConfig:
    attempt_auto_book: bool
    auto_book_sensitivity_level: SensitivityLevel
