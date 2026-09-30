SELECT *
FROM {{ ref('fct_daily_revenue') }}
WHERE revenue < 0
