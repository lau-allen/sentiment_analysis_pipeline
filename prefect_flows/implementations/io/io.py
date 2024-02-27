from prefect import flow 
from prefect_aws.s3 import S3Bucket
import json 
import tempfile 
import os 
import asyncio

class io:

    def __init__(self):
        """
        Generator function 
        """
        #define s3 block
        self.s3_bucket = S3Bucket.load('pipeline-webscrape-extract')
        #define temp directory
        self.temp_dir = tempfile.TemporaryDirectory()

    def __del__(self):
        """
        Destructor to clean up temp directory 
        """
        #delete temp directory if exists 
        if self.temp_dir:
            self.temp_dir.cleanup()

    def ls(self) -> list:
        """
        Output list of bucket items and associated metadata

        Returns:
            list: list of bucket items 
        """
        #retrieve list of objects located in the bucket 
        return self.s3_bucket.list_objects()

    def write_to_json(self,data_dict:dict,fname:str,path=None) -> None:
        """
        Writes data to json files in a temp directory or defined directory. 

        Args:
            data_dict (dict): dictionary of data 
            fname (str): file name 
            path (str, optional): path to write json files. Defaults to None.
        """
        #if extension doesn't exist, then append 
        if not fname.endswith('.json'):
            fname = fname+'.json'
        #if path doesn't exist, then write dict to temp dir as json
        if path == None:
            with open(os.path.join(self.temp_dir.name,fname), 'w') as f:
                json.dump(data_dict,f)
        else:
            with open(os.path.join(path,fname), 'w') as f:
                json.dump(data_dict,f)
        return 

    async def push_to_s3(self,f:str) -> None:
        """
        Push data to S3 bucket 

        Args:
            f (str): path to file object 
        """
        #await pushing object to bucket 
        await self.s3_bucket.upload_from_path(f)
        return 

    async def async_push_to_s3(self,paths:list) -> None:
        """
        Define tasks to asynchronously push files to S3 bucket 

        Args:
            paths (list): list of paths to files 
        """
        #create task list 
        tasks = [self.push_to_s3(f) for f in paths]
        #wait for tasks to complete
        await asyncio.gather(*tasks)
        return 
    
    def pushObject_to_S3(self,path=None) -> None:
        """
        Entry to either asynchronously push all files in temp directory to S3 bucket or 
        push single file to bucket

        Args:
            path (str, optional): path to file. Defaults to None.
        """
        #if path is None, will push all contents of temp directory to S3 Bucket asynchronously  
        if path == None:
            #create list of paths to files 
            paths = []
            for f in os.listdir(self.temp_dir.name):
                paths.append(os.path.join(self.temp_dir.name,f))
            #async push to s3 bucket 
            asyncio.run(self.async_push_to_s3(paths))
        else:
            #push defined content to bucket 
            self.s3_bucket.upload_from_path(from_path=path)


if __name__ == '__main__':
    # test = io()
    # data1 = {'test':1,'test2':2}
    # data2 = {'test':1,'test2':2}
    # data3 = {'test':1,'test2':2}
    # data = [data1,data2,data3]
    # for i,d in enumerate(data):
    #     test.write_to_json(d,f'test_{i}')
    # test.pushObject_to_S3()
    # del test
    pass



