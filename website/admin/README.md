# Admin UI — deployment & testing

This folder contains a small admin UI for browsing contact messages stored in Cloudflare KV and the client-side code that calls the Admin Worker.

Overview
- UI files: `index.html`, `admin.css`, `app.js`
- Admin Worker (server): `website/worker/admin/index.js` — exposes endpoints to list, get and delete contact records from the `CONTACTS_KV` namespace. The worker expects an admin token in the `x-admin-token` header.

Prerequisites
- Cloudflare account with access to the zone for your site (e.g. `specflow.tech`).
- `wrangler` CLI installed and authenticated: `npm install -g wrangler` then `wrangler login`.

Deployment checklist
1. Create a KV namespace and note the returned id:

   ```powershell
   cd website/worker
   wrangler kv:namespace create "contacts_kv"
   ```

2. Update the `wrangler.toml` in the worker directory:
   - Set your `account_id`.
   - Add the `kv_namespaces` entry with the `id` returned by step 1 and the binding name `CONTACTS_KV`.

3. Set the admin token (keep this secret):

   ```powershell
   cd website/worker/admin
   wrangler secret put ADMIN_TOKEN
   # enter a strong token when prompted
   ```

4. Publish the Admin Worker (from `website/worker/admin`):

   ```powershell
   wrangler publish
   ```

5. Configure routes in Cloudflare (either in `wrangler.toml` or the Cloudflare dashboard) so the admin worker is reachable at a path like:

   - `https://specflow.tech/api/admin/*`

   And the contact worker (which writes KV entries) at:

   - `https://specflow.tech/api/contact`

Notes
- The Admin Worker expects the admin token in the `x-admin-token` header for all admin requests. Keep the token private.
- If you change the worker route, update the `base` URL in `website/admin/app.js` (currently `'/api/admin/messages'`).

Testing the deployed worker
- List messages:

  ```bash
  curl -H "x-admin-token: YOUR_TOKEN" https://specflow.tech/api/admin/messages
  ```

- Get a single message (replace `<key>`):

  ```bash
  curl -H "x-admin-token: YOUR_TOKEN" https://specflow.tech/api/admin/messages/<key>
  ```

- Delete a message:

  ```bash
  curl -X DELETE -H "x-admin-token: YOUR_TOKEN" https://specflow.tech/api/admin/messages/<key>
  ```

Local testing (developer flow)
- You can run `wrangler dev` from the worker directory to test the worker locally. If you serve the `website/admin/index.html` locally (e.g. `python -m http.server --directory website 8001`) the admin UI can call the local worker endpoint created by `wrangler dev`.
- Alternatively, use `curl` to test the endpoints directly while developing.

Security & production notes
- Use a strong `ADMIN_TOKEN` and rotate it if you suspect compromise.
- Consider IP allowlisting or Cloudflare Access in front of the admin endpoints for additional protection.
- For production workloads, use durable storage (e.g., a managed DB) if you have strict retention/querying requirements — KV is good for low-volume messages and simple admin workflows.

If you want, I can run the commit & push for this README now and show the commit hash.
