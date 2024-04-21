{{ config(materialized='view', alias='FHVHV') }}

SELECT
    hvfhs_license_num,
    dispatching_base_num,
    originating_base_num,
    request_datetime,
    on_scene_datetime,
    pickup_datetime,
    dropoff_datetime,
    "PULocationID" as pu_location_id,
    "DOLocationID" as do_location_id,
    trip_miles,
    trip_time,
    base_passenger_fare,
    tolls,
    bcf,
    sales_tax,
    congestion_surcharge,
    airport_fee,
    tips,
    driver_pay,
    shared_request_flag,
    shared_match_flag,
    access_a_ride_flag,
    wav_request_flag,
    wav_match_flag
FROM 
    {{source("public","fhvhv_tripdata_2024_01")}}