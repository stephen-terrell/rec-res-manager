from dataclasses import dataclass

from src.model.enum.protocol_type import ProtocolType


@dataclass
class PermitReservationConfigV1:
    permit_id: int
    protocol: ProtocolType
