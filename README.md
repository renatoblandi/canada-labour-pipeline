# Canada Labour Pipeline

An ELT pipeline for Statistics Canada Labour Force Survey data, built to demonstrate real data engineering practices using industry standard tools.

Data is ingested monthly from StatCan, loaded raw into PostgreSQL, and transformed through a medallion architecture using dbt. The pipeline is orchestrated with Airflow and runs fully containerized with Docker.

## Stack

- Airflow for orchestration
- dbt for transformation
- PostgreSQL for storage
- Docker for containerization
- Python for ingestion
- uv for package management

## Architecture

StatCan publishes updated Labor Force Survey data on the first Friday of every month. The pipeline downloads the full table as ZIP, extracts it, loads the raw data into the Bronze layer, and transforms it through Silver and Gold using dbt.

## Layers

- Bronze: raw data as published by StatCan, no transformations applied
- Silver: cleaned and typed data, columns renamed, scaling applied, noise dropped
- Gold: aggregated metrics

## Design decisions

### Full refresh load

Every run replaces the whole Bronze table with the latest file instead of appending only the new month.

- StatCan republishes the full history (1976 to the latest month) every month, so each file is a complete snapshot.
- Past months get revised. Seasonal factors are recalculated every year and earlier estimates can change. An incremental load would keep outdated values for those months.
- The table has ~5.5M rows, so reloading everything is cheap and avoids incremental logic.

### Where filtering happens

- Silver keeps every row. It only renames, casts, applies the scale factor and drops unused columns.
- Gold applies the business filters: only `Estimate` values (standard errors are mostly empty before 2001) and `Seasonally adjusted` data by default, which is the standard for month-to-month comparisons.

### Scaling

`VALUE` is multiplied by 1000 only when `SCALAR_FACTOR` is `thousands` (person counts). Rates are already percentages and stay as they are.

## Status

Work in progress!