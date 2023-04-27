import json
from src.event.api.alert.v1.delete import DeleteAlert
from src.event.api.alert.v1.get import GetAlert
from src.event.api.alert.v1.list import ListAlerts
from src.event.api.alert.v1.post import PostAlert
from src.event.api.alert.v1.put import PutAlert

from dataclasses import dataclass


@dataclass
class AlertEvent:
    __event: dict
    __context: dict

    def __init__(self,  event: dict, context: dict):
        self.__event = event
        if 'body' in event:
            # TODO: what is this for?
            self.__event['body'] = json.loads(event['body'])
        self.__context = context

    def handle(self):
        if 'routeKey' not in self.__event:
            raise ValueError(f'Unknown event: {self.__event}')

        match self.__event:
            case {'routeKey': 'GET /alerts'}:
                api_handler = ListAlerts
            case {'routeKey': 'GET /alerts/{alertId}'}:
                api_handler = GetAlert
            case {'routeKey': 'PUT /alerts'}:
                api_handler = PutAlert
            case {'routeKey': 'POST /alerts/{alertId}'}:
                api_handler = PostAlert
            case {'routeKey': 'DELETE /alerts/{alertId}'}:
                api_handler = DeleteAlert
            case _:
                raise ValueError(f'invalid routeKey: \"{self.__event["routeKey"]}\"')

        print(self.__event)

        api_handler = api_handler(self.__event)
        return api_handler.enact()
