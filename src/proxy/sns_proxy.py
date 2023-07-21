import boto3
import os
from typing import List

from src.model.subscription_config import SubscriptionConfig
from src.model.enum.protocol_type import ProtocolType


class SnsProxy:
    __topic_name_pattern: str = "rec-res-notification-{owner}"
    __arn_pattern: str = "arn:aws:sns:{region}:{account_id}:rec-res-notification-{owner}"
    __aws_region: str
    __aws_account_id: str
    __existing_topic_arns: List[str]
    __existing_topic_arns_is_dirty: bool = False

    def __init__(self):
        self.__sns_resource = boto3.resource("sns")
        self.__sns_client = boto3.client("sns")
        self.__aws_region = os.environ["AWS_REGION"]
        self.__aws_account_id = os.environ["AWS_ACCOUNT_ID"]

    def send_notification(self, owner: str, message: str):
        topic = self.__sns_resource.Topic(
            self.__arn_pattern.format(region=self.__aws_region, account_id=self.__aws_account_id, owner=owner)
        )  # TODO: update
        topic.publish(Subject="Found campground availability", Message=message)

    def topic_exists(self, owner: str):
        owner_topic_arn = self.__get_topic_arn_for_owner(owner)

        all_topics = self.__get_all_topics()

        return owner_topic_arn in all_topics

    def create_topic(self, owner: str):
        self.__sns_client.create_topic(Name=self.__topic_name_pattern.format(owner=owner))
        self.__existing_topic_arns_is_dirty = True

    def create_subscriptions(self, owner: str, subscriptions: List[dict]):
        self.__sns_resource.Topic(self.__get_topic_arn_for_owner(owner))

    def me_is_test(self, asdf, fdsa):
        return asdf + fdsa

    def set_topic_subscriptions_for_owner(self, owner: str, subscriptions: List[SubscriptionConfig]):
        owner_topic_arn = self.__get_topic_arn_for_owner(owner)
        list_subscriptions_response = self.__sns_client.list_subscriptions_by_topic(TopicArn=owner_topic_arn)

        subscriptions_dict = {}
        for sub in subscriptions:
            subscriptions_dict[sub.endpoint] = sub.protocol_type

        # remove any old subscriptions
        existing_subscriptions_dict = {}
        for existing_subscription in list_subscriptions_response["Subscriptions"]:
            if (
                existing_subscription["Endpoint"] not in subscriptions_dict
                and existing_subscription["SubscriptionArn"] != "PendingConfirmation"
            ):
                self.__sns_client.unsubscribe(SubscriptionArn=existing_subscription["SubscriptionArn"])
            else:
                existing_subscriptions_dict[existing_subscription["Endpoint"]] = existing_subscription["Protocol"]

        # create any new subscriptions
        for endpoint, protocol in subscriptions_dict.items():
            if protocol != ProtocolType.EMAIL:
                print(f"Unsupported ProtocolType [{protocol}] in user config for owner [{owner}")
                continue

            if endpoint not in existing_subscriptions_dict:
                self.__sns_client.subscribe(TopicArn=owner_topic_arn, Protocol=protocol.value, Endpoint=endpoint)

    def __get_all_topics(self) -> List[str]:
        if (
            self.__existing_topic_arns is not None
            and len(self.__existing_topic_arns) > 0
            and not self.__existing_topic_arns_is_dirty
        ):
            return self.__existing_topic_arns
        topics: List[str] = []
        call_list = True
        next_indicator = ""
        while call_list:
            list_topics_response = self.__sns_client.list_topics(NextToken=next_indicator)
            topics.extend(topic["TopicArn"] for topic in list_topics_response["Topics"])
            if "NextToken" in list_topics_response and list_topics_response["NextToken"]:
                next_indicator = list_topics_response["NextToken"]
            else:
                call_list = False

        self.__existing_topic_arns = topics
        self.__existing_topic_arns_is_dirty = False

        return topics

    def __get_topic_arn_for_owner(self, owner: str) -> str:
        return self.__arn_pattern.format(region=self.__aws_region, account_id=self.__aws_account_id, owner=owner)
