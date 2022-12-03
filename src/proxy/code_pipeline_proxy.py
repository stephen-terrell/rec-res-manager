import boto3


class CodePipelineProxy:
    __code_pipeline_client = None

    def __init__(self):
        self.__code_pipeline_client = boto3.client('codepipeline')

    def report_job_failure(self, job_id: str, failure_message: str):
        self.__code_pipeline_client.put_job_failure_result(
            jobId=job_id,
            failureDetails={
                'type': 'ConfigurationError',
                'message': failure_message
            }
        )

    def report_job_success(self, job_id: str):
        self.__code_pipeline_client.put_job_success_result(jobId=job_id)
