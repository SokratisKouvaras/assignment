{{ config(materialized='view', alias='FHVHV') }}

SELECT
    hvfhs_license_num,
    dispatching_base_num,
    originating_base_num,
    CAST(request_datetime AS TIMESTAMP) AS request_datetime,
    CAST(on_scene_datetime AS TIMESTAMP) AS on_scene_datetime,
    CAST(pickup_datetime AS TIMESTAMP) AS pickup_datetime,
    CAST(dropoff_datetime AS TIMESTAMP) AS dropoff_datetime,
    "PULocationID" AS pu_location_id,
    "DOLocationID" AS do_location_id,
    CAST(trip_miles AS FLOAT) AS trip_miles,
    CAST(trip_time AS FLOAT) AS trip_time,
    CAST(base_passenger_fare AS FLOAT) AS base_passenger_fare,
    CAST(tolls AS FLOAT) AS tolls,
    CAST(bcf AS FLOAT) AS bcf,
    CAST(sales_tax AS FLOAT) AS sales_tax,
    CAST(congestion_surcharge AS FLOAT) AS congestion_surcharge,
    CAST(airport_fee AS FLOAT) AS airport_fee,
    CAST(tips AS FLOAT) AS tips,
    CAST(driver_pay AS FLOAT) AS driver_pay,
    {{ convert_flag('shared_request_flag') }} AS shared_request_flag,
    {{ convert_flag('shared_match_flag') }} AS shared_match_flag,
    {{ convert_flag('access_a_ride_flag') }} AS access_a_ride_flag,
    {{ convert_flag('wav_request_flag') }} AS wav_request_flag
FROM 
    {{source("public","fhvhv_tripdata_2024_01")}}