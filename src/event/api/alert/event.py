import json
from src.event.api.alert.v1.list import ListAlerts
from src.event.api.alert.v1.get import GetAlert
from src.event.api.alert.v1.put import PutAlert
from src.event.api.alert.v1.delete import DeleteAlert
from src.event.api.alert.v1.post import PostAlert

from dataclasses import dataclass


@dataclass
class AlertEvent:
    __event: dict
    __context: dict

    def __init__(self,  event: dict, context: dict):
        self.__event = event
        if 'body' in event:
            self.__event['body'] = json.loads(event['body'])
        self.__context = context

    def handle(self):
        if 'routeKey' not in self.__event:
            raise ValueError(f'Unknown event: {self.__event}')

        # TODO: replace this with match/case whenever AWS gets around to adding python3.9 to Lambda
        route_key = self.__event['routeKey']
        if route_key == 'GET /alerts':
            api_handler = ListAlerts
        elif route_key == 'GET /alerts/{alertId}':
            api_handler = GetAlert
        elif route_key == 'PUT /alerts':
            api_handler = PutAlert
        elif route_key == 'POST /alerts/{alertId}':
            api_handler = PostAlert
        elif route_key == 'DELETE /alerts/{alertId}':
            api_handler = DeleteAlert
        else:
            raise ValueError(f'invalid routeKey: \"{self.__event["routeKey"]}\"')

        print(self.__event)

        api_handler = api_handler(self.__event)
        return api_handler.enact()
