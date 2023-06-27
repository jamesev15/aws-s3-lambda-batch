import os
import boto3


def process_s3_event() -> None:
    bucket_name = os.getenv("BUCKET_NAME", "")
    object_key = os.getenv("OBJECT_KEY", "")

    response = boto3.client("s3").get_object(
        Bucket=bucket_name, Key=object_key
    )
    content = response["Body"].read()

    print(f"{bucket_name} - {object_key} | {content}")


if __name__ == "__main__":
    process_s3_event()
