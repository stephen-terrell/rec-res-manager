from dataclasses import dataclass, field

from src.model.enum.campsite_type import CampsiteType


@dataclass
class CampsiteAvailability:
    campsite_id: str
    campsite_type: CampsiteType
    site: str
    availabilities: dict = field(default_factory=dict)

    def is_fully_available(self) -> bool:
        for key, value in self.availabilities.items():
            if value != 'Available':
                return False

        return True

    def is_partially_available(self) -> bool:
        for key, value in self.availabilities.items():
            if value == 'Available':
                return True

        return False

    def add_availability(self, date: str, status: str):
        self.availabilities[date] = status
