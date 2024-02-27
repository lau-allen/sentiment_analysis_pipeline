from prefect import flow 
from prefect_aws.s3 import S3Bucket

class io:

    def __init__(self):
        #define s3 block
        self.s3_block = S3Bucket.load('pipeline-webscrape-extract')

    def ls(self):
        return self.s3_block.list_objects()
    



if __name__ == '__main__':
    test = io()
    print(test.ls())
