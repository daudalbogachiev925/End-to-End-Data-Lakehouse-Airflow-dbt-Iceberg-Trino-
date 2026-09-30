{{ config(materialized='table', schema='gold') }}

SELECT
    event_date,
    country,
    COUNT(DISTINCT user_id) AS dau,
    COUNT_IF(event_type = 'purchase') AS purchases,
    SUM(CASE WHEN event_type = 'purchase' THEN price ELSE 0 END) AS revenue,
    ROUND(AVG(CASE WHEN event_type = 'purchase' THEN price END), 2) AS aov
FROM {{ ref('stg_events') }}
GROUP BY 1, 2
