# Sources
## Tables
### FHVHV
{% docs FHVHV %}
This table the daily taxi trips from the FHVHV NYC dataset.
{% enddocs %}
### FHVHV Features

{% docs hvfhs_license_num %}
The TLC license number of the HVFHS base or business
As of September 2019, the HVFHS licensees are the following:
• HV0002: Juno
• HV0003: Uber
• HV0004: Via
• HV0005: Lyft
{% enddocs %}

{% docs dispatching_base_num %}
The TLC Base License Number of the base that dispatched the trip.
{% enddocs %}

{% docs originating_base_num %}
base number of the base that received the original trip request.
{% enddocs %}

{% docs request_datetime %}
date/time when passenger requested to be picked up
{% enddocs %}

{% docs on_scene_datetime %}
date/time when driver arrived at the pick-up location (Accessible
Vehicles-only)
{% enddocs %}

{% docs pickup_datetime %}
The date and time of the trip pick-up.
{% enddocs %}

{% docs dropoff_datetime %}
The date and time of the trip drop-off.
{% enddocs %}

{% docs pu_location_id %}
TLC Taxi Zone in which the trip began
{% enddocs %}

{% docs do_location_id %}
TLC Taxi Zone in which the trip ended
{% enddocs %}

{% docs trip_miles %}
total miles for passenger trip
{% enddocs %}

{% docs trip_time %}
total time in seconds for passenger trip
{% enddocs %}

{% docs base_passenger_fare %}
base passenger fare before tolls, tips, taxes, and fees.
{% enddocs %}

{% docs tolls %}
Total amount of all tolls paid in trip.
{% enddocs %}

{% docs bcf %}
total amount collected in trip for Black Car Fund
{% enddocs %}

{% docs sales_tax %}
total amount collected in trip for NYS sales tax
{% enddocs %}

{% docs congestion_surcharge %}
Total amount collected in trip for NYS congestion surcharge
{% enddocs %}

{% docs airport_fee %}
$2.50 for both drop off and pick up at LaGuardia, Newark, and John
F. Kennedy airports
{% enddocs %}

{% docs tips %}
total amount of tips received from passenger
{% enddocs %}

{% docs driver_pay %}
total driver pay (not including tolls or tips and net of commission,
surcharges, or taxes)
{% enddocs %}

{% docs shared_request_flag %}
Did the passenger agree to a shared/pooled ride, regardless of
whether they were matched? (Y/N)
{% enddocs %}

{% docs shared_match_flag %}
Did the passenger share the vehicle with another passenger who
booked separately at any point during the trip? (Y/N)
{% enddocs %}

{% docs access_a_ride_flag %}
Was the trip administered on behalf of the Metropolitan
Transportation Authority (MTA)? (Y/N)
{% enddocs %}

{% docs wav_request_flag %}
Did the passenger request a wheelchair-accessible vehicle (WAV)?
(Y/N)
{% enddocs %}

{% docs wav_match_flag %}
Did the trip occur in a wheelchair-accessible vehicle (WAV) (Y/N)
{% enddocs %}

# CleansedZone
## Tables

{% docs CleansedZone_FHVHV %}
This table is a simple proxy model of the FHVHV dataset holding the daily taxi trips.
The model features have been assigned the correct datatype and every column is in lower snake case.
{% enddocs %}

### CleansedZone_FHVHV Features
{% docs CleansedZone_hvfhs_license_num %}
test
{% enddocs %}

{% docs CleansedZone_dispatching_base_num %}
The TLC Base License Number of the base that dispatched the trip.
{% enddocs %}

{% docs CleansedZone_originating_base_num %}
base number of the base that received the original trip request.
{% enddocs %}

{% docs CleansedZone_request_datetime %}
date/time when passenger requested to be picked up
{% enddocs %}

{% docs CleansedZone_on_scene_datetime %}
date/time when driver arrived at the pick-up location (Accessible
Vehicles-only)
{% enddocs %}

{% docs CleansedZone_pickup_datetime %}
The date and time of the trip pick-up.
{% enddocs %}

{% docs CleansedZone_dropoff_datetime %}
The date and time of the trip drop-off.
{% enddocs %}

{% docs CleansedZone_pu_location_id %}
TLC Taxi Zone in which the trip began
{% enddocs %}

{% docs CleansedZone_do_location_id %}
TLC Taxi Zone in which the trip ended
{% enddocs %}

{% docs CleansedZone_trip_miles %}
total miles for passenger trip
{% enddocs %}

{% docs CleansedZone_trip_time %}
total time in seconds for passenger trip
{% enddocs %}

{% docs CleansedZone_base_passenger_fare %}
base passenger fare before tolls, tips, taxes, and fees.
{% enddocs %}

{% docs CleansedZone_tolls %}
Total amount of all tolls paid in trip.
{% enddocs %}

{% docs CleansedZone_bcf %}
total amount collected in trip for Black Car Fund
{% enddocs %}

{% docs CleansedZone_sales_tax %}
total amount collected in trip for NYS sales tax
{% enddocs %}

{% docs CleansedZone_congestion_surcharge %}
Total amount collected in trip for NYS congestion surcharge
{% enddocs %}

{% docs CleansedZone_airport_fee %}
$2.50 for both drop off and pick up at LaGuardia, Newark, and John
F. Kennedy airports
{% enddocs %}

{% docs CleansedZone_tips %}
total amount of tips received from passenger
{% enddocs %}

{% docs CleansedZone_driver_pay %}
total driver pay (not including tolls or tips and net of commission,
surcharges, or taxes)
{% enddocs %}

{% docs CleansedZone_shared_request_flag %}
Did the passenger agree to a shared/pooled ride, regardless of
whether they were matched? (Y/N)
{% enddocs %}

{% docs CleansedZone_shared_match_flag %}
Did the passenger share the vehicle with another passenger who
booked separately at any point during the trip? (Y/N)
{% enddocs %}

{% docs CleansedZone_access_a_ride_flag %}
Was the trip administered on behalf of the Metropolitan
Transportation Authority (MTA)? (Y/N)
{% enddocs %}

{% docs CleansedZone_wav_request_flag %}
Did the passenger request a wheelchair-accessible vehicle (WAV)?
(Y/N)
{% enddocs %}

{% docs CleansedZone_wav_match_flag %}
Did the trip occur in a wheelchair-accessible vehicle (WAV) (Y/N)
{% enddocs %}

# DCZone
## Tables
### DCZone_DC_Trips

{% docs DCZone_DC_Trips %}
This table is the expanded version of the original FHVHV trips model enriched with additional features related to the 
taxi bases and pickup/drop-off locations.
{% enddocs %}

### CleansedZone_FHVHV Features
{% docs DCZone_DC_Trips_dw_trip_id %}
The primary key of the Trips domain concept. 

{% enddocs %}