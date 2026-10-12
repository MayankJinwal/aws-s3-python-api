import os
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

class AzureBlobService:
    def __init__(self, connection_string=None):
         if not connection_string:
              connection_string = os.getenv('AZURE_CONNECTION_STRING')
         if not connection_string:
              raise ValueError("Azure connection string not found in arguments or environment variables.")

         self.client = BlobServiceClient.from_connection_string(connection_string)
             
    def create_container(self, container_name):
        try:
            self.client.create_container(name=container_name)
            print(f"Container '{container_name}' created successfully.")
        except ResourceExistsError:
            print(f"Container '{container_name}' already exists, skipping.")

    def upload_file(self, container_name, blob_name, file_path):
        try:
            with open(file_path, "rb") as data:
                blob_client = self.client.get_blob_client(container=container_name, blob=blob_name)
                blob_client.upload_blob(data, overwrite=True)
                print(f"Uploaded '{blob_name}' successfully!")
        except FileNotFoundError:
            print(f"Local file not found: {file_path}")
        except Exception as e:
            print(f"Upload failed: {e}")

    def list_blobs(self, container_name):
        try:
            container_client = self.client.get_container_client(container_name)
            blobs = container_client.list_blobs()

            for b in blobs:
                print(f"name : {b.name}, size :{b.size}")
        except Exception as e:
            print(f"Failed to list blobs: {e}")

    def download_file(self, container_name, blob_name, destination_path):
        try:
            blob_client = self.client.get_blob_client(container=container_name,blob=blob_name)
            download_stream = blob_client.download_blob()
            with open(destination_path, "wb") as file:
                file.write(download_stream.readall())
                print(f"Download Sucessful :{destination_path}")
        except Exception as e:
            print(f"Download Failed {e}")

    def delete_file(self, container_name, blob_name):
        try:
            blob_client = self.client.get_blob_client(container=container_name,blob=blob_name)
            blob_client.delete_blob()
            print(f"Deleted Sucessfully : {blob_name}")
        except Exception as e:
            print(f"File Not Deleted {e}")


if __name__ == "__main__":
    service = AzureBlobService()
    service.create_container("mayank-test-container")
    service.upload_file("mayank-test-container", "sample.txt", "sample.txt")
    service.list_blobs("mayank-test-container")
    service.download_file("mayank-test-container", "sample.txt", "downloaded_sample.txt")
    service.delete_file("mayank-test-container", "sample.txt")
