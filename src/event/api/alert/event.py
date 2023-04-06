from src.event.api.alert.v1.list import list_alerts

from dataclasses import dataclass


@dataclass
class AlertEvent:
    event: dict
    context: dict

    def __init__(self,  event: dict, context: dict):
        self.event = event
        self.context = context

    def handle(self):
        match self.event:
            case {'routeKey': 'GET /alerts/{user}'}:
                api_handler = list_alerts
            case _:
                raise ValueError(f'invalid routeKey: \"{self.event["routeKey"]}\"')

        print(self.event)

        return api_handler(self.event)
