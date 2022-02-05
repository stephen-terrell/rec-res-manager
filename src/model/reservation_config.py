from dataclasses import dataclass
from typing import List
from src.model.campground_reservation_config import CampgroundReservationConfigV1
from src.model.permit_reservation_config import PermitReservationConfigV1


@dataclass
class ReservationConfigV1:
    owner_id: str
    subscribers: List[str]
    auto_book_credentials: str
    campgrounds: List[CampgroundReservationConfigV1]
    permits: List[PermitReservationConfigV1]
