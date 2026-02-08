#!/usr/bin/env python
# coding: utf-8

import os
import glob
import pandas as pd
from sqlalchemy import create_engine, text
from tqdm.auto import tqdm
import click
import kagglehub

# -----------------------------
# Spotify dataset column types
# -----------------------------
dtype = {
    "track_id": "string",
    "artists": "string",
    "album_name": "string",
    "track_name": "string",
    "popularity": "Int64",
    "duration_ms": "Int64",
    "explicit": "boolean",
    "danceability": "float64",
    "energy": "float64",
    "key": "Int64",
    "loudness": "float64",
    "mode": "Int64",
    "speechiness": "float64",
    "acousticness": "float64",
    "instrumentalness": "float64",
    "liveness": "float64",
    "valence": "float64",
    "tempo": "float64",
    "time_signature": "Int64",
    "track_genre": "string"
}

parse_dates = []

# -----------------------------
# CLI options
# -----------------------------
@click.command()
@click.option('--pg_user', default='root', help='PostgreSQL user')
@click.option('--pg_password', default='root', help='PostgreSQL password')
@click.option('--pg_host', default='localhost', help='PostgreSQL host')
@click.option('--pg_port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg_database', default='spotify', help='PostgreSQL database name')
@click.option('--target_table', default='spotify_tracks', help='Target table name')
@click.option('--csv_path', default='spotify_tracks.csv', help='Local path to Spotify CSV file')
@click.option('--use_local', is_flag=True, default=False, help='Only use local CSV, do not download if missing')
@click.option('--chunksize', default=10000, type=int, help='Chunk size for data ingestion')
def run(pg_user, pg_password, pg_host, pg_port, pg_database, target_table, csv_path, use_local, chunksize):
    """
    Ingest Spotify dataset into PostgreSQL in chunks.
    
    Examples:
        # Download from KaggleHub (default if CSV doesn't exist):
        python spotify_ingest.py --pg_host spotify_postgres --pg_user spotify_user --pg_password spotify_password
        
        # Use local CSV file (download if missing):
        python spotify_ingest.py --pg_host spotify_postgres --csv_path ./my_spotify_data.csv
        
        # Use ONLY local CSV (fail if it doesn't exist):
        python spotify_ingest.py --pg_host spotify_postgres --csv_path ./my_spotify_data.csv --use_local
    """

    # -----------------------------
    # 1️⃣ Load CSV from local source or KaggleHub
    # -----------------------------
    if os.path.exists(csv_path):
        print(f"✅ Using existing CSV at {csv_path}")
    elif use_local:
        raise FileNotFoundError(f"CSV not found at {csv_path}. Set --use_local to disable automatic downloads.")
    else:
        print("📥 CSV not found locally. Downloading via KaggleHub...")
        dataset_path = kagglehub.dataset_download("maharshipandya/-spotify-tracks-dataset")

        # Search for CSV inside downloaded folder
        csv_files = glob.glob(os.path.join(dataset_path, "*.csv"))
        if not csv_files:
            csv_files = glob.glob(os.path.join(dataset_path, "**/*.csv"), recursive=True)
        if not csv_files:
            raise FileNotFoundError("Spotify CSV not found in downloaded dataset folder!")

        # Use the first CSV found
        csv_path = csv_files[0]
        print(f"✅ CSV found: {csv_path}")

    # -----------------------------
    # 2️⃣ Connect to PostgreSQL
    # -----------------------------
    print(f"🔗 Connecting to Postgres at {pg_host}:{pg_port} database '{pg_database}'...")
    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}')

    # -----------------------------
    # 3️⃣ Read CSV in chunks and ingest
    # -----------------------------
    print(f"📊 Reading CSV in chunks of {chunksize} rows...")
    df_iter = pd.read_csv(
        csv_path,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize
    )

    first = True
    total_rows = 0

    for df_chunk in tqdm(df_iter, desc="Ingesting chunks"):
        if first:
            # Create table schema
            df_chunk.head(0).to_sql(
                name=target_table,
                con=engine,
                if_exists='replace'
            )
            first = False

        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists='append',
            index=False
        )
        total_rows += len(df_chunk)

    # -----------------------------
    # 4️⃣ Final row count
    # -----------------------------
    print(f"✅ Ingestion completed for table '{target_table}'. Total rows ingested: {total_rows}")

    # Optional: verify row count in database
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {target_table}"))
        print("Total rows in database:", result.scalar())


# -----------------------------
# Entry point
# -----------------------------
if __name__ == '__main__':
    run()
