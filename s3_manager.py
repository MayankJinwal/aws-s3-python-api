from dotenv import load_dotenv
import boto3

load_dotenv()
s3_client = boto3.client('s3')

response = s3_client.list_buckets()

print(response)
