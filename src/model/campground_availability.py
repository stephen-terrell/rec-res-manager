from dataclasses import dataclass, field
from typing import List

from src.model.campsite_availability import CampsiteAvailability
from src.proxy.recreation_prox import RecreationProxy


@dataclass
class CampgroundAvailability:
    campground_id: str
    __campground_name: dict = field(default_factory=lambda: {}, init=False)
    __campsites: List[CampsiteAvailability] = field(default_factory=lambda: [], init=False)

    __recreation_proxy: RecreationProxy = field(init=False)

    def __post_init__(self):
        self.__recreation_proxy = RecreationProxy()

    def add_campsite(self, campsite: CampsiteAvailability):
        self.__campsites.append(campsite)

    def add_campsites(self, campsites: List[CampsiteAvailability]):
        self.__campsites.extend(campsites)

    def get_campsites(self) -> List[CampsiteAvailability]:
        return self.__campsites

    def get_campground_name(self):
        if not self.__campground_name:
            self.__campground_name = self.__recreation_proxy.get_campground_name(self.campground_id)

        return self.__campground_name
