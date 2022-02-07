from dataclasses import dataclass, field
from typing import List

from src.model.campsite_availability import CampsiteAvailability
from src.proxy.recreation_prox import RecreationProxy


@dataclass
class CampgroundAvailability:
    campground_id: str
    __campground_name: dict = field(init=False, default=None)
    __campsites: List[CampsiteAvailability] = field(default_factory=lambda: [], init=False)

    __recreation_proxy: RecreationProxy = field(init=False)

    def __post_init__(self):
        self.__recreation_proxy = RecreationProxy()

    def add_campsite(self, campsite: CampsiteAvailability):
        self.__campsites.append(campsite)

    def get_campsites(self) -> List[CampsiteAvailability]:
        return self.__campsites

    def get_campground_name(self):
        if self.__campground_name is None:
            self.__campground_name = self.__recreation_proxy.get_campground_name(self.campground_id)

        return self.__campground_name
