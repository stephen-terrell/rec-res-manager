from dataclasses import dataclass


@dataclass
class AutoBookPreferenceConfig:
    attempt_auto_book: bool
    auto_book_sensitivity_level: str
