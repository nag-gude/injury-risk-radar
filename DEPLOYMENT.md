# Deployment (Vercel + Custom Domain)

## Full-stack on Vercel (frontend + FastAPI)

1. **Install Vercel CLI** (optional):
   - `npm i -g vercel`

2. **Set environment variables** in Vercel:
   - `JWT_SECRET`
   - `KV_URL` or `REDIS_URL` (Vercel KV provides `KV_URL`)
   - `SEED_TOKEN` (optional, protects `/seed`)

3. **Deploy**:
   - From the repo root: `vercel --prod`

## Custom Domain: `cloudaimlops.com`

1. **Add domain** in Vercel project settings:
   - Settings → Domains → Add `cloudaimlops.com`
2. **Update DNS** at your domain registrar:
   - Add the Vercel A/CNAME records shown in the Vercel UI.
3. **Verify**:
   - Wait for DNS to propagate, then confirm in Vercel.

## Notes
- The frontend defaults to `/api` for the FastAPI base path on Vercel.
- If using Vercel KV, connect it to the project and copy `KV_URL` to env vars.
- To seed demo data, call `POST /api/seed` with header `X-Seed-Token` if enabled.
