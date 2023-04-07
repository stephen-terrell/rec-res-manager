import json
import os

from src.proxy.s3_proxy import S3Proxy


class ListAlerts:

    def enact(self, event):
        user_id: str = event['pathParameters']['userId']
        s3 = S3Proxy()
        config_object = s3.get_object(os.environ['USER_CONFIG_BUCKET_NAME'], 'user-config-v2.json')

        body = config_object['Body']
        stream = body.read()
        decode = stream.decode('utf-8')
        user_config = json.loads(decode)

        user_alert_configs: dict = user_config['userConfigs'][user_id]['alertConfigs']

        result = [{
            'userId': user_id,
            'alertId': key,
            'type': value['type'],
            'campgroundId': value['campgroundId'],
            'checkInDate': value['checkInDate'],
            'checkOutDate': value['checkOutDate'],
            'notificationPreferences': {
                **value['notificationPreferences']
            }
        } for key, value in user_alert_configs.items()]

        return result
