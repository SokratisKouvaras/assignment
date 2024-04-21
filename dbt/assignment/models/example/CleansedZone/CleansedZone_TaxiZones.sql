{{ config(materialized='view',alias='TaxiZones') }}

SELECT
    "LocationID" AS location_id,
    "Borough" AS borough,
    "Zone" AS zone,
    service_zone
FROM 
    {{ref("taxi_zone_lookup")}}
