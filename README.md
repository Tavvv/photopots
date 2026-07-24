# PhotoPots

Marketing website for the PhotoPots app — keeps work and life photos apart.

- `website/` — static site (vanilla HTML/CSS/JS), no build step
- **Hosting:** Cloudflare Pages (direct upload), project name `photopots`
- **Preview:** https://photopots.pages.dev
- **Production:** https://www.photopots.com and https://photopots.com — custom domains attached to the Pages project; go live once DNS at the registrar points to Cloudflare (CNAME `www` → `photopots.pages.dev`; apex via registrar forwarding or a Cloudflare zone)
- **Fallback:** the same files are also deployed as Workers Static Assets on worker `photopots-site` (https://photopots-site.ohhwowlabs.workers.dev)

## Deploying updates

Upload `website/` contents to Pages directly (mirrors `wrangler pages deploy`):

1. Compute each file's key as `blake3(base64(file_contents) + extension_without_dot).hexdigest()[:32]` — **not** a plain sha256; the wrong hash format is accepted on upload but the deployment then serves HTTP 500.
2. `GET /accounts/{id}/pages/projects/photopots/upload-token` → short-lived JWT.
3. `POST /pages/assets/check-missing` (Bearer JWT) → upload the missing files to `POST /pages/assets/upload` as `[{key, value: base64, metadata: {contentType}, base64: true}]`, then `POST /pages/assets/upsert-hashes` **after** uploading (upserting before upload poisons the cache).
4. Create the deployment: `POST /accounts/{id}/pages/projects/photopots/deployments` (multipart) with a `manifest` field mapping `"/path" → hash` and `branch = main`.
