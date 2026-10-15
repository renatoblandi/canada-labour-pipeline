WITH unemployment AS (
    SELECT
        ref_date,
        geo,
        age_group,
        value AS unemployment_rate
    FROM {{ ref('labour_force') }}
    WHERE labour_force_characteristics = 'Unemployment rate'
        AND statistics = 'Estimate'
        AND data_type = 'Seasonally adjusted'
        AND gender = 'Total - Gender'
        AND age_group IN ('15 years and over', '25 to 54 years')
),

canada AS (
    SELECT
        ref_date,
        age_group,
        unemployment_rate AS canada_unemployment_rate
    FROM unemployment
    WHERE geo = 'Canada'
)

SELECT
    u.ref_date,
    u.geo,
    u.age_group,
    u.unemployment_rate,
    c.canada_unemployment_rate,
    u.unemployment_rate - c.canada_unemployment_rate AS gap_vs_canada_pp
FROM unemployment u
JOIN canada as C
    ON u.ref_date = c.ref_date
    AND u.age_group = c.age_group