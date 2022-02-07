import boto3


class S3Proxy:
    __s3_client = boto3.client('s3')

    def get_object(self, bucket_name: str, key: str):
        return self.__s3_client.get_object(Bucket=bucket_name, Key=key)

    def put_object(self, bucket_name: str, key: str, object_data: str):
        pass
