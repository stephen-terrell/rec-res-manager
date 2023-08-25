import json
import os
from typing import List

from src.factory.reservation_config_factory import ReservationConfigFactory
from src.model.reservation_config import ReservationConfigV1
from src.proxy.s3_proxy import S3Proxy


class UserConfigProvider:
    reservation_config_factory: ReservationConfigFactory
    s3_proxy: S3Proxy
    __user_config_bucket_name: str
    __user_config_key_name: str

    def __init__(self):
        self.reservation_config_factory = ReservationConfigFactory()
        self.s3_proxy = S3Proxy()
        self.__user_config_bucket_name = os.environ["USER_CONFIG_BUCKET_NAME"]
        self.__user_config_key_name = "user-config-v2.json"

    def get_user_configs(self) -> List[ReservationConfigV1]:
        result = []

        for config in camp_configs:
            result.append(self.reservation_config_factory.get_reservation_config(user_config=config))

        return result

    def get_v2_user_config(self) -> dict:
        default: dict = {"userConfigs": {}}
        get_object_result = self.s3_proxy.get_object(self.__user_config_bucket_name, self.__user_config_key_name)

        if get_object_result is None or "Body" not in get_object_result:
            return default

        decoded_result = get_object_result["Body"].read().decode("utf-8")

        if decoded_result == "" or decoded_result == "{}":
            return default

        return json.loads(decoded_result)

    def update_v2_user_config(self, config: dict):
        self.s3_proxy.put_object(
            self.__user_config_bucket_name,
            self.__user_config_key_name,
            json.dumps(config),
        )


camp_configs = [
    {
        "owner": "carly-stephen",
        "version": 1,
        "subscribers": [
            "something@gmail.com",
        ],
        "autoBookCredentials": {
            "enc": "",
        },
        "campgrounds": [
            {
                "campgroundId": "247663",  # Signal Mtn
                "checkInDate": "08/16/2023",
                "checkOutDate": "08/18/2023",
                "allowRvLikeSites": True,
                "notificationPreferences": {
                    "notificationsEnabled": True,
                    "notificationSensitivityLevel": "ANY_DAYS_AVAILABLE",
                },
                "autoBookPreferences": {
                    "attemptAutoBook": True,
                    "autoBookSensitivityLevel": "ALL_DAYS_AVAILABLE",
                },
            },
            {
                "campgroundId": "10132033",  # Bishop Park
                "checkInDate": "08/10/2023",
                "checkOutDate": "08/11/2023",
                "allowRvLikeSites": True,
                "notificationPreferences": {
                    "notificationsEnabled": True,
                    "notificationSensitivityLevel": "ANY_DAYS_AVAILABLE",
                },
                "autoBookPreferences": {
                    "attemptAutoBook": True,
                    "autoBookSensitivityLevel": "ALL_DAYS_AVAILABLE",
                },
            },
        ],
        "permits": [
            {
                "coming": "soon",
            },
        ],
    },
]
