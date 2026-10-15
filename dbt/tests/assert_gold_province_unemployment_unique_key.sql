SELECT
    geo,
    age_group,
    ref_date,
    COUNT(*) AS n_rows
FROM {{ ref('province_unemployment_monthly') }}
GROUP BY geo, age_group, ref_date
HAVING COUNT(*) > 1