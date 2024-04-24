{{ config(alias='BusiestPickupLocations') }}

SELECT
    pu_location_id,
    count(dw_trip_id) as number_of_trips
FROM 
    {{ref("DCZone_DC_Trips")}}
GROUP BY
    pu_location_id
ORDER BY number_of_trips desc
LIMIT 5
