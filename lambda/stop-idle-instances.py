# File: stop_idle_instances.py
# This Lambda function stops EC2 instances that have been running for more than 24 hours.

import boto3
import logging
from datetime import datetime, timezone, timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    threshold_time = datetime.now(timezone.utc) - timedelta(hours=24)

    response = ec2.describe_instances(Filters=[
        {'Name': 'instance-state-name', 'Values': ['running']}
    ])

    stopped_instances = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            launch_time = instance['LaunchTime']

            # Stop if running for more than 24 hours
            if launch_time < threshold_time:
                ec2.stop_instances(InstanceIds=[instance_id])
                logger.info(f"Stopped idle instance: {instance_id}")
                stopped_instances.append(instance_id)

    if not stopped_instances:
        logger.info("No idle EC2 instances found.")
    return {
        'statusCode': 200,
        'stoppedInstances': stopped_instances
    }
