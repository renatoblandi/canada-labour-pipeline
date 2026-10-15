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
)

SELECT *
FROM unemployment