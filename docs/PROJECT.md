# Project Documentation

## Overview

Injury Risk Radar is a decision-support tool that helps athletes and coaches
identify elevated injury risk before it happens. It uses daily training load
and recovery indicators to compute a risk score (Low, Moderate, High) and
provides simple, preventative recommendations.

## Architecture

The application is a full-stack web app:

- **Frontend**: static web UI (HTML/CSS/JS) that calls REST endpoints.
- **Backend**: FastAPI app with authentication, logging, risk scoring, and
  recommendations.
- **Data store**: Redis (Vercel KV compatible) to persist users and logs.

Architecture image: `docs/architecture.svg`

## Core Data Flow

1. User registers and logs in.
2. Daily log submitted (duration, intensity, soreness, sleep, rest day).
3. Backend calculates training load and stores the log.
4. Dashboard aggregates logs, computes risk summary, and returns insights.

## Risk Engine

The risk engine computes:

- **Acute load**: average training load over last 7 days.
- **Chronic load**: average training load over last 28 days.
- **Load ratio**: acute / chronic load.
- **Fatigue score**: soreness, sleep quality, and rest-day signal.

These signals are combined into a 0–100 score and mapped to Low/Moderate/High
with actionable guidance.

## Technologies Used

- **Python / FastAPI** for API endpoints and business logic.
- **Redis / Vercel KV** for data persistence.
- **JWT** for stateless authentication.
- **HTML, CSS, JavaScript** for the frontend.
- **Chart.js** for trend visualization.
- **Vercel** for hosting (full-stack).

## Deployment

See `DEPLOYMENT.md` for GCP and Vercel deployment instructions.

## Demo + Testing

- Use `POST /api/seed` to generate demo data.
- Use the frontend dashboard to view trends and risk insights.
