import os
import boto3

# Initialize MinIO client
s3 = boto3.client(
    's3',
    endpoint_url="http://4.222.216.225:9000",
    aws_access_key_id="",
    aws_secret_access_key=""
)

bucket = "communityhealthdata"
local_dir = "/home/gatitu/communityhealthdata"

for file in os.listdir(local_dir):
    if file.endswith(".csv"):
        file_path = os.path.join(local_dir, file)
        s3.upload_file(file_path, bucket, file)
        print(f"Uploaded {file}")
