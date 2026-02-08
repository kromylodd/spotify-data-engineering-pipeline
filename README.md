# spotify-data-engineering-pipeline
A production-style end-to-end data engineering pipeline using Spotify track data, demonstrating ingestion, transformation, data modeling, and analytics-ready datasets.

# 🎧 Spotify Data Engineering Pipeline

An end-to-end data engineering project that builds a scalable analytics pipeline using Spotify track metadata and audio features.

The goal of this project is to simulate a real-world data platform: ingesting raw music data, transforming it into analytics-ready models, and serving insights for downstream use cases such as dashboards and machine learning.

---

## 📌 Project Overview

This project processes a Spotify tracks dataset containing metadata and audio features (e.g. danceability, energy, tempo, popularity).

It demonstrates core data engineering concepts:
- Batch data ingestion
- Data modeling (fact & dimension tables)
- Data transformations
- Analytical queries
- Orchestration-ready structure

---

## 📂 Dataset

**Source:** Spotify Tracks Dataset  
**Size:** ~100K+ tracks  
**Format:** CSV  

**Key Fields:**
- Track name
- Artist(s)
- Album
- Release date
- Popularity score
- Audio features:
  - Danceability
  - Energy
  - Loudness
  - Tempo
  - Acousticness
  - Valence



