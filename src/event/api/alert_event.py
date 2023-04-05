from dataclasses import dataclass


@dataclass
class AlertEvent:
    event: dict
    context: dict

    def __init__(self,  event: dict, context: dict):
        self.event = event
        self.context = context

    def handle(self):
        print(self.event)

        result = {'hello': 'world'}
        if 'pathParameters' in self.event and 'user' in self.event['pathParameters']:
            result['user'] = self.event['pathParameters']['user']
        return result
