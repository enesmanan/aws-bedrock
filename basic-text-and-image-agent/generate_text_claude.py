import boto3
import json
from botocore.config import Config

# Specify a valid AWS region where Amazon Bedrock is available
region_name = "us-east-1"  # N. Virginia region

# Create a custom configuration
my_config = Config(
    region_name=region_name,
    signature_version='v4',
    retries={
        'max_attempts': 10,
        'mode': 'standard'
    }
)

prompt_data = """
Tell me what you know about Çorum and 
give recommendations for places to visit.
"""

# Create the Bedrock client with the specified region and config
bedrock = boto3.client(service_name="bedrock-runtime", config=my_config)

payload = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 512,
    "messages": [
        {
            "role": "user",
            "content": prompt_data
        }
    ],
    "temperature": 0.8,
    "top_p": 0.8
}

body = json.dumps(payload)
model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

try:
    response = bedrock.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )

    response_body = json.loads(response.get("body").read())
    response_text = response_body['content'][0]['text']
    print(response_text)
except Exception as e:
    print(f"An error occurred: {str(e)}")
