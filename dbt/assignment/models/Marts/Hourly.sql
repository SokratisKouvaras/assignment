{{ config(alias='Hourly') }}

SELECT
    pickup_hour,
    avg(trip_miles) as average_travel_distance_in_miles,
    avg(trip_time) as average_travel_duration_in_seconds
FROM 
    {{ref("DCZone_DC_Trips")}}
GROUP BY
    pickup_hour
ORDER BY pickup_hour ASC

