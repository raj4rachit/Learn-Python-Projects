import os

import boto3
from botocore.exceptions import NoCredentialsError, ClientError

# Initialize S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY'
)

# Set your bucket name
bucket_name = 'hrmsreactdata'
folder_path = ''
download_dir = 'downloaded_images/'  # Local directory to save downloaded images

# Ensure the local directory exists
if not os.path.exists(download_dir):
    os.makedirs(download_dir)


def download_image(image_key):
    """
    Downloads an image from the S3 bucket.
    :param image_key: The key (path) of the image in the S3 bucket
    """
    try:
        # Create the local file path
        local_file_path = os.path.join(download_dir, os.path.basename(image_key))

        # Download the file from S3
        s3.download_file(bucket_name, image_key, local_file_path)
        print(f"Downloaded {image_key} to {local_file_path}")

    except NoCredentialsError:
        print("Credentials not available.")
    except ClientError as e:
        print(f"Error occurred: {e}")

def delete_image(image_key):
    """
    Deletes an image from the S3 bucket.
    :param image_key: The key (path) of the image in the S3 bucket
    """
    try:
        s3.delete_object(Bucket=bucket_name, Key=image_key)
        print(f"Deleted {image_key} from {bucket_name}")
    except NoCredentialsError:
        print("Credentials not available.")
    except ClientError as e:
        print(f"Error occurred: {e}")

def delete_multiple_images(image_keys):
    """
    Deletes multiple images from the S3 bucket.
    :param image_keys: A list of keys (paths) of images in the S3 bucket
    """
    try:
        delete_response = s3.delete_objects(
            Bucket=bucket_name,
            Delete={
                'Objects': [{'Key': key} for key in image_keys]
            }
        )
        print(f"Deleted {len(delete_response.get('Deleted', []))} images.")
    except NoCredentialsError:
        print("Credentials not available.")
    except ClientError as e:
        print(f"Error occurred: {e}")


def delete_folder(folder_prefix):
    """
    Deletes all objects with the specified prefix (folder) from the S3 bucket.
    :param folder_prefix: The prefix (folder path) of the images in the S3 bucket
    """
    try:
        # List all objects with the specified prefix (folder)
        objects_to_delete = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix)

        if 'Contents' in objects_to_delete:
            delete_response = s3.delete_objects(
                Bucket=bucket_name,
                Delete={
                    'Objects': [{'Key': obj['Key']} for obj in objects_to_delete['Contents']]
                }
            )
            print(f"Deleted {len(delete_response.get('Deleted', []))} objects from {folder_prefix}.")
        else:
            print(f"No objects found in {folder_prefix}")

    except NoCredentialsError:
        print("Credentials not available.")
    except ClientError as e:
        print(f"Error occurred: {e}")

def list_bucket_images():
    """
    List all images in the S3 bucket with common image extensions.
    """
    try:
        # List all objects in the bucket
        response = s3.list_objects_v2(Bucket=bucket_name)

        if 'Contents' in response:
            print("Images in the bucket:")
            for obj in response['Contents']:
                key = obj['Key']
                # Filter based on file extensions
                if key.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                    print(key)
        else:
            print(f"No objects found in bucket {bucket_name}")

    except NoCredentialsError:
        print("Credentials not available.")
    except ClientError as e:
        print(f"Error occurred: {e}")

def list_bucket_images_recursive(folder_path):
    """
    List all images in the S3 bucket recursively (including subfolders).
    """
    try:
        paginator = s3.get_paginator('list_objects_v2')
        if folder_path:
            page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=folder_path)
        else:
            page_iterator = paginator.paginate(Bucket=bucket_name)

        print(f"Images in the bucket '{folder_path}' (including subfolders):")
        for page in page_iterator:
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    # Filter based on common image file extensions
                    if key.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                        print(key)
                        #download_image(key)
                        #delete_image(key)

        # if folder_path:
        #     delete_folder(folder_path)

    except NoCredentialsError:
        print("Credentials not available.")
    except ClientError as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    # # Example: Deleting a single image
    # image_key = 'path/to/your/image.jpg'
    # delete_image(image_key)
    #
    # # Example: Deleting multiple images
    # image_keys = [
    #     'path/to/your/image1.jpg',
    #     'path/to/your/image2.jpg'
    # ]
    # delete_multiple_images(image_keys)
    #
    # # Example: Deleting a folder
    # folder_prefix = 'path/to/your/folder/'
    # delete_folder(folder_prefix)
    #
    # # Example: lis a folder images
    # list_bucket_images()
    folder_path='imagetracking/schedulesoftware.net/2024/01/01/6/'
    list_bucket_images_recursive(folder_path)
