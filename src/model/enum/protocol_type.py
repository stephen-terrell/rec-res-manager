from enum import Enum


class ProtocolType(Enum):
    HTTP = "http"
    HTTPS = "https"
    EMAIL = "email"
    EMAIL_JSON = "email-json"
    SMS = "sms"
    SQS = "sqs"
    APPLICATION = "application"
    LAMBDA = "lambda"
    FIREHOSE = "firehose"
