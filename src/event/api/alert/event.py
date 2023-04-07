from src.event.api.alert.v1.list import ListAlerts

from dataclasses import dataclass


@dataclass
class AlertEvent:
    event: dict
    context: dict

    def __init__(self,  event: dict, context: dict):
        self.event = event
        self.context = context

    def handle(self):
        if 'routeKey' not in self.event:
            raise ValueError(f'invalid routeKey: \"{self.event["routeKey"]}\"')

        # TODO: replace this with match/case whenever AWS gets around to adding python3.9 to Lambda
        route_key = self.event['routeKey']
        if route_key == 'GET /alerts/{user}':
            api_handler = ListAlerts
        else:
            raise ValueError(f'invalid routeKey: \"{self.event["routeKey"]}\"')

        print(self.event)

        return api_handler.enact(self.event)
