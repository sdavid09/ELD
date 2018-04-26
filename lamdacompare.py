import boto3
from decimal import Decimal
import json
import urllib

print('Loading function')

#dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')


# --------------- Helper Functions ------------------

def index_faces(bucket, key, key2):

    response = rekognition.compare_faces(
        SourceImage={
            "S3Object": {
                "Bucket": 'eldimage',
                "Name": key,
            }
        },
        TargetImage={
            "S3Object": {
                "Bucket": 'eldimage',
                "Name": key2,
            }
        },
        SimilarityThreshold=80,
    )
    return response['SourceImageFace'], response['FaceMatches']

# --------------- Main handler ------------------

def lambda_handler(event, context):

    # Get the object from the event
    bucket = 'eldimage'
    key = 'test.jpg'
    key2 ='test2.jpg'
    #bucket = event['Records'][0]['s3']['bucket']['name']
    #key= event['Records'][0]['s3']['object']['key']
    try:

        # Calls Amazon Rekognition IndexFaces API to detect faces in S3 object 
        # to index faces into specified collection
        
        response = index_faces(bucket, key, key2)
        
        # Commit faceId and full name object metadata to DynamoDB
        
   

        # Print response to console
        print(response)

        return response
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket))
        raise e
