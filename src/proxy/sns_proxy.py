import boto3


class SnsProxy:
    __sns_resource = None
    __arn_pattern = 'arn:aws:sns:us-west-2:379689532145:rec-res-notification-{owner}'

    def __init__(self):
        self.__sns_resource = boto3.resource('sns')

    def send_notification(self, owner: str, message: str):
        topic = self.__sns_resource.Topic(self.__arn_pattern.format(owner=owner))
        topic.publish(
            Subject='Found campground availability',
            Message=message
        )
