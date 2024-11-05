import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

db_url = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@postgres:{DB_PORT}/{DB_NAME}"
engine = create_engine(db_url)


def update_record(
    record_id: int,
    src_url: str,
    dst_url: str,
    resolution: str,
    size: int,
    status="Success",
) -> None:
    with engine.connect() as connection:
        query = text(
            """
            UPDATE image_app_image
            SET src_url = '%s',
                dst_url = '%s',
                resolution = '%s',
                size = %s,
                status = '%s'
            WHERE id = %s;
            """
            % (src_url, dst_url, resolution, size, status, record_id)
        )
        connection.execute(query)
        connection.commit()
