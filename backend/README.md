# Backend

Run locally:

1. Create a virtual environment and install dependencies:
   - `pip install -r requirements.txt`
2. Export environment variables:
   - `export JWT_SECRET=change-me`
   - `export REDIS_URL=redis://:password@hostname:6379/0`
   - `export SEED_TOKEN=change-me` (optional for `/seed`)
3. Start the API:
   - `uvicorn app.main:app --reload`
