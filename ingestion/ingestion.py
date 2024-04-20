import logging
from sqlalchemy import types
from datetime import datetime
import pandas as pd

logger = logging.getLogger(__name__)

PD_DATA_TYPES = {
    "hvfhs_license_num": str,
    "dispatching_base_num": str,
    "originating_base_num": str,
    "request_datetime": str,
    "on_scene_datetime": str,
    "pickup_datetime": str,
    "dropoff_datetime": str,
    "PULocationID": str,
    "DOLocationID": str,
    "trip_miles": str,
    "trip_time": str,
    "base_passenger_fare": str,
    "tolls": str,
    "bcf": str,
    "sales_tax": str,
    "congestion_surcharge": str,
    "airport_fee": str,
    "tips": str,
    "driver_pay": str,
    "shared_request_flag": str,
    "shared_match_flag": str,
    "access_a_ride_flag": str,
    "wav_request_flag": str,
    "wav_match_flag": str,
}

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


def get_parquet_content(year="2024", month="01"):
    """
    This function performs a GET request on the https://d37ci6vzurychx.cloudfront.net/trip-data/
    endpoint for the fhvhv_tripdata. The default year is set to 2024 and the default month to 01 as described
    in the assignment.
    The function returns the content of the GET request that is a parquet formatted string.
    """

    URL = f"https://d37ci6vzurychx.cloudfront.net/trip-data/fhvhv_tripdata_{year}-{month}.parquet"
    try:
        logger.warning(f"{datetime.now()}:Trying to fetch the content of {URL} ...")
        # 5kk empty rows removed
        data = pd.read_parquet(path=URL).astype(PD_DATA_TYPES)  # .dropna()
        print(data.dtypes)
        logger.warning(
            f"{datetime.now()}:Succesfully loaded the content of {URL} in memory"
        )
        return data
    except Exception as e:
        logger.warning(
            f"{datetime.now()}:The following exception occured while trying to get the parquet content : {e}"
        )


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
            dtype=PG_DATA_TYPES,
        )
        logger.warning(
            f"{datetime.now()}:Succesfully stored the dataframe in Postgres in table: {pg_table_name}"
        )
    except Exception as e:
        logger.warning(
            f"{datetime.now()}:The following exception occured while trying to store the dataframe in Postgres: {e}"
        )


def main():
    df_parquet = get_parquet_content()
    store_dataframe_to_pg(
        df_parquet, f"fhvhv_tripdata_{datetime.now():%Y_%m_%d_%H_%M_%S%z}"
    )


if __name__ == "__main__":
    main()
