import json
import boto3
import os

# Get SageMaker endpoint name from environment variable
ENDPOINT_NAME = os.environ.get("SAGEMAKER_ENDPOINT_NAME", "my-sagemaker-endpoint")

def lambda_handler(event, context):
    # Example payload you might send
    payload = {
        "instances": [[1.0, 2.0, 3.0]]
    }

    # Convert payload to JSON string
    payload_str = json.dumps(payload)

    # Create SageMaker runtime client
    runtime = boto3.client("sagemaker-runtime")

    # Invoke endpoint
    response = runtime.invoke_endpoint(
        EndpointName=ENDPOINT_NAME,
        ContentType="application/json",
        Body=payload_str
    )

    # Read response body
    result = response["Body"].read().decode("utf-8")

    # Log or return
    print("SageMaker response:", result)
    return {
        "statusCode": 200,
        "body": json.dumps({"result": result})
    }

