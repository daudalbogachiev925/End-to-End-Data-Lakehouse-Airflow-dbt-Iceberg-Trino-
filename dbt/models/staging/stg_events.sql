{{ config(materialized='table', schema='silver') }}

SELECT
    event_id,
    user_id,
    LOWER(event_type) AS event_type,
    product_id,
    CAST(price AS DECIMAL(10,2)) AS price,
    country,
    CAST(timestamp AS TIMESTAMP) AS event_ts,
    CAST(event_date AS DATE) AS event_date
FROM {{ source('bronze', 'events_raw') }}
WHERE event_id IS NOT NULL
