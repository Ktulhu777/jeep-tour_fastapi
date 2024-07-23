import os

from fastapi import UploadFile
from miniopy_async import Minio


class S3Client(Minio):

    async def add_avatar(self, photo: UploadFile, username: str):
        if photo:
            file_size = os.fstat(photo.file.fileno()).st_size
            await self.put_object(username,
                                  f'ava_{username}.{photo.filename[photo.filename.find(".")+1:]}', photo.file,
                                  file_size)
            return True
