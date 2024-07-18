from minio import Minio
from config.config import HOST_MINIO, ACCESS_KEY, SECRET_KEY


s3client = Minio(endpoint=HOST_MINIO,
                 access_key=ACCESS_KEY,
                 secret_key=SECRET_KEY,
                 secure=False)
