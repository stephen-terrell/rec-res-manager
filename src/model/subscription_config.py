from dataclasses import dataclass

from src.model.enum.protocol_type import ProtocolType


@dataclass
class SubscriptionConfig:
    endpoint: str
    protocol_type: ProtocolType
