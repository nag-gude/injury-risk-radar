# Injury Risk Radar

Injury Risk Radar helps athletes and coaches spot overuse risk early by turning
daily training and recovery logs into a clear risk score and actionable
prevention tips.

## Features

- Daily training and recovery logging
- Injury risk scoring with recommendations
- Dashboard with trends and recent logs
- Coach-ready summaries (team aggregation ready)

## Architecture

The system is a full-stack web app with a FastAPI backend and a static frontend.
Data is stored in Redis (Vercel KV compatible) for rapid reads/writes.

Architecture diagram: `docs/architecture.svg`

## Tech Stack

- Backend: FastAPI, Python
- Frontend: HTML, CSS, JavaScript, Chart.js
- Data store: Redis / Vercel KV
- Hosting: Vercel (full-stack), optional GCP for backend

## Quick Start

1. Install backend deps:
   - `pip install -r backend/requirements.txt`
2. Set env vars:
   - `export JWT_SECRET=change-me`
   - `export REDIS_URL=redis://:password@hostname:6379/0`
3. Run backend:
   - `uvicorn app.main:app --reload --app-dir backend`
4. Open `frontend/index.html` in a browser.

## Demo Data

Use the seed endpoint to populate a demo user and logs:

- `POST /api/seed`
- Optional header: `X-Seed-Token: <your token>`

Returns demo credentials in the response.
