{{ config(alias='DCZone_DC_Trips') }}

/* Expand the original data with date that derive from the timestamps and fill NULL values where it makes sense */
WITH CTE_Expanded_BASe AS (
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
/* 
- Further expand the model by replacing the location ids with the metadata from the taxi zone seed.
- Further expand the model with the vendor information 
*/
SELECT
    md5(
        concat(
            base.hvfhs_license_num,
            base.pu_location_id,
            base.request_datetime,
            base.pickup_datetime,
            base.do_location_id,
            base.dropoff_datetime
            )
        ) AS dw_trip_id,
    extract('hour' from pickup_datetime) AS pickup_hour,
    extract('hour' from dropoff_datetime) AS dropoff_hour,
    base.*,
    CASE
        WHEN base.airport_fee > 0 THEN TRUE
        ELSE FALSE
    END AS is_airport_trip,
    CASE
        WHEN base.pu_location_id = do_location_id THEN TRUE
        ELSE FALSE
    END AS is_local_trip,
    CASE
        WHEN base.tips > 0 THEN TRUE
        ELSE FALSE
    END AS is_happy_customer,
    CASE
        WHEN base.hvfhs_license_num = 'HV0002' THEN 'Juno'
        WHEN base.hvfhs_license_num = 'HV0003' THEN 'Uber'
        WHEN base.hvfhs_license_num = 'HV0004' THEN 'Via'
        WHEN base.hvfhs_license_num = 'HV0005' THEN 'Lyft'
        ELSE 'Unknown'
    END AS company_name,
    pick_up_metadata.borough AS pick_up_borough,
    pick_up_metadata.zone AS pick_up_zone,
    pick_up_metadata.service_zone AS pick_up_service_zone,
    drop_off_metadata.borough AS drop_off_borough,
    drop_off_metadata.zone AS drop_off_zone,
    drop_off_metadata.service_zone AS drop_off_service_zone,
    extract('week' from pickup_date) AS pickup_week,
    extract('week' from dropoff_date) AS dropoff_week,
    dispatching_base.latitude AS dispatching_base_latitude,
    dispatching_base.longitude AS dispatching_base_longitude,
    dispatching_base.type_of_base AS dispatching_base_type,
    dispatching_base.entity_name AS dispatching_base_entity_name,
    originating_base.latitude AS originating_base_latitude,
    originating_base.longitude AS originating_base_longitude,
    originating_base.type_of_base AS originating_base_type,
    originating_base.entity_name AS originating_base_entity_name
FROM CTE_Expanded_Base AS base
LEFT JOIN {{ref("CleansedZone_TaxiZones")}} AS pick_up_metadata
ON pick_up_metadata.location_id = base.pu_location_id
LEFT JOIN {{ref("CleansedZone_TaxiZones")}} AS drop_off_metadata
ON drop_off_metadata.location_id = base.do_location_id
LEFT JOIN {{ref("CleansedZone_TaxiBases")}} AS dispatching_base
ON dispatching_base.license_number = base.dispatching_base_num
LEFT JOIN {{ref("CleansedZone_TaxiBases")}} AS originating_base
ON originating_base.license_number = base.originating_base_num