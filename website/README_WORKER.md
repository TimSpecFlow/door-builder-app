# Cloudflare Worker: Contact form forwarding (SendGrid)

This Worker accepts POST requests with JSON `{ name, email, message }` and stores submissions in a Cloudflare KV namespace (binding name: `CONTACTS_KV`).

Prerequisites

- A Cloudflare account with your domain managed on Cloudflare.
- `wrangler` CLI installed locally: `npm install -g wrangler` or follow https://developers.cloudflare.com/workers/cli-wrangler/install

Setup & deploy (KV)

1. Login to Cloudflare with Wrangler (this opens a browser):

```powershell
wrangler login
```

2. Create a KV namespace (run in project root or `website/worker`):

```powershell
cd website/worker
wrangler kv:namespace create "contacts_kv"
# Example output will include an id; note it (e.g. 123abc...)
```

3. Update `worker/wrangler.toml` with your account id and the KV namespace id. In `worker/wrangler.toml` replace `YOUR_ACCOUNT_ID` and `YOUR_KV_NAMESPACE_ID` with the values from Cloudflare.

4. Publish the Worker:

```powershell
wrangler publish
```

5. Route the Worker to your domain (recommended):

- In the Cloudflare dashboard, go to Workers → Routes and add a route such as `specflow.tech/api/contact` pointing to the published Worker.

Using the Worker from the site

- The landing page posts JSON to `/api/contact`. Once the Worker is routed at `specflow.tech/api/contact`, the relative path resolves and submissions will be stored in KV.

Inspecting stored messages

- You can read stored entries via the Cloudflare dashboard's KV preview, or call the Worker (or write another admin Worker) to list/retrieve messages.

Notes

- This avoids using an external email provider — messages are stored safely in your Cloudflare KV. If you later want to forward to email, we can add a scheduled Worker or a small admin endpoint that reads new entries and emails them.
