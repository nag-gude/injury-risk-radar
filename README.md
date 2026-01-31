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


# Inspiration
Sports injuries often come from overuse and missed recovery signals. We wanted a simple, daily check‑in that translates training load and wellness into clear, preventative guidance athletes and coaches can act on.

# What it does
Injury Risk Radar lets users log training duration, intensity, soreness, sleep, and rest days. It calculates a risk score (Low/Moderate/High), shows trend charts, and provides actionable recommendations to reduce injury risk.

# How we built it
We built a FastAPI backend with JWT auth and a risk‑scoring engine, a static web frontend with Chart.js for visual trends, and a Redis/Vercel KV store for fast persistence. The app is deployed as a full‑stack Vercel project with a /api backend route.

# Challenges we ran into
- Adapting the backend for serverless execution on Vercel and fixing import/path issues.
- Replacing Firebase with Vercel KV and updating data access patterns.
- Handling dependency/runtime quirks (bcrypt and Python packaging).
- Ensuring the dashboard charts update cleanly without duplicate canvas usage.

# Accomplishments that we're proud of
- A working end‑to‑end MVP with auth, logging, risk scoring, and recommendations.
- A lightweight UI that supports quick daily input and clear risk visualization.
- A deployment setup that runs full‑stack on Vercel with minimal infrastructure.

# What we learned
We learned how to adapt a FastAPI app to serverless deployment, use Redis/Vercel KV effectively, and design a risk scoring approach that’s transparent and easy to explain to non‑technical users.

# What’s next for Injury Risk Radar
- Add wearable integrations and automatic data ingestion.
- Improve risk modeling with personalized ML and sport‑specific patterns.
- Expand coach/team analytics with aggregate dashboards.
- Add notifications and scheduled reminders for consistent logging.
