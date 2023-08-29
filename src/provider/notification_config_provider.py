import json
import os

from src.proxy.s3_proxy import S3Proxy


class NotificationConfigProvider:
    __config = None
    __v2_config = None
    __s3_proxy: S3Proxy
    __config_bucket_name: str
    __config_key = "notification/config.json"
    __v2_config_key = "notification/config-v2.json"

    def __init__(self):
        self.__s3_proxy = S3Proxy()
        self.__config_bucket_name = os.environ["USER_CONFIG_BUCKET_NAME"]

    def get_notification_config(self) -> dict:
        if self.__config is not None:
            return self.__config

        config_object = self.__s3_proxy.get_object(self.__config_bucket_name, self.__config_key)
        if config_object is None:
            return {}

        config = json.loads(config_object["Body"].read().decode("utf-8"))

        self.__config = config

        return config

    # TODO: unit test
    def get_v2_notification_config(self) -> dict:
        if self.__v2_config is not None:
            return self.__v2_config

        config_object = self.__s3_proxy.get_object(self.__config_bucket_name, self.__v2_config_key)
        if config_object is None:
            return {}

        config = json.loads(config_object["Body"].read().decode("utf-8"))

        self.__v2_config = config

        return config

    # TODO: probably just update this to always overwrite the campground dict for a user
    # TODO: unit test
    def update_v2_notification_config(self, update_config: dict):
        current_config = self.get_v2_notification_config()

        for owner, owner_update_config in update_config.items():
            if owner not in current_config:
                current_config[owner] = {}
            for campground_id, available_campsites in owner_update_config.items():
                if campground_id not in current_config[owner]:
                    current_config[owner][campground_id] = {}
                for campsite_availability in available_campsites:
                    current_config[owner][campground_id][
                        campsite_availability.campsite_id
                    ] = campsite_availability.availabilities

        self.__s3_proxy.put_object(self.__config_bucket_name, self.__v2_config_key, json.dumps(current_config))

    def update_notification_config(self, update_config: dict):
        current_config = self.get_notification_config()

        for owner, owner_update_config in update_config.items():
            if owner not in current_config:
                current_config[owner] = owner_update_config
            else:
                for (
                    campground_id,
                    campground_update_config,
                ) in owner_update_config.items():
                    if campground_id not in current_config[owner]:
                        current_config[owner][campground_id] = campground_update_config
                    else:
                        for (
                            campsite_id,
                            campsite_update_config,
                        ) in campground_update_config.items():
                            current_config[owner][campground_id][campsite_id] = campsite_update_config

        self.__s3_proxy.put_object(self.__config_bucket_name, self.__config_key, json.dumps(current_config))
