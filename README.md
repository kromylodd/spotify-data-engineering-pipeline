# 🎧 Spotify Data Engineering Pipeline

A production-style, end-to-end Spotify data engineering pipeline using Spotify track metadata and audio features. This repository demonstrates a full cloud-based batch pipeline with deterministic cleaning, orchestration, cloud storage, warehouse optimization, and visualization.

This repository demonstrates: workflow orchestration with Kestra, cloud data lake + warehouse, BigQuery partitioning & clustering for query performance, deterministic cleaning with Pandas, and reproducible, idempotent flows for provisioning and ingestion.

---

**Project Goal**

- Build a reproducible, cloud-native batch pipeline that ingests raw Spotify CSV data, cleans it with Python/Pandas, stores cleaned artifacts in Google Cloud Storage (GCS), loads data into BigQuery, performs transformations and optimizations, and powers a Looker Studio dashboard.
- Demonstrate orchestration (Kestra), cloud provisioning automation, and BigQuery modeling (partitioning & clustering) for efficient analytics.

---

**Problem Description**

Raw datasets often include accidental index columns and other junk columns, causing schema drift and broken downstream queries. Manual ingestion and one-off transformations produce brittle dashboards and high query costs. This project automates ingestion, enforces schema during cleaning, version-controls cleaned artifacts in GCS, and builds an optimized analytics table in BigQuery.

---

**Solution Overview**

Kestra flows implement an end-to-end DAG that:

- Downloads the raw CSV (`download_csv`)
- Cleans with Pandas selecting an exact column list (`clean_csv`)
- Uploads the cleaned CSV to GCS (`upload_to_gcs`)
- Loads the staging table in BigQuery (`load_to_bq`)
- Creates/replaces an optimized analytics table (`transform_spotify_table`)
- Dashboard consumes the optimized table


- Flows include idempotent setup (`gcp_setup`) and KV initialization (`gcp_kv`).

---

## Architecture & Pipeline Flow

Textual flow:

Raw CSV (`dataset.csv`) → Kestra download → Pandas cleaning → GCS (cleaned CSV) → BigQuery staging → BigQuery optimized table → Looker Studio

---

## Technologies Used

- Orchestration: Kestra
- Cloud: Google Cloud Storage (GCS), BigQuery
- Language & Tools: Python (Pandas), SQL
- Local dev: Docker Compose (Kestra, Postgres, pgAdmin)
- Visualization: Google Looker Studio

---

## Pipeline Components (Kestra flows)

- `gcp_kv` — seeds KV with `GCP_PROJECT_ID`, `GCP_LOCATION`, `GCP_BUCKET_NAME`, `GCP_DATASET`.
- `gcp_setup` — creates GCS bucket and BigQuery dataset (idempotent `ifExists: SKIP`).
- `gcp_spotify_data_ingest` — main DAG:
  - `download_csv` (HTTP Download)
  - `clean_csv` (Pandas script — selects exact 20 columns, saves with `index=False`)
  - `upload_to_gcs` (GCS upload)
  - `load_to_bq` (BigQuery LOAD DATA OVERWRITE into staging)
  - `transform_spotify_table` (CREATE OR REPLACE optimized table with partitioning & clustering)

---

## Data Warehouse Optimization

- Partitioning: `spotify_tracks_clean` uses `RANGE_BUCKET(popularity, GENERATE_ARRAY(0,100,10))` to partition by popularity ranges (0–9, 10–19, ...).
- Clustering: `CLUSTER BY track_genre` to speed up genre-filtered queries.
- Benefits: reduced scanned bytes, faster aggregations, and lower cost for dashboard queries.

---

## Dashboard (Looker Studio)

Minimum visualizations:

- Top genres by average popularity (bar chart)
- Distribution of tracks across popularity buckets (histogram)

Optional tiles:

- Top artists by valence
- Audio‑feature trends by genre

<img width="895" height="433" alt="image" src="https://github.com/user-attachments/assets/49af0460-124d-4ab7-96d1-a5c2b72aac49" />



---

## Reproducibility — Setup & Run

Prerequisites:
- GCP project with BigQuery & GCS enabled
- Service account JSON with BigQuery & GCS permissions
- Docker & Docker Compose (for local Kestra + Postgres)

Local quick demo (start services):
```bash
cd pipeline
docker-compose up -d
docker-compose ps
```

Configure Kestra KV values in `gcp_kv` or via Kestra UI:
- `GCP_PROJECT_ID`, `GCP_LOCATION`, `GCP_BUCKET_NAME` (globally unique), `GCP_DATASET`.

Run Kestra flows in this order:
1. `gcp_kv`
2. `gcp_setup`
3. `gcp_spotify_data_ingest`

Verify BigQuery tables:
- Staging: `{{GCP_PROJECT_ID}}.{{GCP_DATASET}}.spotify_tracks`
- Optimized: `{{GCP_PROJECT_ID}}.{{GCP_DATASET}}.spotify_tracks_clean`

Optional local Postgres ingestion (dev):
```bash
python -m pip install -r pipeline/spotify/requirements.txt
python pipeline/spotify/spotify_ingest.py \
  --pg_user=spotify_user \
  --pg_password=spotify_password \
  --pg_host=localhost \
  --pg_database=spotify_analytics \
  --csv_path=dataset.csv
```

---

## Dataset

Source: https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset

- `dataset.csv` — sample Spotify tracks dataset with key columns:
  `track_id`, `artists`, `album_name`, `track_name`, `popularity`, `duration_ms`, `explicit`, `danceability`, `energy`, `key`, `loudness`, `mode`, `speechiness`, `acousticness`, `instrumentalness`, `liveness`, `valence`, `tempo`, `time_signature`, `track_genre`.

---

## Future Improvements

- Add `dbt` for transformations, tests, and lineage.
- Integrate data quality checks (Great Expectations) into Kestra flows.
- Add Terraform for full IaC and GitHub Actions CI to run smoke tests.
- Add streaming ingestion and ML-ready feature tables.

---

## Repository Structure

- `pipeline/docker-compose.yaml` — local services (Kestra, Postgres, pgAdmin, ingestion container)
- `pipeline/spotify/` — ingestion code, Dockerfile, requirements.txt, `spotify_ingest.py`
- `dataset.csv` — sample dataset
- `README.md` — this file

