{{ config(materialized='view',alias='TaxiBases') }}

SELECT
    license_number,
    entity_name,
    telephone_number,
    shl_endorsed,
    building,
    street,
    city,
    state,
    postcode,
    type_of_base,
    latitude,
    longitude,
    date
FROM 
    {{ref("current_bases")}}
