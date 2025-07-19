import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Moved client creation into function so it can be mocked
    sagemaker_client = boto3.client('sagemaker-runtime')
    endpoint_name = os.environ.get('SAGEMAKER_ENDPOINT_NAME', 'default-endpoint')
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

# ---------- 🔬 Unit Test (for CI Green Check) ----------
if __name__ == "__main__":
    import unittest
    from unittest.mock import patch, MagicMock
    import json

    class TestLambdaHandler(unittest.TestCase):
        @patch('lambda_function.boto3.client')
        def test_successful_invoke(self, mock_boto_client):
            # Mock the SageMaker response
            mock_response = MagicMock()
            mock_response['Body'].read.return_value = b'{"result": "success"}'

            # Mock client to return the mock response
            mock_client = MagicMock()
            mock_client.invoke_endpoint.return_value = mock_response
            mock_boto_client.return_value = mock_client

            # Set fake env and input
            os.environ['SAGEMAKER_ENDPOINT_NAME'] = 'mock-endpoint'
            event = {"body": json.dumps({"key": "value"})}

            # Call the handler
            response = lambda_handler(event, None)

            # Assert response is mocked, not real
            self.assertEqual(response['statusCode'], 200)
            self.assertIn("success", response['body'])

    unittest.main()

