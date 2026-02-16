import os
import pandas as pd
from sqlalchemy import create_engine, text
from tqdm.auto import tqdm
import click

# Define ONLY the columns we want in the DB
COLUMNS_TO_KEEP = [
    "track_id", "artists", "album_name", "track_name", "popularity", 
    "duration_ms", "explicit", "danceability", "energy", "key", 
    "loudness", "mode", "speechiness", "acousticness", "instrumentalness", 
    "liveness", "valence", "tempo", "time_signature", "track_genre"
]

@click.command()
@click.option('--pg_user', default='spotify_user')
@click.option('--pg_password', default='spotify_password')
@click.option('--pg_host', default='localhost')
@click.option('--pg_database', default='spotify_analytics')
@click.option('--csv_path', default='dataset.csv')
def run(pg_user, pg_password, pg_host, pg_database, csv_path):
    # 1. Connection
    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:5432/{pg_database}')

    # 2. FORCE DROP TABLE (Ensures junk columns are physically removed)
    with engine.connect() as conn:
        print("🗑️ Dropping old table to reset schema...")
        conn.execute(text("DROP TABLE IF EXISTS spotify_tracks;"))
        conn.commit()

    # 3. Read and Ingest
    print(f"📊 Reading {csv_path} (Filtering columns)...")
    df_iter = pd.read_csv(
        csv_path,
        usecols=COLUMNS_TO_KEEP, # This prevents 'index' or 'Unnamed: 0' from entering memory
        chunksize=10000
    )

    for df_chunk in tqdm(df_iter):
        df_chunk = df_chunk.dropna(subset=['track_id'])
        # index=False ensures Pandas doesn't create a 'level_0' or 'index' column in SQL
        df_chunk.to_sql('spotify_tracks', engine, if_exists='append', index=False)

    print("✅ Ingestion complete. Check pgAdmin - the junk columns are gone!")

if __name__ == '__main__':
    run()