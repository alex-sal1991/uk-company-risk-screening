from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from pathlib import Path
import os


load_dotenv()

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

if connection_string is None:
    raise ValueError("No storage connection string")

service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = service_client.get_container_client("bronze")

bronze_path_files = list(Path("data/bronze").rglob("*.json"))
total = len(bronze_path_files)

count = 0
for file in bronze_path_files:
    blob_file = file.relative_to("data/bronze").as_posix()
    with open(file, "rb") as f:
        container_client.upload_blob(name=blob_file, data=f, overwrite=True)
    
    count += 1
    if count % 500 == 0:
        print(f"{count} out of {total} files.")

print(f"Done: {count} out of {total} files uploaded.")

    


