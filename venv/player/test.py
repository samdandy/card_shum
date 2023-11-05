import boto3,os,environ
from django.http import JsonResponse
from django.core.management import settings
from pathlib import Path    
from player.website.funcs import lookup_card

s3 = boto3.client('s3')
env = environ.Env(
    DEBUG=(bool,False)
)


print(lookup_card('Jose Altuve 2011 Topps Houston Astros -auto -autograph PSA 10'))

BASE_DIR = Path(__file__).resolve().parent

environ.Env.read_env(BASE_DIR /'.env')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')

print(AWS_STORAGE_BUCKET_NAME)
# # Specify the S3 bucket name
# bucket_name = 'cardappshum'

# # List objects in the S3 bucket
# objects = s3.list_objects_v2(Bucket=bucket_name)

# # Extract the object keys (file names)
# object_keys = [obj['Key'] for obj in objects.get('Contents', [])]


# def get_s3_object_url(bucket_name, object_key):
#     # Initialize the S3 client using your AWS credentials
#     s3 = boto3.client('s3')

#     # Generate the S3 URL
#     s3_url = s3.generate_presigned_url(
#         ClientMethod='get_object',
#         Params={'Bucket': bucket_name, 'Key': object_key}
#     )
#     s3.close()
#     return s3_url
# matching_values = [x for x in object_keys if x == 'images/mmj.jpg']
# print(get_s3_object_url('cardappshum',str(matching_values)))

