#!/usr/bin/env python

import argparse
import mimetypes
import sys
from os import walk
from uuid import uuid4
from time import sleep

import boto3

parser = argparse.ArgumentParser()
parser.add_argument('distribution_id', help='CloudFront distribution ID to invalidate')
args = parser.parse_args()

BUCKET = 'juicemia.com'

bucket = boto3.resource('s3', region_name='us-east-1').Bucket(BUCKET)
cf_client = boto3.client('cloudfront')

def guess_mime(path):
    first_try = mimetypes.guess_type(path)[0]

    if first_try is not None:
        return first_try

    # Here we catch cases that mimetypes.guess_type has trouble with.
    suffix = path.split('.')[-1]
    if suffix == 'woff2':
        return 'binary/octet-streams'

    return 'binary/octet-stream'

for root, dirs, files in walk('www'):
    for file in files:
        path = '{}/{}'.format(root, file)
        key = path[4:]

        print('uploading {} to {}...'.format(path, key))
        with open(path, 'rb') as f:
            bucket.put_object(Key=key, Body=f, ContentType=guess_mime(path))

print('invalidating cloudfront...')
invalidation = cf_client.create_invalidation(
    DistributionId=args.distribution_id,
    InvalidationBatch={
        'Paths': {
            'Quantity': 1,
            'Items': ['/*']
        },
        'CallerReference': uuid4().hex
    }
)['Invalidation']

dots = 1
while invalidation['Status'] != 'Completed':
    print('invalidation {} is in progress{}  '.format(invalidation['Id'], '.' * dots), end='\r')

    invalidation = cf_client.get_invalidation(
        Id=invalidation['Id'],
        DistributionId=args.distribution_id
    )['Invalidation']

    dots = (dots % 3) + 1
    sleep(2)

# This moves the output to a new line, because the last print ended with a carriage return instead of a newline.
# The same character needs to be printed out if not it'll change on the same line before moving to the next one.
print('i')
print('invalidation {} is completed!'.format(invalidation['Id']))
sys.exit(0)
