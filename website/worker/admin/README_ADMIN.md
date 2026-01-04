# Admin Worker (KV) — inspect contact submissions

This admin Worker exposes a small JSON API to list, read, and delete contact submissions stored in the `CONTACTS_KV` namespace.

Security
- The Worker expects an `x-admin-token` header containing the `ADMIN_TOKEN` secret. Set this before publishing.

Endpoints
- GET `/messages` — returns up to 100 recent messages (array under `items`).
- GET `/messages/:id` — returns a single message JSON (the stored record).
- DELETE `/messages/:id` — deletes the message with the given id.

Deploy

1. Login with `wrangler login`.
2. Create or note the KV namespace id (if you haven't already):

```powershell
cd website/worker
wrangler kv:namespace create "contacts_kv"
# note the id
```

3. Edit `website/worker/admin/wrangler.toml` and set `account_id` and `YOUR_KV_NAMESPACE_ID`.

4. Add the admin token secret:

```powershell
wrangler secret put ADMIN_TOKEN
# enter a strong secret (store it securely)
```

5. Publish the admin worker:

```powershell
wrangler publish
```

6. Add a route in Cloudflare Dashboard for the admin worker (for example):

- `admin.specflow.tech/*` or `specflow.tech/api/admin/*`

Usage example (curl):

```powershell
curl -H "x-admin-token: <your-token>" https://specflow.tech/api/admin/messages
curl -H "x-admin-token: <your-token>" https://specflow.tech/api/admin/messages/<id>
```

Notes
- Keep `ADMIN_TOKEN` secret and use a secure route (e.g., `admin.specflow.tech`) with Cloudflare access controls if desired.
- If you want, I can add basic pagination to the list endpoint or a small web UI to view messages.
