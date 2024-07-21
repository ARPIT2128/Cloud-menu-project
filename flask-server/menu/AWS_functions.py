import boto3
import os
from dotenv import load_dotenv


def get_ec2_service(region_name, aws_access_key_id, aws_secret_access_key, service_type='client'):
    """
    Function to create an EC2 client or resource based on the service type.
    """
    if service_type == 'client':
        return boto3.client(
            service_name="ec2",
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
    elif service_type == 'resource':
        return boto3.resource(
            service_name="ec2",
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
    else:
        raise ValueError("Invalid service type. Choose 'client' or 'resource'.")

def terminate_instances(ec2_client, instance_ids):
    """
    Function to terminate EC2 instances.
    """
    response = ec2_client.terminate_instances(
        InstanceIds=instance_ids
    )
    print("Instances Terminated!!!")
    return response

def initiate_instance(ec2_resource, image_id, instance_type, min_count, max_count):
    """
    Function to initiate EC2 instances.
    """
    return ec2_resource.create_instances(
        ImageId=image_id,
        InstanceType=instance_type,
        MinCount=min_count,
        MaxCount=max_count
    )

def Driver_terminate_instances(region_name, aws_access_key_id, aws_secret_access_key, instance_ids):
    """
    Driver function to terminate instances.
    """
    ec2_client = get_ec2_service(region_name, aws_access_key_id, aws_secret_access_key, service_type='client')
    
    # Terminate instances
    response = terminate_instances(ec2_client, instance_ids)
    return response

def Driver_initiate_instance(region_name, aws_access_key_id, aws_secret_access_key):
    """
    Driver function to initiate instances.
    """
    ec2_resource = get_ec2_service(region_name, aws_access_key_id, aws_secret_access_key, service_type='resource')

    # Initiate a new instance
    image_id = "ami-0cc9838aa7ab1dce7"
    instance_type = "t2.micro"
    min_count = 1
    max_count = 1
    new_instance = initiate_instance(ec2_resource, image_id, instance_type, min_count, max_count)
    return new_instance

