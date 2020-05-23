from google.cloud import storage


def upload_to_storage(source_file_name):
    """Uploads a file to the bucket."""
    bucket_name = "car-hire"
    destination_blob_name = "encodings.pickle"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )