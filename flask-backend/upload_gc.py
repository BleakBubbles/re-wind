from google.cloud import storage

def upload_to_gc(source_file_path, destination_blob_name):
    # Initialize the Google Cloud Storage client with the credentials
    credentials_file = "/Users/lindsayxie/Documents/API testing/keys.json"
    storage_client = storage.Client.from_service_account_json(credentials_file)

    # Get the target bucket
    bucket_name = "rewind-audio-bucket"
    bucket = storage_client.bucket(bucket_name)

    # Upload the file to the bucket
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_path)

    print(f"File {source_file_path} uploaded to gs://{bucket_name}/{destination_blob_name}")

if __name__ == "__main__":
    # Replace the following variables with your specific values
    SOURCE_FILE_PATH = "/Users/lindsayxie/Documents/API testing/20240127_182854.wav"
    DESTINATION_BLOB_NAME = "20240127_182854.wav"

    upload_to_gc(SOURCE_FILE_PATH, DESTINATION_BLOB_NAME)