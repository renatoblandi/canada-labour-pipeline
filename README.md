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

## Status

Work in progress!