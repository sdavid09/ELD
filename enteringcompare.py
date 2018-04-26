import boto3
from decimal import Decimal
import json
import urllib
import pprint

print('Loading function')


s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')

s3_res = boto3.resource('s3')

my_bucket = s3_res.Bucket('eldimageentering')

#for file in my_bucket.objects.all():
#    print file.key
# --------------- Helper Functions ------------------

def index_faces(bucket, bucket2, key, key2):

    response = rekognition.compare_faces(
        SourceImage={
            "S3Object": {
                "Bucket": bucket,
                "Name": key,
            }
        },
        TargetImage={
            "S3Object": {
                "Bucket": bucket2,
                "Name": key2,
            }
        },
        SimilarityThreshold=80,
    )
    return response['SourceImageFace'], response['FaceMatches']

# --------------- Main handler ------------------

def lambda_handler(event, context):

    # Get the object from the event
    bucket = 'eldimageentering'
    bucket2 = 'eldimageinside'
    #key = 'test.jpg'
    #key2 ='test2.jpg'
    cur_bucket = event['Records'][0]['s3']['bucket']['name'].encode('utf8')
    #key= event['Records'][0]['s3']['object']['key']
    key = event['Records'][0]['s3']['object']['key'].encode('utf8')
    
    #print bucket
   
    try:

        # Calls Amazon Rekognition IndexFaces API to detect faces in S3 object 
        # to index faces into specified collection
        
        #response = index_faces(bucket, key, key2)
        
        # Commit faceId and full name object metadata to DynamoDB
        
   

        # Print response to console
 
        #s3 = boto3.resource('s3')
       
        imgs=[]

        my_bucket = s3_res.Bucket('eldimageinside')
        for file in my_bucket.objects.all():
            imgs.append(file.key)
            
            #print file.key
           
        if len(imgs) == 0: # check if anything is inside else, add first image 
            print "NOTHING INSIDE INSIDE , ADDING FIRST IMAGE"
            
            copy_source = {
                'Bucket': 'eldimageentering',
                'Key': key
                }
            s3_res.meta.client.copy(copy_source, 'eldimageinside', copy_source['Key'])
            return
    
        s3 = boto3.resource('s3')
        #for bucket in s3.buckets.all():
        #    for obj in bucket.objects.filter(Prefix='Building/entrance/img_entering/'):
        #        imgs.append(obj.key)
      
        #imgs.remove("Building/entrance/img_entering/") # remove home path so face comparison wont try to compare
        #print imgs # list of all keys
        flag = 0 
        val = list( map ( lambda x: x.encode('utf8'), imgs)) # convert list of unicode to string
        for x in val:
        #    print x
        #    #print (cur_bucket, bucket2, key, x)
            print x
            print key
            response = index_faces('eldimageentering', 'eldimageinside', key, x)
            print response
        #    flag = 0
        #    #response = "TEST"
        #    print response
            try:
                
                    if response[1][0]['Similarity'] > 70 :# print only similarity 
                        flag =1
                        print "MATCH!"
                        break
        #            print "MATCH!" 
            except:
                print "NOT MATCH!"# 
        if flag == 0:
            copy_source = {
                'Bucket': 'eldimageentering',
                'Key': key
                }
            s3_res.meta.client.copy(copy_source, 'eldimageinside', copy_source['Key'])
                #print "MATCH!" 
            #else:
               # print "NOT MATCH!"# 
            
       
        
        #return response
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket))
        raise e
