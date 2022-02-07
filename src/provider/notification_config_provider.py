import json

from src.proxy.s3_proxy import S3Proxy


class NotificationConfigProvider:
    __config = None
    __s3_proxy: S3Proxy
    __config_bucket_name: str
    __config_key = '/notification/config.json'

    def __init__(self):
        self.__s3_proxy = S3Proxy()

    def get_notification_config(self) -> dict:
        if self.__config is not None:
            return self.__config

        config_object = self.__s3_proxy.get_object(self.__config_bucket_name, self.__config_key)

        config = json.loads(config_object['Body'].read().decode('utf-8'))

        self.__config = config

        return config

    def update_notification_config(self, update_config: dict):
        current_config = self.get_notification_config()

        for owner, owner_update_config in update_config.items():
            if owner not in current_config:
                current_config[owner] = owner_update_config
            else:
                for campground_id, campground_update_config in owner_update_config.items():
                    if campground_id not in current_config[owner]:
                        current_config[owner][campground_id] = campground_update_config
                    else:
                        for campsite_id, campsite_update_config in campground_update_config.items():
                            current_config[owner][campground_id][campsite_id] = campsite_update_config

        self.__s3_proxy.put_object(self.__config_bucket_name, self.__config_key, json.dumps(current_config))


test_config = {
    'carly-stephen': {
        '232279': {
            '10082193': {
                '2022-02-11': 'Available',
                '2022-02-12': 'Available'
            },
            '86302': {
                '2022-02-11': 'Available',
                '2022-02-12': 'Available'
            },
            '86910': {
                '2022-02-11': 'Available',
                '2022-02-12': 'Reserved'
            },
            '87127': {
                '2022-02-11': 'Reserved',
                '2022-02-12': 'Available'
            },
            '87130': {
                '2022-02-11': 'Available',
                '2022-02-12': 'Reserved'
            },
            '87181': {
                '2022-02-11': 'Available',
                '2022-02-12': 'Reserved'
            },
            '87288': {
                '2022-02-11': 'Available',
                '2022-02-12': 'Reserved'
            },
            '87366': {
                '2022-02-11': 'Available',
                '2022-02-12': 'Available'
            },
            '87495': {
                '2022-02-11': 'Available',
                '2022-02-12': 'Available'
            },
            '87519': {
                '2022-02-11': 'Available',
                '2022-02-12': 'Available'
            },
            '87844': {
                '2022-02-11': 'Available',
                '2022-02-12': 'Reserved'
            },
        }
    }
}