import boto3
from decimal import Decimal
import json
import urllib
import pprint

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
        
        #response = index_faces(bucket, key, key2)
        
        # Commit faceId and full name object metadata to DynamoDB
        
   

        # Print response to console
       # if response[1][0]['Similarity'] > 90 :# print only similarity 
       #     print "MATCH!"   # 
       
       
        imgs=[]
        val=[]
        s3 = boto3.resource('s3')
        for bucket in s3.buckets.all():
            for obj in bucket.objects.filter(Prefix='Building/entrance/img_entering/'):
                imgs.append(obj.key)
      
        imgs.remove("Building/entrance/img_entering/") # remove home path so face comparison wont try to compare
        #val = imgs[:]
        #print imgs # list of all keys
       # filter(lambda x: response[1][0]['Similarity'] > 90)
        val = list( map ( lambda x: x.encode('utf8'), imgs)) # convert list of unicode to string
        for x in val:
            response = index_faces('eldimage', 'test.jpg', x)
            print response
            try:
                if response[1][0]['Similarity'] > 90 :# print only similarity 
                    print "MATCH!" 
            except:
                print "NOT MATCH!"# 
       
        
        #return response
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket))
        raise e
