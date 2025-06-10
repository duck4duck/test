import asyncio
from contextlib import asynccontextmanager
from aiobotocore.session import get_session 
import os
from config import settings

class S3_Client():
    def __init__(self,
                 access_key:str,
                 secret_key:str,
                 endpoint_url:str,
                 bucket_name:str,):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key":secret_key,
            "endpoint_url":endpoint_url
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3",**self.config) as client:
            yield client


    async def upload_file(self,file_path:str,object_name:str):
        object_name = file_path.split("/")[-1]
        async with self.get_client() as client:
            with open(file_path,"rb") as file:
                await client.put_object(
                    Bucket = self.bucket_name,
                    Key = object_name,
                    Body = file,
                )


    async def create_bucket(self):
         async with self.get_client() as client:
            response = await client.list_buckets()
            existing_buckets = [bucket['Name'] for bucket in response['Buckets']]
            if self.bucket_name in existing_buckets:
                print(f"Bucket '{self.bucket_name}' уже существует.")
                return
            await client.create_bucket(Bucket=self.bucket_name)
            print(f"Bucket '{self.bucket_name}' создан.")

s3_client = S3_Client(
    access_key=settings.s3_access_key,
    secret_key=settings.s3_secret_key,
    endpoint_url=settings.s3_endpoint_url,
    bucket_name=settings.s3_bucket_name
)
    # await s3_client.create_bucket()
    # await s3_client.upload_file("/home/ipcat/mytest/api_v1/s3/pic.jpeg","pic.jpeg")
    


