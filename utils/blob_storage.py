import json
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


def get_blob_client():
    account_url = "https://merakiconfigbackupappore.blob.core.windows.net"
    default_credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)
    return blob_service_client


def create_container(blob_service_client, container_name):
    container_client = blob_service_client.get_container_client(container=container_name)
    if not container_client:
        print(container_name)
        container_client = blob_service_client.create_container(container_name)
    return container_client


def dump_data(file_location, data):
    blob_client = get_blob_client()
    container_name = 'config-output'
    container_client = create_container(blob_client, container_name)
    upload_blob(container_client, file_location, data)


def upload_blob(container_client, file_location, data):
    container_client.upload_blob(name=file_location, data=json.dumps(data))
