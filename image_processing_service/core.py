import base64
import json
import logging

from consts import RESOLUTION
from utils_change_images import ImageProcessing
from utils_postgres import update_record
from utils_s3 import S3FileUploader

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("image_processing.log"), logging.StreamHandler()],
)
logger = logging.getLogger("add_file")


def add_new_file_data(ch, method, properties, body: str):
    file_data = json.loads(body)
    file_data["src_file"] = base64.b64decode(file_data["src_file"][0].encode("utf-8"))

    image_processing = ImageProcessing(file_data.get("src_file"), RESOLUTION)
    dst_file = image_processing.get_converted_file()
    metadata = image_processing.get_metadata()

    src_url = S3FileUploader(
        file=file_data.get("src_file"),
        file_format=metadata.get("format"),
        directory="src",
    ).upload_file_to_s3()
    dst_url = S3FileUploader(
        file=dst_file, file_format=metadata.get("format"), directory="dst"
    ).upload_file_to_s3()

    update_record(
        record_id=file_data.get("id"),
        src_url=src_url,
        dst_url=dst_url,
        resolution=f'{metadata.get("resolution")[0]}X{metadata.get("resolution")[0]}',
        size=metadata.get("size"),
    )
    logger.debug(f"File for id = {file_data.get("id")} has been uploaded successfully.")
