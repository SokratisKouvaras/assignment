import logging
from sqlalchemy import types 

logger = logging.getLogger(__name__)

PG_DATA_TYPES = {
    "hvfhs_license_num": types.Text,
    "dispatching_base_num": types.Text,
    "originating_base_num": types.Text,
    "request_datetime": types.TIMESTAMP(0),
    "on_scene_datetime": types.TIMESTAMP(0),
    "pickup_datetime": types.TIMESTAMP(0),
    "dropoff_datetime": types.TIMESTAMP(0),
    "PULocationID": types.Integer,
    "DOLocationID": types.Integer,
    "trip_miles": types.Float,
    "trip_time": types.Integer,
    "base_passenger_fare": types.Float,
    "tolls": types.Float,
    "bcf": types.Float,
    "sales_tax": types.Float,
    "congestion_surcharge": types.Float,
    "airport_fee": types.Float,
    "tips": types.Float,
    "driver_pay": types.Float,
    "shared_request_flag": types.Text,
    "shared_match_flag": types.Text,
    "access_a_ride_flag": types.Text,
    "wav_request_flag": types.Text,
    "wav_match_flag": types.Text,
}


def get_parquet_content(year="2024", month="01"):
    """
    This function performs a GET request on the https://d37ci6vzurychx.cloudfront.net/trip-data/
    endpoint for the fhvhv_tripdata. The default year is set to 2024 and the default month to 01 as described
    in the assignment.
    The function returns the content of the GET request that is a parquet formatted string.
    """
    import requests

    URL = f"https://d37ci6vzurychx.cloudfront.net/trip-data/fhvhv_tripdata_{year}-{month}.parquet"
    try:
        logger.warning(f"{datetime.now()}:Trying to fetch the content of {URL} ...")
        r = requests.get(URL)
        logger.warning(f"{datetime.now()}:Succesfully loaded the content of {URL} in memory")
    except Exception as e:
        logger.warning(
            f"{datetime.now()}:The following exception occured while trying to get the parquet content : {e}"
        )
    return r.content


def store_dataframe_to_pg(df_to_store, pg_table_name):
    """
    This function creates a connection to a local instance of a PG container
    and stores the input dataframe with the name provided in the function arguments.
    The credentials are hardcoded since this is a simple test scenario.
    To avoid memory issues the chunksize is set to 10k rows.
    """
    import sqlalchemy as sa

    connection_url = sa.URL.create(
        "postgresql",
        username="postgres",
        password="",
        host="127.0.0.1",
        port="5432",
        database="postgres",
    )
    engine = sa.create_engine(connection_url)
    try:
        logger.warning(f"{datetime.now()}:Storing the dataframe in Postgres...")
        df_to_store.to_sql(
            pg_table_name,
            engine,
            chunksize=100000,
            if_exists="replace",
            method=None,
            index=False,
            schema="public",
            dtype = PG_DATA_TYPES
        )
        logger.warning(
            f"{datetime.now()}:Succesfully stored the dataframe in Postgres in table: {pg_table_name}"
        )
    except Exception as e:
        logger.warning(
            f"{datetime.now()}:The following exception occured while trying to store the dataframe in Postgres: {e}"
        )


def main():
    import pandas as pd
    from io import BytesIO
    from datetime import datetime

    # get the content of the table and store it in a pandas dataframe
    logger.warning(
        f"{datetime.now()}:Converting the content of the parquet sting in a pandas dataframe..."
    )
    df_parquet = pd.read_parquet(BytesIO(get_parquet_content()))
    logger.warning(f"{datetime.now()}:Succesfully created the pandas dataframe")
    store_dataframe_to_pg(
        df_parquet, f"fhvhv_tripdata_{datetime.now():%Y_%m_%d_%H_%M_%S%z}"
    )


if __name__ == "__main__":
    main()
