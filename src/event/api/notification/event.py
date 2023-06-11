from src.event.api.notification.v1.delete import DeleteNotification
from src.event.api.notification.v1.list import ListNotifications
from src.event.api.notification.v1.put import PutNotification
from dataclasses import dataclass
import json


@dataclass
class NotificationEvent:
    __event: dict
    __context: dict

    def __init__(self, event: dict, context: dict):
        self.__event = event
        if "body" in event:
            # request body is just a string, so you need to parse it
            self.__event["body"] = json.loads(event["body"])
        self.__context = context

    def handle(self):
        if "routeKey" not in self.__event:
            raise ValueError(f"Unknown event: {self.__event}")

        match self.__event:
            case {"routeKey": "GET /notifications"}:
                api_handler = ListNotifications
            case {"routeKey": "PUT /notifications"}:
                api_handler = PutNotification
            case {"routeKey": "DELETE /notifications/{notificationId}"}:
                api_handler = DeleteNotification
            case _:
                print(self.__event)
                raise ValueError(f'invalid routeKey: "{self.__event["routeKey"]}"')

        print(self.__event)

        return api_handler(self.__event).enact()
