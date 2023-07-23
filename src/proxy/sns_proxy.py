import boto3
import os
from typing import List

from src.model.subscription_config import SubscriptionConfig
from src.model.enum.protocol_type import ProtocolType


class SnsProxy:
    def __init__(self):
        self.__topic_name_pattern: str = "rec-res-notification-{owner}"
        self.__arn_pattern: str = "arn:aws:sns:{region}:{account_id}:rec-res-notification-{owner}"
        self.__sns_resource = boto3.resource("sns")
        self.__sns_client = boto3.client("sns")
        self.__aws_region = os.environ["AWS_REGION"]
        self.__aws_account_id = os.environ["AWS_ACCOUNT_ID"]
        self.__existing_topic_arns: List[str] = []
        self.__existing_topic_arns_is_dirty: bool = False

    def send_notification(self, owner: str, message: str):
        topic = self.__sns_resource.Topic(
            self.__arn_pattern.format(region=self.__aws_region, account_id=self.__aws_account_id, owner=owner)
        )  # TODO: update
        topic.publish(Subject="Found campground availability", Message=message)

    def topic_exists(self, owner: str) -> bool:
        owner_topic_arn = self.__get_topic_arn_for_owner(owner)

        try:
            self.__sns_client.get_topic_attributes(TopicArn=owner_topic_arn)
            return True
        except self.__sns_client.exceptions.NotFoundException:
            return False

    def create_topic(self, owner: str):
        self.__sns_client.create_topic(Name=self.__topic_name_pattern.format(owner=owner))
        self.__existing_topic_arns_is_dirty = True

    def create_subscriptions(self, owner: str, subscriptions: List[dict]):
        self.__sns_resource.Topic(self.__get_topic_arn_for_owner(owner))

    def me_is_test(self, asdf, fdsa):
        return asdf + fdsa

    def create_subscription(self, owner: str, subscription_config: SubscriptionConfig) -> str:
        if subscription_config.protocol_type != ProtocolType.EMAIL:
            raise Exception(f"Unsupported ProtocolType: [{subscription_config.protocol_type}]")

        subscribe_response = self.__sns_client.subscribe(
            TopicArn=self.__get_topic_arn_for_owner(owner),
            Protocol=subscription_config.protocol_type.value,
            Endpoint=subscription_config.endpoint,
            ReturnSubscriptionArn=True,
        )

        return subscribe_response["SubscriptionArn"].split(":")[-1]

    def remove_subscription(self, owner: str, subscription_id):
        topic_arn = self.__get_topic_arn_for_owner(owner)
        subscription_arn = topic_arn + ":" + subscription_id

        self.__sns_client.unsubscribe(SubscriptionArn=subscription_arn)

    def list_subscriptions(self, owner: str) -> List[dict]:
        owner_topic_arn = self.__get_topic_arn_for_owner(owner)
        list_subscriptions_response = self.__sns_client.list_subscriptions_by_topic(TopicArn=owner_topic_arn)

        return list_subscriptions_response["Subscriptions"]

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

    def __get_all_topics(self) -> List[str]:  # TODO: not needed?
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
