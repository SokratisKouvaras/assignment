{{ config(alias='Hourly') }}

SELECT
    request_date,
    count(dw_trip_id) as number_of_trips
FROM 
    {{ref("DCZone_DC_Trips")}}
GROUP BY
    request_date
ORDER BY request_date ASC

