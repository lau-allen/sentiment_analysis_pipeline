#import libraries 
import os 
import config
from prefect_aws import S3Bucket, AwsCredentials,ECSTask
import json

if __name__ == '__main__':

    with open('terraform/terraform.tfstate','r') as f:
        outputs = json.load(f)['outputs']

    # #create s3 user credentials block
    # s3_user_credentials = AwsCredentials(
    #     aws_access_key_id = os.environ.get("MY_AWS_S3_ACCESS_KEY_ID"),
    #     aws_secret_access_key = os.environ.get("MY_AWS_S3_SECRET_ACCESS_KEY")
    #     )
    # s3_user_credentials.save(name="sap-s3-user-credentials",overwrite=True)
    
    # #create s3 bucket block
    # s3_bucket = S3Bucket.create(
    #     bucket=config.s3_block,
    #     credentials="sap-s3-user-credentials"
    #     )
    # s3_bucket.save(name=config.s3_block,overwrite=True)

    #create ECS task block 
    webscrape_extract_ecs_task = ECSTask(
        image="alau002/sap-webscrape-extract:latest",
        vpc_id=outputs['vpc_id']['value'],
        cluster=outputs['prefect_agent_cluster_name']['value'],
        execution_role_arn=outputs['prefect_agent_execution_role_arn']['value'],
        task_customizations=[
            {
                "op": "add",
                "path": "/networkConfiguration/awsvpcConfiguration/securityGroups",
                "value": [outputs['prefect_agent_security_group']['value']]
            }
        ],
        task_start_timeout_seconds=120
    )
    webscrape_extract_ecs_task.save(name=config.webscrape_ecs_task,overwrite=True)
    
