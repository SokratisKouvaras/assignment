from fastparquet import ParquetFile
import requests
import pyarrow as pa
import pyarrow.parquet as pq
import logging
from sqlalchemy import types
import sqlalchemy as sa
from datetime import datetime

# Generic config
BATCH_SIZE = 100000
LOCAL_PARQUET_FILENAME = "temp.parquet"

CONNECTION_URL = sa.URL.create(
    "postgresql",
    username="postgres",
    password="",
    host="127.0.0.1",
    port="5432",
    database="postgres",
)
ENGINE = sa.create_engine(CONNECTION_URL)
PG_DATA_TYPES = {
    "hvfhs_license_num": types.Text,
    "dispatching_base_num": types.Text,
    "originating_base_num": types.Text,
    "request_datetime": types.Text,
    "on_scene_datetime": types.Text,
    "pickup_datetime": types.Text,
    "dropoff_datetime": types.Text,
    "PULocationID": types.Text,
    "DOLocationID": types.Text,
    "trip_miles": types.Text,
    "trip_time": types.Text,
    "base_passenger_fare": types.Text,
    "tolls": types.Text,
    "bcf": types.Text,
    "sales_tax": types.Text,
    "congestion_surcharge": types.Text,
    "airport_fee": types.Text,
    "tips": types.Text,
    "driver_pay": types.Text,
    "shared_request_flag": types.Text,
    "shared_match_flag": types.Text,
    "access_a_ride_flag": types.Text,
    "wav_request_flag": types.Text,
    "wav_match_flag": types.Text,
}
PG_DESTINATION_SCHEMA = "public"
logger = logging.getLogger(__name__)


def get_parquet_content(dataset, year, month):
    """
    This function performs a GET request on the https://d37ci6vzurychx.cloudfront.net/trip-data/
    endpoint for the fhvhv_tripdata. The default year is set to 2024 and the default month to 01 as described
    in the assignment.
    The function stores the content of the get request on a local file.
    """

    URL = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{dataset}_{year}-{month}.parquet"
    try:
        logger.warning(f"{datetime.now()}:Trying to fetch the content of {URL} ...")

        with open(LOCAL_PARQUET_FILENAME, "wb") as binary_file:

            binary_file.write(requests.get(URL).content)

        logger.warning(
            f"{datetime.now()}:Succesfully saved the content of {URL} in {LOCAL_PARQUET_FILENAME} file"
        )
        return
    except Exception as e:
        logger.warning(
            f"{datetime.now()}:The following exception occured while trying to get the parquet content : {e}"
        )


def send_parquet_file_to_pg(parquet_file, pg_table_name):
    """
    This function splits a ParquetFile object into BATCH_SIZE number of batches
    as set in the config variable (hardcoded to 100k). Using a for loop
    to iterate over all the batches it converts them to Pandas dataframes
    and using the to_sql function it writes them in Postgres.
    """
    counter = 1

    logger.warning(
        f"{datetime.now()}: Trying to send parquet to PG using {BATCH_SIZE} batches"
    )
    try:
        for i in parquet_file.iter_batches(batch_size=BATCH_SIZE):
            db_connection = ENGINE.connect()
            logger.warning(f"{datetime.now()} : Trying to send  batch {counter}")
            i.to_pandas().to_sql(
                pg_table_name,
                con=db_connection,
                chunksize=None,
                if_exists="append",
                method=None,
                index=False,
                schema=PG_DESTINATION_SCHEMA,
                dtype=PG_DATA_TYPES,
            )
            db_connection.close()
            logger.warning(f"{datetime.now()} : Succesfully sent batch {counter}")
            counter += 1
        return
    except Exception as e:
        logger.warning(
            f"{datetime.now()}:The following exception occured while trying to send the parquet batches to Postgres : {e}"
        )


"""
This function replaces the PG table with the newly ingested one
"""


def cleanup(old_pg_table_name, new_pg_table_name):
    from sqlalchemy import text

    sql = f"""
    DROP TABLE IF EXISTS {new_pg_table_name};
    ALTER TABLE {old_pg_table_name} RENAME TO {new_pg_table_name};
    """
    try:
        logger.warning(
            f"Trying to replace {old_pg_table_name} with {new_pg_table_name}"
        )
        db_connection = ENGINE.connect()
        db_connection.execute(text(sql))
        db_connection.commit()
        db_connection.close()
        logger.warning(
            f"Successfully replaced {old_pg_table_name} with {new_pg_table_name}"
        )
    except Exception as e:
        logger.warning(
            f"An exception occured while trying to replace {old_pg_table_name} with {new_pg_table_name}"
        )


"""
dataset : 'yellow_tripdata', 'green_tripdata','fhvhv_tripdata'
"""


def main(dataset="fhvhv_tripdata", year="2024", month="01"):
    PG_TABLE_NAME = f"{dataset}_{year}_{month}_{datetime.now():%Y_%m_%d_%H_%M_%S%z}"
    get_parquet_content(dataset, year, month)
    parquet_file = pq.ParquetFile(f"./{LOCAL_PARQUET_FILENAME}")
    send_parquet_file_to_pg(parquet_file, PG_TABLE_NAME)
    cleanup(
        old_pg_table_name=PG_TABLE_NAME, new_pg_table_name=f"{dataset}_{year}_{month}"
    )


if __name__ == "__main__":
    main()
