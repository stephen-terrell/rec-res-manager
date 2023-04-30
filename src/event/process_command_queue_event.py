import json

from src.command.api.alert.v1.create import CreateAlert
from src.command.api.alert.v1.delete import DeleteAlert
from src.command.api.alert.v1.update import UpdateAlert
from src.provider.user_config_provider import UserConfigProvider
from src.proxy.sqs_proxy import SqsProxy


class ProcessCommandQueueEvent:
    __user_config_provider: UserConfigProvider

    def __init__(self, event: dict, context: dict):
        self._event = event
        self._context = context

        self._user_config_provider = UserConfigProvider()
        self._sqs_proxy = SqsProxy()

        self._handler_map = {
            "CREATE_ALERT": CreateAlert.handle_command,
            "DELETE_ALERT": DeleteAlert.handle_command,
            "UPDATE_ALERT": UpdateAlert.handle_command,
        }

    def handle(self):
        print(self._event)

        user_config = self._user_config_provider.get_v2_user_config()
        receipt_handles = []

        for record in self._event["Records"]:
            body = json.loads(record["body"])
            receipt_handles.append(record["receiptHandle"])

            command_name = body["commandName"]
            if command_name not in self._handler_map:
                print(f'unsupported commandName: {body["commandName"]}')
                print(record)
                continue

            user_config = self._handler_map[command_name](user_config, body["data"])

        self._user_config_provider.update_v2_user_config(user_config)
        self._sqs_proxy.delete_api_command_messages(receipt_handles)

        return user_config
