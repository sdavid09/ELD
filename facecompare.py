import boto3

BUCKET = "amazon-rekognition"
KEY_SOURCE = "test.jpg"
KEY_TARGET = "test2.jpg"
ACCESS_ID = 'AKIAJJWO4E6N6SOHE47A'
ACCESS_KEY = 'i+3gHE63hRyMyaJyZVn0SgoLlz7xvmnNxdU4ktem'

def compare_faces(bucket, key, bucket_target, key_target, threshold=80, region="us-east-1"):
    #rekognition = boto3.client("rekognition", region)
    rekognition = boto3.client("rekognition",region, aws_access_key_id=ACCESS_ID, aws_secret_access_key=ACCESS_KEY)
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
                "Name": key_target,
            }
        },
        SimilarityThreshold=threshold,
    )
    return response['SourceImageFace'], response['FaceMatches']


source_face, matches = compare_faces(BUCKET, KEY_SOURCE, BUCKET, KEY_TARGET)

# the main source face
print "Source Face ({Confidence}%)".format(**source_face)

# one match for each target face
for match in matches:
    print "Target Face ({Confidence}%)".format(**match['Face'])
    print "  Similarity : {}%".format(match['Similarity'])

"""
    Expected output:
    
    Source Face (99.945602417%)
    Target Face (99.9963378906%)
      Similarity : 89.0%

"""
