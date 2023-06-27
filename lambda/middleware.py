import os
from enum import Enum
from typing import Any
import uuid

import boto3


class S3Event(Enum):
    OBJECT_CREATED = "ObjectCreated:Put"


def get_s3_bucket(event) -> str:
    return event["Records"][0]["s3"]["bucket"]["name"]


def get_s3_key(event) -> str:
    return event["Records"][0]["s3"]["object"]["key"]


def get_s3_event_name(event) -> str:
    return event["Records"][0]["eventName"]


def get_job_queue() -> str:
    return os.getenv("JOB_QUEUE", "")


def get_job_definition() -> str:
    return os.getenv("JOB_DEFINITION", "")


def s3_object_creation_handler(event: dict) -> None:
    job_name = f"job-{uuid.uuid4()}"
    bucket_name = get_s3_bucket(event)
    object_key = get_s3_key(event)

    print(
        f"JobName: {job_name} | Bucket: {bucket_name} | Object: {object_key}"
    )

    boto3.client("batch").submit_job(
        jobName=job_name,
        jobQueue=get_job_queue(),
        jobDefinition=get_job_definition(),
        containerOverrides={
            "environment": [
                {"name": "BUCKET_NAME", "value": bucket_name},
                {"name": "OBJECT_KEY", "value": object_key},
            ]
        },
    )


def handler(event: dict, context: Any) -> dict:
    s3_event = get_s3_event_name(event)

    if s3_event == S3Event.OBJECT_CREATED.value:
        s3_object_creation_handler(event)

    return {"statusCode": 200}
