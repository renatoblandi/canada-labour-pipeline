SELECT
    vector,
    ref_date,
    COUNT(*) AS n_rows
FROM {{ ref('labour_force') }}
GROUP BY vector, ref_date
HAVING COUNT(*) > 1