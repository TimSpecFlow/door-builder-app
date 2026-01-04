# Deploy SpecFlow.tech (Cloudflare Pages)

This document explains how to publish the static landing page to Cloudflare Pages and connect your `SpecFlow.tech` domain which is already managed in Cloudflare.

Quick steps

1. Create a GitHub repository and commit the `website/` folder (or push the whole repo).
2. In the Cloudflare dashboard, open **Pages** and create a new project that points to the GitHub repository and the branch (e.g., `main`).
3. Set the build settings:
   - Framework: `None` (since this is a static site)
   - Build command: (leave blank)
   - Build output directory: `website`
4. Deploy — Cloudflare will build and publish your site.
5. In the Pages project, add a custom domain: `specflow.tech`. Cloudflare will verify and automatically provision HTTPS.

DNS notes

- Because your domain is already on Cloudflare, Pages will manage the necessary DNS entries automatically. If Cloudflare asks you to add records, follow the UI guidance; normally Cloudflare Pages will add the required cname/verification records.

Local preview

Open `website/index.html` in your browser to preview locally, or serve it with a simple static server:

```powershell
# From project root
python -m http.server 8001 --directory website
# open http://127.0.0.1:8001
```

Alternative: Deploy via GitHub Pages or Netlify — but Cloudflare Pages is recommended since your domain is already managed there.

If you'd like, I can:

- Create the GitHub repo and push these files (I will need GitHub access), or
- Generate a small CI config for automatic builds, or
- Add a custom contact form (Formspree or Cloudflare Workers) to accept form submissions.
