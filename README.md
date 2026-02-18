🎧 Spotify Data Engineering Pipeline

A production-style end-to-end data engineering pipeline that ingests, transforms, and analyzes Spotify track data to produce analytics-ready datasets in a cloud data warehouse.

This project demonstrates a real-world data platform architecture including data ingestion, cleaning, transformation, optimization, orchestration, and visualization.

🚀 Project Goal

The goal of this project is to simulate a modern data engineering workflow by building an automated pipeline that:

ingests raw music data

cleans and standardizes schemas

stores data in a cloud data warehouse

optimizes storage for analytics queries

serves insights through dashboards

The pipeline transforms raw Spotify track metadata into structured datasets that enable efficient analysis of music trends and audio characteristics.

❗ Problem Description
Problem

Music platforms generate large volumes of track metadata that must be efficiently stored, processed, and analyzed. However, raw datasets often contain inconsistent schemas, redundant columns, and are not optimized for analytical queries.

Without proper ingestion pipelines and warehouse optimization, querying music features such as popularity, genre distribution, and audio characteristics becomes slow and inefficient.

Solution

This project builds an automated data pipeline that:

ingests Spotify track data from external sources

removes unnecessary and inconsistent columns

validates and standardizes the dataset

stores data in an optimized cloud data warehouse

enables fast analytical queries

supports dashboard visualization

The data is stored in a partitioned and clustered table to improve query performance and reduce scan costs.

Use Cases

The system enables analysts to explore:

track popularity distribution

genre trends

audio feature relationships

music characteristics across tracks

🏗 Architecture
Pipeline Flow

Data Source (CSV)
      ↓
Download
      ↓
Data Cleaning (Python / Pandas)
      ↓
Google Cloud Storage (Data Lake)
      ↓
BigQuery Raw Table
      ↓
Transformation & Optimization
      ↓
Analytics Table
      ↓
Dashboard (Looker Studio)

Technologies Used

Workflow orchestration → Kestra

Cloud platform → Google Cloud

Data lake → Google Cloud Storage

Data warehouse → Google BigQuery

Data processing → Python, Pandas

Visualization → Google Looker Studio

⚙️ Pipeline Components
1. Data Ingestion

Dataset downloaded from GitHub

Workflow orchestrated using Kestra

Raw data stored in Google Cloud Storage

2. Data Cleaning

Python and Pandas are used to:

remove unnecessary columns (index, Unnamed: 0)

enforce schema consistency

filter invalid records

produce clean CSV output

3. Data Warehouse Loading

Cleaned data is loaded into BigQuery:

structured schema

analytics-ready format

query optimized storage

4. Data Transformation & Optimization

A transformed table is created for analytics:

filtered valid records

partitioned by popularity range

clustered by track genre

Optimization Strategy

Partitioning by popularity → improves ranking queries

Clustering by genre → speeds filtering and aggregation queries

This reduces query cost and improves performance.

📂 Dataset
Source

Spotify Tracks Dataset (public dataset)

Size

~100K+ tracks

Format

CSV

Key Fields

track_id

artists

album_name

track_name

popularity

duration_ms

danceability

energy

loudness

acousticness

valence

tempo

track_genre

The dataset contains metadata and audio features describing musical characteristics of tracks.

📊 Dashboard

A dashboard was built in Google Looker Studio to visualize analytics results.

Visualizations

Track Distribution by Genre — shows number of tracks per genre

Average Popularity by Genre — compares genre popularity

The dashboard enables exploration of music trends and audio characteristics.

(Add screenshot here)

🔄 Reproducibility
Prerequisites

Google Cloud account

Docker installed

Kestra running locally

Google Cloud Storage bucket

BigQuery dataset

Service account credentials

Setup Instructions
1. Clone repository

git clone https://github.com/kromylodd/spotify-data-engineering-pipeline
cd spotify-data-engineering-pipeline

2. Configure Google Cloud

Create a project

Create Google Cloud Storage bucket

Create BigQuery dataset

Create service account

Download credentials JSON

3. Start Kestra
   
docker compose up

4. Configure Kestra KV Store

Add: 
GCP_CREDS
GCP_PROJECT_ID
GCP_BUCKET_NAME
GCP_DATASET
GCP_LOCATION

5. Run Pipeline

Execute: 

gcp_spotify_data_ingest

Output

Cleaned dataset stored in Google Cloud Storage

Raw table in BigQuery

Optimized analytics table in BigQuery

Looker Studio dashboard

✅ Project Features

End-to-end batch data pipeline

Workflow orchestration

Data cleaning and validation

Cloud data warehouse storage

Query optimization (partitioning + clustering)

Analytics dashboard

Fully reproducible setup

📈 Future Improvements

Infrastructure as Code (Terraform)

dbt transformation layer

Streaming ingestion pipeline

Machine learning features
