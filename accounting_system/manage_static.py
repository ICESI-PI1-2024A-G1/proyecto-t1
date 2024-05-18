import boto3
import os
import environ
import mimetypes

from settings import BASE_DIR

env = environ.Env()
environ.Env.read_env()

print("Creating S3 client...")

# Creates an S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=env("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=env("AWS_SECRET_ACCESS_KEY"),
)

print("Client created.")

print("Locating bucket...")

# The s3 bucket where you want to upload your static files
bucket_name = "ccsa-accounting-bucket"

# The path to your static files directory
static_files_dir = os.path.join(BASE_DIR, "static")

print("Bucket located.")

cors_configuration = {
    "CORSRules": [
        {
            "AllowedHeaders": ["*"],
            "AllowedMethods": ["GET", "HEAD"],
            "AllowedOrigins": ["*"],
            "ExposeHeaders": [],
        }
    ]
}

# Set the CORS configuration for the bucket
s3.put_bucket_cors(Bucket=bucket_name, CORSConfiguration=cors_configuration)

print("CORS configuration updated successfully.")

print("Uploading files...")

# Walk through the static files directory
for root, dirs, files in os.walk(static_files_dir):
    for file in files:
        # Get the full path to the file
        file_path = os.path.join(root, file)

        # Get the relative path to the file from the static files directory
        s3_key = os.path.relpath(file_path, static_files_dir)

        # Determine the content type of the file
        content_type, _ = mimetypes.guess_type(file_path)
        extra_args = {"ContentType": content_type} if content_type else {}

        # Upload the file to S3
        s3.upload_file(file_path, bucket_name, s3_key, ExtraArgs=extra_args)

print("All files uploaded successfully.")
