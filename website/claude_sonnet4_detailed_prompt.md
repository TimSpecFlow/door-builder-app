You are a full-stack project scaffolding assistant. Recreate the following project structure and content exactly. Produce all files and contents so the repository is runnable locally and deployable to Cloudflare Pages + Workers. Provide clear steps for the user to finish the Cloudflare configuration (account id, kv id, secret).

Project goals (short)
- Landing page for SpecFlow.tech with a contact form that posts to `/api/contact`.
- Django starter with an `/api/estimate/` POST endpoint that returns JSON estimates for a door spec.
- React (Vite) builder app that posts to `/api/estimate/` and updates live.
- Cloudflare Worker `website/worker/index.js` that accepts `POST /api/contact` and writes messages to a KV namespace bound as `CONTACTS_KV`.
- Cloudflare Admin Worker `website/worker/admin/index.js` exposing:
  - GET /messages -> list keys and metadata
  - GET /messages/:key -> return stored message JSON
  - DELETE /messages/:key -> delete entry
  - Admin worker requires `x-admin-token` header checked against an `ADMIN_TOKEN` secret
- Admin static UI `website/admin/` that lists messages and allows view/delete. Token input must not be sent in query strings; use `x-admin-token` header.

Repo layout to produce (exact key paths)
- website/index.html
- website/styles.css
- website/admin/index.html
- website/admin/admin.css
- website/admin/app.js
- website/admin/run-local.ps1
- website/worker/index.js
- website/worker/wrangler.toml
- website/worker/admin/index.js
- website/worker/admin/wrangler.toml
- website/worker/admin/README_ADMIN.md
- frontend/package.json
- frontend/vite.config.js
- frontend/src/App.jsx
- frontend/src/main.jsx
- frontend/README.md
- door_builder/manage.py
- door_builder/door_builder/settings.py
- door_builder/door_builder/urls.py
- door_builder/catalog/apps.py
- door_builder/catalog/views.py
- door_builder/catalog/serializers.py
- door_builder/requirements.txt
- Root README.md

Important implementation notes
- All HTTP endpoints must use JSON; Workers must accept JSON body and return JSON responses.
- KV keys should be `contact:<timestamp>-<random>` and store JSON with fields: `name`, `email`, `message`, `created`.
- Admin Worker must check `x-admin-token` header: if not present or wrong, return HTTP 401.
- Provide example curl commands for:
  - Submitting a contact
  - Listing messages (admin)
  - Getting message (admin)
  - Deleting message (admin)
- Add `run-local.ps1` under `website/admin/` to serve `website` with `python -m http.server` and optionally run `wrangler dev` for the admin worker when invoked with `-StartWrangler`.
- Add a `run-dev.ps1` at repo root that starts Django dev server (in venv), starts Vite dev server for frontend, and a static server for website simultaneously (or provide clear separate commands to do so).

Security & secrets
- Do not hardcode secrets. Use `wrangler secret put ADMIN_TOKEN` to set the admin token; in files use instruction placeholders and use `YOUR_ADMIN_TOKEN_PLACEHOLDER` only in docs.
- Add a short note on using Cloudflare Access or IP allowlist for the admin route.

Testing & deployment checklist (exact commands)
- How to: install Node/Python, create venv, install pip requirements, npm install in frontend, run servers locally.
- How to: `wrangler login`, `wrangler kv namespace create "contacts_kv"` (or `wrangler kv:namespace create` syntax depending on wrangler), copy the returned id.
- How to edit `website/worker/wrangler.toml` and `website/worker/admin/wrangler.toml` to set `account_id` and put KV id.
- How to set `ADMIN_TOKEN` and publish both Workers (`wrangler publish`) and set routes in the Cloudflare Dashboard.
- How to deploy Pages (connect repo, build output directory=`website`).
- Provide rollback and log inspection commands for Workers.

Deliver the output in the following structured order:
1. Root README.md (QuickStart)
2. File tree (bulleted)
3. Full file contents for each path above, each labelled with the path
4. Exact PowerShell commands for local dev, KV creation, secret setting, publish, and test curl commands
5. Minimal smoke tests (what success responses look like)
6. Notes about quotas and cost and recommended usage for production

Edge cases
- If Cloudflare `wrangler` version differences exist, include both `wrangler kv namespace create` and `wrangler kv:namespace create` forms and instruct the user to run the correct one for their `wrangler -v`.
- If the admin secret is missing and the admin UI tries to call the admin worker, return a clear 401 with {"error":"unauthorized"}.

When you produce the files, make sure:
- All file paths use forward slashes.
- Files use consistent indentation and modern JS (ESM).
- Include `package.json` and `requirements.txt`.
- Include minimal ESLint/prettier config only if necessary; prefer simple readable code.

Finish by asking: "Do you want this committed to a new GitHub repo and pushed (I can open a PR describing the changes)?" If account credentials are needed, request them interactively (do not attempt to use them automatically).

How I recommend you run the prompt
- Use the Detailed prompt for Claude Sonnet 4. It should produce a full file tree and file contents.
- Ask Claude to return files as a downloadable archive if the interface supports it.
- After Claude returns files, run the QuickStart commands I gave above and paste any errors back here for help.

If you want, I can now:
- Convert the Detailed prompt into a single file in your repo (apply_patch) and commit it, or
- Run through the first publish steps interactively with you.

Which would you like next?
