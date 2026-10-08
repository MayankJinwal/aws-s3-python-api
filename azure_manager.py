import os
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()
res = os.getenv('AZURE_CONNECTION_STRING')

blob_service_client = BlobServiceClient.from_connection_string(res)
#blob_service_client.create_container(name="mayank-test-container")
try:
    blob_service_client.create_container(name="mayank-test-container")
except ResourceExistsError:
    print("Container already exists, skipping creation.")

blob_client = blob_service_client.get_blob_client(container="mayank-test-container", blob="sample.txt")

with open("sample.txt", "rb") as data:
    # yahan upload call aayegi
        blob_client.upload_blob(data, overwrite=True)
        print("Uploaded sample.txt successfully!")

containers = blob_service_client.list_containers()


container_client = blob_service_client.get_container_client("mayank-test-container")
blobs = container_client.list_blobs()

for b in blobs:
    print("Found blob:", b.name, b.size)

for c in containers:
    print(c['name'])

download_stream = blob_client.download_blob()
content = download_stream.readall().decode('utf-8')
print("Downloaded content:", content)