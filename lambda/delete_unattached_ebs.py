# File: delete_unattached_ebs.py
# This script deletes unattached EBS volumes in AWS

import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    response = ec2.describe_volumes(Filters=[
        {'Name': 'status', 'Values': ['available']}
    ])

    deleted_volumes = []

    for volume in response['Volumes']:
        volume_id = volume['VolumeId']
        try:
            ec2.delete_volume(VolumeId=volume_id)
            logger.info(f"Deleted unattached EBS volume: {volume_id}")
            deleted_volumes.append(volume_id)
        except Exception as e:
            logger.error(f"Failed to delete volume {volume_id}: {str(e)}")

    if not deleted_volumes:
        logger.info("No unattached EBS volumes found.")
    return {
        'statusCode': 200,
        'deletedVolumes': deleted_volumes
    }
