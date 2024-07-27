import json
import os

from fastapi import UploadFile
from miniopy_async import Minio
from config.config import HOST_MINIO, ACCESS_KEY, SECRET_KEY


class S3Client(Minio):
    async def set_policy(self, bucket_name: str):
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {"Effect": "Allow", "Principal": "*", "Action": ["s3:GetObject"],
                 "Resource": [f"arn:aws:s3:::{bucket_name}/*"]
                 }
            ]
        }
        await self.set_bucket_policy(bucket_name, json.dumps(policy))

    async def make_bucket(self, bucket_name, location="us-east-1", object_lock=False) -> None:
        await super().make_bucket(bucket_name, location, object_lock)
        await self.set_policy(bucket_name)

    async def add_avatar(self, photo: UploadFile, username: str):
        if photo:
            file_size = os.fstat(photo.file.fileno()).st_size
            await self.put_object(username,
                                  f'ava_{username}.{photo.filename[photo.filename.find(".") + 1:]}', photo.file,
                                  file_size)
            return True

    async def add_default_avatar(self, username, filename):
        with open(filename, mode='rb') as photo:
            file_size = os.path.getsize(photo.fileno())
            await self.put_object(
                username,
                filename,
                photo,
                file_size
            )
        os.remove(filename)
        return True


s3_client = S3Client(endpoint=HOST_MINIO, access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)
