# File: release_unused_eips.py

import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    try:
        # Describe all allocated EIPs
        response = ec2.describe_addresses()
        addresses = response['Addresses']

        released_ips = []

        for address in addresses:
            public_ip = address.get('PublicIp')
            allocation_id = address.get('AllocationId')
            instance_id = address.get('InstanceId', None)
            network_interface_id = address.get('NetworkInterfaceId', None)

            # Check if not associated with any resource
            if not instance_id and not network_interface_id:
                ec2.release_address(AllocationId=allocation_id)
                logger.info(f"Released unused EIP: {public_ip}")
                released_ips.append(public_ip)

        if not released_ips:
            logger.info("No unused Elastic IPs to release.")
        return {
            'statusCode': 200,
            'releasedIPs': released_ips
        }

    except Exception as e:
        logger.error(f"Failed to release EIPs: {str(e)}")
        return {
            'statusCode': 500,
            'error': str(e)
        }
