#!/usr/bin/python


import boto3
import pymysql

#config file for rds credentials
db_username = "eldunt"
db_password = "untace2018"
db_name = "elddb"
db_endpoint = "eldinstance.cv9eiidzvrjf.us-east-1.rds.amazonaws.com"

s3 = boto3.resource('s3')

buckets = ['eldimageentering', 'eldimageinside', 'eldimageexiting', 'eldimage']
for buck in buckets: # loops through list of buckets defined and deletes files
    my_bucket = s3.Bucket(buck)
    for img in my_bucket.objects.all():
        img.delete()
#for bucket in s3.buckets.all():
#    print bucket.name

try:
    db = pymysql.connect(host=db_endpoint, user=db_username, port=3306, db=db_name, passwd=db_password)
except Exception as e:
    print e

con = db.cursor()

tables = ["image_inside", "main_door", "room2_mic", "room1_mic","RM_1", "RM_2", "rm2_thermal", "rm1_thermal"]
# delete all tables in mysql
try:
    for tab in tables:
        con.execute("DELETE FROM {}".format(tab))
        db.commit()
except Exception as e:
    print e
    db.rollback()
