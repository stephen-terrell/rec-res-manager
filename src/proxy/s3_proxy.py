import boto3
from botocore.exceptions import ClientError


class S3Proxy:
    __s3_client = boto3.client("s3")

    def get_object(self, bucket_name: str, key: str):
        try:
            return self.__s3_client.get_object(Bucket=bucket_name, Key=key)
        except ClientError as ex:
            if ex.response["Error"]["Code"] == "NoSuchKey":
                return None
            else:
                raise ex

    def put_object(self, bucket_name: str, key: str, object_data: str):
        self.__s3_client.put_object(Bucket=bucket_name, Key=key, Body=object_data)
