from fastparquet import ParquetFile
import requests
import pyarrow as pa
import pyarrow.parquet as pq
import logging
from sqlalchemy import types
import pandas
import sqlalchemy as sa
from datetime import datetime
connection_url = sa.URL.create(
        "postgresql",
        username="postgres",
        password="",
        host="127.0.0.1",
        port="5432",
        database="postgres",
    )
engine = sa.create_engine(connection_url)
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
logger = logging.getLogger(__name__)
URL = 'https://d37ci6vzurychx.cloudfront.net/trip-data/fhvhv_tripdata_2024-01.parquet'
with open("myfile.parquet", "wb") as binary_file:
    # Write bytes to file
    logger.warning('trying to save file')
    binary_file.write(requests.get(URL).content)
    logger.warning('file saved')
parquet_file = pq.ParquetFile('./myfile.parquet')
counter = 1
for i in parquet_file.iter_batches(batch_size=100000):
    logger.warning(f"{datetime.now()} : RecordBatch {counter}")
    i.to_pandas().to_sql(
            "testfrompyarrow",
            engine,
            chunksize=None,
            if_exists="append",
            method=None,
            index=False,
            schema="public",
            dtype=PG_DATA_TYPES,
        )
    counter = counter + 1


#import pyarrow.csv
#pa.csv.write_csv(pq.read_table(r.text), "table.csv",
#                 write_options=pa.csv.WriteOptions(include_header=True))