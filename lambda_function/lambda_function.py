import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sagemaker_client = boto3.client('sagemaker-runtime')

def lambda_handler(event, context):
    endpoint_name = os.environ['SAGEMAKER_ENDPOINT_NAME']
    payload = event.get("body", "{}")

    try:
        logger.info(f"Invoking SageMaker endpoint: {endpoint_name} with payload: {payload}")
        response = sagemaker_client.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType='application/json',
            Body=payload
        )
        result = response['Body'].read().decode('utf-8')
        logger.info(f"SageMaker response: {result}")

        return {
            'statusCode': 200,
            'body': result
        }

    except Exception as e:
        logger.error(f"Error invoking SageMaker endpoint: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'body': f"Error invoking SageMaker: {str(e)}"
        }

