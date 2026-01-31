# Backend

Run locally:

1. Create a virtual environment and install dependencies:
   - `pip install -r requirements.txt`
2. Export environment variables:
   - `export JWT_SECRET=change-me`
   - `export FIRESTORE_PROJECT=your-gcp-project-id`
3. Start the API:
   - `uvicorn app.main:app --reload`
