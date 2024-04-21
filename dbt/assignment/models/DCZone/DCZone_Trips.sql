{{ config(materialized='table', alias='DCZone_Trips') }}

/* Expand the original data with date that derive from the timestamps and fill NULL values where it makes sense */
WITH CTE_Expanded_Base AS (
SELECT
    hvfhs_license_num,
    dispatching_base_num,
    originating_base_num,
    request_datetime,
    CAST(request_datetime AS DATE) AS request_date,
    on_scene_datetime,
    CAST(on_scene_datetime AS DATE) AS on_scene_date,
    pickup_datetime,
    CAST(pickup_datetime AS DATE) AS pickup_date,
    dropoff_datetime,
    CAST(dropoff_datetime AS DATE) AS dropoff_date,
    pu_location_id,
    do_location_id,
    COALESCE(trip_miles,0) AS trip_miles,
    COALESCE(trip_time,0) AS trip_time,
    COALESCE(base_passenger_fare,0) AS base_passenger_fare,
    COALESCE(tolls,0) AS tolls,
    COALESCE(bcf,0) AS bcf,
    COALESCE(sales_tax,0) AS sales_tax,
    COALESCE(congestion_surcharge,0) AS congestion_surcharge,
    COALESCE(airport_fee,0) AS airport_fee,
    COALESCE(tips,0) AS tips,
    COALESCE(driver_pay,0) AS driver_pay,
    shared_request_flag,
    shared_match_flag,
    access_a_ride_flag,
    wav_request_flag
FROM 
    {{ref("CleansedZone_FHVHV")}}
)
SELECT
    base.*,
    CASE
        WHEN airport_fee > 0 THEN TRUE
        ELSE FALSE
    END AS IsAirportTrip,
    CASE
        WHEN tips > 0 THEN TRUE
        ELSE FALSE
    END AS IsHappyCustomer
FROM CTE_Expanded_Base