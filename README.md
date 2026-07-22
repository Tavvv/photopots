# PhotoPots

Marketing website for the PhotoPots app — keeps work and life photos apart.

- `website/` — static site (vanilla HTML/CSS/JS), no build step
- **Hosting:** Cloudflare Workers (Static Assets), worker name `photopots-site`
- **Preview:** https://photopots-site.ohhwowlabs.workers.dev
- **Production (pending DNS):** https://www.photopots.com — custom domain will be attached to the Worker once the `photopots.com` zone is added to the Cloudflare account

## Deploying updates

The site is deployed by uploading `website/` contents as Workers Static Assets:

1. `POST /accounts/{id}/workers/scripts/photopots-site/assets-upload-session` with a `{path: {hash, size}}` manifest (hash = first 16 bytes of SHA-256, hex)
2. Upload the returned buckets to `/accounts/{id}/workers/assets/upload?base64=true` (multipart, one part per file hash, Bearer = session JWT)
3. `PUT /accounts/{id}/workers/scripts/photopots-site` with the worker module + `assets` binding and the completion JWT

Note: Cloudflare Pages direct upload was attempted first but the Pages serving stack returned HTTP 500 for all deployments on this account (verified via Cloudflare URL Scanner), so the site runs on the Workers stack instead.
