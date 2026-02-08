cd /workspaces/spotify-data-engineering-pipeline/pipeline
docker-compose down

cd /workspaces/spotify-data-engineering-pipeline/pipeline
docker-compose up -d

# Check what's running
docker-compose ps

# View logs
docker-compose logs -f

# Stop without removing containers
docker-compose stop

# Start already-existing containers
docker-compose start

# If you are using Docker Compose and have a PostgreSQL service named `spotify_postgres` in the same network, you can run the container with the following command to connect to the PostgreSQL service:

# Option 1: Download from KaggleHub (default)
docker run --rm \
  --network pipeline_data-network \
  spotify-ingest \
  --pg_user=spotify_user \
  --pg_password=spotify_password \
  --pg_host=spotify_postgres \
  --pg_port=5432 \
  --pg_database=spotify_analytics

# Option 2: Use local CSV file (if it exists in the container)
# docker run --rm \
#   --network pipeline_data-network \
#   -v /path/to/local/csv:/app \
#   spotify-ingest \
#   --pg_user=spotify_user \
#   --pg_password=spotify_password \
#   --pg_host=spotify_postgres \
#   --pg_port=5432 \
#   --pg_database=spotify_analytics \
#   --csv_path=/app/your_spotify_data.csv

# Option 3: Use ONLY local CSV (fail if it doesn't exist locally)
# docker run --rm \
#   --network pipeline_data-network \
#   -v /path/to/local/csv:/app \
#   spotify-ingest \
#   --pg_user=spotify_user \
#   --pg_password=spotify_password \
#   --pg_host=spotify_postgres \
#   --pg_port=5432 \
#   --pg_database=spotify_analytics \
#   --csv_path=/app/your_spotify_data.csv \
#   --use_local