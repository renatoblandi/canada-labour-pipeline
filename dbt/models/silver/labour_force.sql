SELECT
    to_date(ref_date, 'YYYY-MM') AS ref_date,
    geo,
    labour_force_characteristics,
    gender,
    age_group,
    statistics,
    data_type,
    CASE
        WHEN uom = 'Persons in thousands' THEN 'Persons'
        ELSE uom
    END AS unit,
    CASE
        WHEN scalar_factor = 'thousands' THEN NULLIF(value, '')::numeric * 1000
        ELSE NULLIF(value, '')::numeric
    END AS value,
    NULLIF(status, '') AS status,
    vector,
    loaded_at
FROM {{source('bronze', 'labour_force')}}