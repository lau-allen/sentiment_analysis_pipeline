#libraries
from prefect import flow,task
from implementations.io.io import io
import redshift_connector
import boto3 
from botocore.exceptions import ClientError
import config
import json

def get_secret():

    secret_name = config.redshift_secret
    region_name = config.aws_region

    #create secret manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']

    return secret

@task 
def redshift_connection() -> None:
    #get and parse secret string
    secret_data = json.loads(get_secret())

    # # Extract Redshift connection details
    # redshift_username = secret_data['username']
    # redshift_password = secret_data['password']
    # redshift_host = secret_data['host']
    # redshift_port = secret_data['port']
    # redshift_db = secret_data['dbClusterIdentifier']

    # #opening connection to Redshift cluster 
    # conn = redshift_connector.connect(
    #     host = redshift_host,
    #     database= redshift_db,
    #     port = redshift_port, 
    #     user = redshift_username,
    #     password = redshift_password,
    # )
    # return conn 

@task 
def create_schema(connection:redshift_connector.connect) -> None:
    #create cursor object 
    cursor = connection.cursor()
    #check available tables 
    print(cursor.get_tables())

    return 


@flow 
def data_normalization() -> None:
    #obtain Redshift Connection
    conn = redshift_connection()
    # #create schema if not exist 
    # create_schema(conn)

    # #close connection 
    # conn.close()

    return 

if __name__ == '__main__':
    #kickoff data normalization flow 
    data_normalization()



