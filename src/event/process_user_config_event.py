import json
import os
from dataclasses import dataclass
from typing import List

from src.model.enum.protocol_type import ProtocolType
from src.model.subscription_config import SubscriptionConfig
from src.proxy.code_pipeline_proxy import CodePipelineProxy
from src.proxy.s3_proxy import S3Proxy
from src.proxy.sns_proxy import SnsProxy


@dataclass
class ProcessUserConfigEvent:
    event: dict
    context: dict

    __code_pipeline_proxy: CodePipelineProxy
    __s3_proxy: S3Proxy
    __sns_proxy: SnsProxy
    __config_bucket_name: str
    __job_id: str
    __config_name = "user-config/user-config.json"

    def __init__(self, event: dict, context: dict):
        self.event = event
        self.context = context
        self.__code_pipeline_proxy = CodePipelineProxy()
        self.__s3_proxy = S3Proxy()
        self.__sns_proxy = SnsProxy()
        self.__config_bucket_name = os.environ["CONFIG_BUCKET_NAME"]

        if "CodePipeline.job" in self.event and "id" in self.event["CodePipeline.job"]:
            self.__job_id = self.event["CodePipeline.job"]["id"]
        else:
            print("no codepipeline job id found in event. likely running a test")

    def handle(self):
        config_object = self.__s3_proxy.get_object(self.__config_bucket_name, self.__config_name)
        if config_object is None:
            failure_message = (
                f"Could not find user config file [{self.__config_name}] in bucket [{self.__config_bucket_name}]"
            )
            print(failure_message)
            if self.__job_id:
                self.__code_pipeline_proxy.report_job_failure(self.__job_id, failure_message)
        config = json.loads(config_object["Body"].read().decode("utf-8"))

        for user_config in config["userConfigs"]:
            owner = user_config["owner"]

            if not self.__sns_proxy.topic_exists(owner):
                self.__sns_proxy.create_topic(owner)

            self.__sns_proxy.set_topic_subscriptions_for_owner(
                owner, self.__get_user_subscriptions(user_config["subscriptions"])
            )

        if self.__job_id:
            self.__code_pipeline_proxy.report_job_success(self.__job_id)

    @staticmethod
    def __get_user_subscriptions(subs: List[dict]) -> List[SubscriptionConfig]:
        return [
            SubscriptionConfig(endpoint=sub["endpoint"], protocol_type=ProtocolType(sub["protocol"])) for sub in subs
        ]
