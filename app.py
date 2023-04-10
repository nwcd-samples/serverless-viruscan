import re
import os
import sys
import json
import boto3
import subprocess


def download_scan_object(region, bucket, key):
    try:
        # download object from s3
        s3 = boto3.client('s3', region_name=region)
        with open('/tmp/temp_file', 'wb') as data:
            s3.download_fileobj(bucket, key, data)

        print("file downloaded")
        # scaning
        pipe = subprocess.Popen('clamscan /tmp/temp_file', shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print("file scaning")
        scan_result = pipe.stdout.read().decode()
        # update object tag
        TagValue = 'Scaning'
        result = re.search('Infected files: 1', scan_result)
        print(scan_result)
        if result is not None:
            TagValue = 'Infected'
        else:
            TagValue = 'Not Infected'
        s3.put_object_tagging(Bucket=bucket,
                              Key=key,
                              Tagging={
                                  'TagSet': [{'Key': 'Clamav scan result', 'Value': TagValue}]
                              })
        print("scan task finished")
        return TagValue
    except Exception as e:
        print(str(e))
        return None


def handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        download_scan_object("ap-northeast-1", bucket, key)
