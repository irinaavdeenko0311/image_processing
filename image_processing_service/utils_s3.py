import os
import uuid

import boto3
from dotenv import load_dotenv

load_dotenv()


AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
AWS_STORAGE_URL = os.environ.get("AWS_STORAGE_URL")
AWS_BUCKET_NAME = os.environ.get("AWS_BUCKET_NAME")

s3_client = boto3.client(
    "s3",
    endpoint_url=AWS_STORAGE_URL,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)


class S3FileUploader:
    def __init__(self, file: bytes, file_format: str, directory: str):
        self.__file = file
        self.__file_format = file_format
        self.__directory = directory

    def upload_file_to_s3(self) -> str:
        """
        Загрузка файла в s3-хранилище.

        Возвращает url файла в хранилище.
        """

        file_path = self.__get_file_path()
        s3_client.put_object(
            Body=self.__file,
            Bucket=AWS_BUCKET_NAME,
            Key=file_path,
            ContentType=self.__get_content_type(),
        )
        url = f"{AWS_STORAGE_URL}{AWS_BUCKET_NAME}/{file_path}"
        return url

    def __get_content_type(self) -> str:
        """Получение значения заголовка Content Type"""

        content_type = f"image/{self.__file_format}"
        return content_type

    def __get_file_path(self) -> str:
        """Получение пути до файла."""

        unique_filename = f"{self.__get_unique_identifier()}.{self.__file_format}"
        file_path = f"{self.__directory}/{unique_filename}"
        return file_path

    @staticmethod
    def __get_unique_identifier() -> str:
        """Получение идентификатора для уникального имени файла."""

        identifier = str(uuid.uuid4())
        return identifier
