# Claude Opus 4.5 — Door Builder Project Reproduction Prompt

Paste the entire content below into Claude Opus 4.5. It will reproduce the full project.

---

You are a full-stack project scaffolding assistant. Recreate the following project structure and content **exactly**. Produce all files and contents so the repository is runnable locally and deployable to Cloudflare Pages + Workers. Provide clear steps for the user to finish the Cloudflare configuration (account id, KV id, secret).

---

## Project goals (short)

- **Landing page** for SpecFlow.tech with a contact form that posts JSON to `/api/contact`.
- **Django starter** with an `/api/estimate/` POST endpoint that returns JSON estimates for a door spec.
- **React (Vite) builder app** that posts to `/api/estimate/` and shows live price updates.
- **Cloudflare Worker** (`website/worker/index.js`) that accepts `POST /api/contact` and writes messages to a KV namespace bound as `CONTACTS_KV`.
- **Cloudflare Admin Worker** (`website/worker/admin/index.js`) exposing:
  - `GET /messages` → list keys/metadata
  - `GET /messages/:id` → return stored message JSON
  - `DELETE /messages/:id` → delete entry
  - Admin worker requires `x-admin-token` header checked against an `ADMIN_TOKEN` secret.
- **Admin static UI** (`website/admin/`) that lists messages and allows view/delete. Token must be sent via `x-admin-token` header (never in query strings).

---

## Repo layout (exact key paths)

```
door-builder-app/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── README.md
├── catalog/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── door_builder/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── README.md
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       └── styles.css
└── website/
    ├── index.html
    ├── styles.css
    ├── README_DEPLOY.md
    ├── README_WORKER.md
    ├── admin/
    │   ├── index.html
    │   ├── admin.css
    │   ├── app.js
    │   └── run-local.ps1
    └── worker/
        ├── index.js
        ├── wrangler.toml
        └── admin/
            ├── index.js
            ├── wrangler.toml
            └── README_ADMIN.md
```

---

## Full file contents

Produce each file **exactly** as shown below.

---

### manage.py

```python
#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'door_builder.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django. Is it installed?") from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
```

---

### requirements.txt

```
Django>=4.2
djangorestframework>=3.14
gunicorn
```

---

### README.md

```markdown
# Door Builder - Django Starter

Minimal Django starter for the Door Builder app.

## What you get
- Django project `door_builder`
- App `catalog` with an `/api/estimate/` endpoint
- `requirements.txt` and `.gitignore`

## Quick start (PowerShell)

```powershell
cd door-builder-app
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## API example

POST `http://127.0.0.1:8000/api/estimate/`

```json
{
  "width": 36,
  "height": 80,
  "material": "wood",
  "hardware": ["hinges","handle"]
}
```

Response:
```json
{ "estimate": 123.45 }
```

## Next steps
- Create a React frontend or Django templates
- Add Stripe integration
- Expand product models
```

---

### catalog/__init__.py

```python
# catalog app
```

---

### catalog/admin.py

```python
from django.contrib import admin
from .models import DoorSpec


@admin.register(DoorSpec)
class DoorSpecAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_at')
```

---

### catalog/apps.py

```python
from django.apps import AppConfig


class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'
```

---

### catalog/models.py

```python
from django.db import models


class DoorSpec(models.Model):
    width = models.FloatField(help_text='Width in inches')
    height = models.FloatField(help_text='Height in inches')
    material = models.CharField(max_length=50, default='wood')
    finish = models.CharField(max_length=50, blank=True)
    hardware = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Door {self.width}x{self.height} ({self.material})"
```

---

### catalog/serializers.py

```python
from rest_framework import serializers


class EstimateSerializer(serializers.Serializer):
    width = serializers.FloatField(min_value=0.1)
    height = serializers.FloatField(min_value=0.1)
    material = serializers.CharField(default='wood')
    hardware = serializers.ListField(child=serializers.CharField(), required=False)
```

---

### catalog/urls.py

```python
from django.urls import path
from .views import EstimateView

urlpatterns = [
    path('estimate/', EstimateView.as_view(), name='estimate'),
]
```

---

### catalog/views.py

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EstimateSerializer


class EstimateView(APIView):
    """Return a simple price estimate based on area and options."""

    MATERIAL_MULTIPLIERS = {
        'wood': 1.0,
        'steel': 1.5,
        'fiberglass': 1.2,
    }

    HARDWARE_COSTS = {
        'hinges': 10,
        'handle': 25,
        'lockset': 40,
    }

    def post(self, request):
        ser = EstimateSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

        data = ser.validated_data
        width = data['width']
        height = data['height']
        material = data.get('material', 'wood')
        hardware = data.get('hardware', [])

        # Simple area-based pricing (square feet)
        area_sqft = (width * height) / 144.0
        base_price_per_sqft = 50.0
        multiplier = self.MATERIAL_MULTIPLIERS.get(material.lower(), 1.0)

        price = area_sqft * base_price_per_sqft * multiplier

        # Add hardware costs
        for h in hardware:
            price += self.HARDWARE_COSTS.get(h.lower(), 0)

        return Response({'estimate': round(price, 2)})
```

---

### door_builder/__init__.py

```python
# door_builder project package
```

---

### door_builder/settings.py

```python
"""Django settings for door_builder project (minimal)."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET', 'change-me-for-prod')

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'catalog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'door_builder.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'door_builder.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

---

### door_builder/urls.py

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('catalog.urls')),
]
```

---

### door_builder/wsgi.py

```python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'door_builder.settings')
application = get_wsgi_application()
```

---

### frontend/index.html

```html
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Door Builder</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

---

### frontend/package.json

```json
{
  "name": "door-builder-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "18.2.0",
    "react-dom": "18.2.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.0.0",
    "vite": "5.0.0"
  }
}
```

---

### frontend/vite.config.js

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://127.0.0.1:8000'
    }
  }
})
```

---

### frontend/README.md

```markdown
# Door Builder Frontend

Small React single-page app (Vite) that calls the Django backend `/api/estimate/` endpoint and shows live price estimates.

## Quick start (PowerShell)

```powershell
cd frontend
npm install
npm run dev
```

The dev server proxies `/api` to the local Django server (configured in `vite.config.js`).
```

---

### frontend/src/main.jsx

```jsx
import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import './styles.css'

const container = document.getElementById('root')
const root = createRoot(container)
root.render(<App />)
```

---

### frontend/src/App.jsx

```jsx
import React, { useState, useEffect, useCallback } from 'react'

function useDebouncedEffect(fn, deps, delay) {
  useEffect(() => {
    const id = setTimeout(() => fn(), delay)
    return () => clearTimeout(id)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [...(deps || []), delay])
}

export default function App() {
  const [width, setWidth] = useState(36)
  const [height, setHeight] = useState(80)
  const [material, setMaterial] = useState('wood')
  const [hardware, setHardware] = useState({ hinges: true, handle: true, lockset: false })
  const [estimate, setEstimate] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const hardwareList = Object.keys(hardware)

  const compute = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const body = {
        width: Number(width),
        height: Number(height),
        material,
        hardware: hardwareList.filter(h => hardware[h])
      }

      const res = await fetch('/api/estimate/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      })
      if (!res.ok) throw new Error('Estimate request failed')
      const data = await res.json()
      setEstimate(data.estimate)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [width, height, material, hardware])

  // debounce rapid input changes
  useDebouncedEffect(() => { compute() }, [width, height, material, hardware], 350)

  function toggleHardware(name) {
    setHardware(h => ({ ...h, [name]: !h[name] }))
  }

  return (
    <div className="container">
      <h1>Door Spec Builder</h1>
      <div className="row">
        <label>Width (in)</label>
        <input type="number" value={width} onChange={e => setWidth(e.target.value)} />
      </div>
      <div className="row">
        <label>Height (in)</label>
        <input type="number" value={height} onChange={e => setHeight(e.target.value)} />
      </div>
      <div className="row">
        <label>Material</label>
        <select value={material} onChange={e => setMaterial(e.target.value)}>
          <option value="wood">Wood</option>
          <option value="steel">Steel</option>
          <option value="fiberglass">Fiberglass</option>
        </select>
      </div>
      <div className="row">
        <label>Hardware</label>
        <div className="checkboxes">
          {hardwareList.map(h => (
            <label key={h} className="checkbox">
              <input type="checkbox" checked={!!hardware[h]} onChange={() => toggleHardware(h)} /> {h}
            </label>
          ))}
        </div>
      </div>

      <div className="estimate">
        {loading ? (<div className="muted">Calculating...</div>) : error ? (<div className="error">{error}</div>) : (
          <div className="price">Estimate: {estimate != null ? `$${estimate}` : '—'}</div>
        )}
      </div>
    </div>
  )
}
```

---

### frontend/src/styles.css

```css
:root{--bg:#f7f7fb;--card:#fff;--accent:#0f62fe}
body{font-family:Inter,Segoe UI,Arial,sans-serif;background:var(--bg);margin:0;padding:24px}
.container{max-width:760px;margin:0 auto;background:var(--card);padding:20px;border-radius:8px;box-shadow:0 6px 18px rgba(12,18,26,0.08)}
.row{display:flex;align-items:center;gap:12px;margin:10px 0}
label{width:120px;font-weight:600}
input[type=number],select{flex:1;padding:8px;border-radius:6px;border:1px solid #ddd}
.checkboxes{display:flex;gap:12px}
.estimate{margin-top:18px;font-size:1.15rem}
.price{font-weight:700;color:var(--accent)}
.muted{color:#666}
.error{color:#b00020}
```

---

### website/index.html

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>SpecFlow — Door hardware specs & sales (Phoenix / Scottsdale)</title>
    <meta name="description" content="SpecFlow: custom door hardware specs and sales serving Phoenix & Scottsdale. Build, estimate, and order quality door hardware." />
    <link rel="stylesheet" href="styles.css">
    <meta name="theme-color" content="#0f62fe" />
  </head>
  <body>
    <header class="site-header">
      <div class="wrap">
        <a class="brand" href="/">
          <svg width="36" height="36" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <rect x="3" y="3" width="18" height="18" rx="3" fill="#0f62fe" />
            <path d="M7 13h10M7 8h10" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span class="title">SpecFlow</span>
        </a>
        <nav class="nav">
          <a href="#how">How it works</a>
          <a href="#services">Services</a>
          <a class="cta" href="mailto:Matt@SpecFlow.Tech">Contact</a>
        </nav>
      </div>
    </header>

    <main>
      <section class="hero">
        <div class="wrap hero-grid">
          <div>
            <h1>Precision door hardware specs — built for Phoenix & Scottsdale</h1>
            <p class="lead">Design and order finished door hardware with accurate estimates and local delivery. Fast quotes, custom options, and professional advice.</p>
            <div class="actions">
              <a class="primary" href="/frontend/index.html">Try the Builder</a>
              <a class="secondary" href="#contact">Get a Quote</a>
            </div>
          </div>
          <div class="mock">
            <div class="mock-card">
              <div class="mock-line"></div>
              <div class="mock-line short"></div>
              <div class="mock-price">Estimate: <strong>$1,235</strong></div>
            </div>
          </div>
        </div>
      </section>

      <section id="how" class="wrap section">
        <h2>How it works</h2>
        <div class="grid">
          <article>
            <h3>1 — Build</h3>
            <p>Use our spec builder to enter door dimensions, materials, hardware and finishes.</p>
          </article>
          <article>
            <h3>2 — Estimate</h3>
            <p>Get an instant, transparent price estimate and lead time tailored to your options.</p>
          </article>
          <article>
            <h3>3 — Order</h3>
            <p>Place your order online or speak to our local Phoenix team for installation coordination.</p>
          </article>
        </div>
      </section>

      <section id="services" class="wrap section alt">
        <h2>Services</h2>
        <ul class="services">
          <li>
            <h4>Custom hardware specs</h4>
            <p>Doors, hinges, locksets and finishes — tailored to your project and code requirements.</p>
          </li>
          <li>
            <h4>Local Pickup & Delivery</h4>
            <p>Fast delivery across Phoenix and Scottsdale with reliable lead times.</p>
          </li>
          <li>
            <h4>Commercial & Residential</h4>
            <p>Projects of all sizes — from single doors to multi-site rollouts.</p>
          </li>
        </ul>
      </section>

      <section id="contact" class="wrap section contact">
        <h2>Contact</h2>
        <p>Questions or want a custom quote? Email us or call — we respond quickly during business hours.</p>
        <div class="contact-grid">
          <div>
            <p><strong>Email</strong><br><a href="mailto:Matt@SpecFlow.Tech">Matt@SpecFlow.Tech</a></p>
            <p><strong>Phone</strong><br><a href="tel:+14805551234">(480) 555-1234</a></p>
            <p><strong>Service Area</strong><br>Phoenix & Scottsdale, AZ</p>
          </div>
          <div>
            <form id="contact-form" class="contact-form">
              <label for="name">Name</label>
              <input id="name" name="name" required>
              <label for="email">Email</label>
              <input id="email" name="email" type="email" required>
              <label for="message">Message</label>
              <textarea id="message" name="message" rows="4" required></textarea>
              <div class="form-actions">
                <button type="submit" class="primary">Send Message</button>
                <button type="button" class="secondary" onclick="window.location='mailto:Matt@SpecFlow.Tech'">Open Email</button>
              </div>
              <div id="contact-result" style="margin-top:8px;color:var(--muted)"></div>
            </form>
          </div>
        </div>
      </section>
    </main>

    <footer class="wrap footer">
      <small>© <span id="year"></span> SpecFlow — Serving Phoenix & Scottsdale.</small>
    </footer>

    <script>
      document.getElementById('year').textContent = new Date().getFullYear();

      // Contact form handler — posts JSON to /api/contact
      const form = document.getElementById('contact-form')
      const result = document.getElementById('contact-result')
      form.addEventListener('submit', async (e) => {
        e.preventDefault()
        result.textContent = 'Sending...'
        const payload = {
          name: document.getElementById('name').value,
          email: document.getElementById('email').value,
          message: document.getElementById('message').value
        }
        try {
          const res = await fetch('/api/contact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          })
          if (res.ok) {
            result.style.color = 'green'
            result.textContent = 'Message sent — thank you!'
            form.reset()
          } else {
            const j = await res.json().catch(() => ({}))
            result.style.color = 'crimson'
            result.textContent = j.error || 'Failed to send message.'
          }
        } catch (err) {
          result.style.color = 'crimson'
          result.textContent = 'Network error — try again later.'
        }
      })
    </script>
  </body>
</html>
```

---

### website/styles.css

```css
:root{--bg:#b0b0b0;--card:#d0d0d0;--accent:#0f62fe;--muted:#2a2a2a;--text:#0f0f0f}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,'Helvetica Neue',Arial;color:var(--text)}
.wrap{max-width:1100px;margin:0 auto;padding:28px}
.site-header{background:transparent;padding:12px 0}
.site-header .wrap{display:flex;align-items:center;justify-content:space-between}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:inherit}
.brand .title{font-weight:700;font-size:20px}
.nav a{margin-left:16px;color:var(--text);text-decoration:none}
.nav .cta{background:var(--accent);color:#ffffff;padding:8px 12px;border-radius:6px}

.hero{background:#a0a0a0;padding:60px 0}
.hero-grid{display:grid;grid-template-columns:1fr 360px;gap:28px;align-items:center}
.hero h1{font-size:40px;font-weight:bold;color:var(--accent);margin:0 0 12px}
.lead{color:var(--muted);font-size:18px;line-height:1.6;margin-bottom:18px}
.actions a{display:inline-block;margin-right:12px;padding:10px 16px;border-radius:8px;text-decoration:none;transition:transform 0.2s ease,box-shadow 0.2s ease}
.actions a:hover{transform:translateY(-2px);box-shadow:0 4px 10px rgba(0,0,0,0.1)}
.actions .primary{background:var(--accent);color:#fff}
.actions .secondary{background:transparent;border:1px solid #ddd;color:#0b1220}

.mock{display:flex;justify-content:center}
.mock-card{background:linear-gradient(180deg,#fff,#fbfcff);padding:20px;border-radius:12px;box-shadow:0 8px 30px rgba(12,18,26,0.06);width:320px;animation:fadeIn 1s ease-in-out}
.mock-line{height:12px;background:#eef2ff;margin-bottom:12px;border-radius:6px}
.mock-line.short{width:60%}
.mock-price{margin-top:12px;font-weight:700;color:var(--accent)}

.section{padding:50px 0}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.grid article{background:var(--card);border:1px solid #999999;padding:18px;border-radius:10px;box-shadow:0 6px 18px rgba(12,18,26,0.04);transition:transform 0.2s ease,box-shadow 0.2s ease}
.grid article:hover{transform:scale(1.05);box-shadow:0 8px 20px rgba(0,0,0,0.1)}

.alt{background:linear-gradient(180deg,#fff,#fbfdff)}
.services{display:flex;gap:16px;list-style:none;padding:0}
.services li{background:var(--card);border:1px solid #999999;padding:16px;border-radius:10px;flex:1;transition:background-color 0.3s ease}
.services li:hover{background-color:#eef2ff}

.contact-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.contact-form input,.contact-form textarea{width:100%;padding:10px;border-radius:8px;border:1px solid #e6e9ef;margin-bottom:8px}
.form-actions{display:flex;gap:8px}
.primary{background:var(--accent);color:#fff;border:none;padding:10px 14px;border-radius:8px}
.secondary{background:transparent;border:1px solid #ddd;padding:10px 14px;border-radius:8px}

.footer{padding:20px 28px;text-align:center;color:#ffffff;background:#0f62fe}

@media (max-width:800px){
  .hero-grid{grid-template-columns:1fr}
  .grid{grid-template-columns:1fr}
  .contact-grid{grid-template-columns:1fr}
  .nav a{display:none}
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

---

### website/README_DEPLOY.md

```markdown
# Deploy SpecFlow.tech (Cloudflare Pages)

This document explains how to publish the static landing page to Cloudflare Pages and connect your `SpecFlow.tech` domain which is already managed in Cloudflare.

## Quick steps

1. Create a GitHub repository and commit the `website/` folder (or push the whole repo).
2. In the Cloudflare dashboard, open **Pages** and create a new project that points to the GitHub repository and the branch (e.g., `main`).
3. Set the build settings:
   - Framework: `None` (since this is a static site)
   - Build command: (leave blank)
   - Build output directory: `website`
4. Deploy — Cloudflare will build and publish your site.
5. In the Pages project, add a custom domain: `specflow.tech`. Cloudflare will verify and automatically provision HTTPS.

## DNS notes

- Because your domain is already on Cloudflare, Pages will manage the necessary DNS entries automatically. If Cloudflare asks you to add records, follow the UI guidance; normally Cloudflare Pages will add the required cname/verification records.

## Local preview

Open `website/index.html` in your browser to preview locally, or serve it with a simple static server:

```powershell
# From project root
python -m http.server 8001 --directory website
# open http://127.0.0.1:8001
```

Alternative: Deploy via GitHub Pages or Netlify — but Cloudflare Pages is recommended since your domain is already managed there.
```

---

### website/README_WORKER.md

```markdown
# Cloudflare Worker: Contact form forwarding (KV)

This Worker accepts POST requests with JSON `{ name, email, message }` and stores submissions in a Cloudflare KV namespace (binding name: `CONTACTS_KV`).

## Prerequisites

- A Cloudflare account with your domain managed on Cloudflare.
- `wrangler` CLI installed locally: `npm install -g wrangler`

## Setup & deploy (KV)

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

3. Update `worker/wrangler.toml` with your account id and the KV namespace id. Replace `YOUR_ACCOUNT_ID` and `YOUR_KV_NAMESPACE_ID` with the values from Cloudflare.

4. Publish the Worker:

```powershell
wrangler publish
```

5. Route the Worker to your domain (recommended):

- In the Cloudflare dashboard, go to Workers → Routes and add a route such as `specflow.tech/api/contact` pointing to the published Worker.

## Using the Worker from the site

- The landing page posts JSON to `/api/contact`. Once the Worker is routed at `specflow.tech/api/contact`, the relative path resolves and submissions will be stored in KV.

## Inspecting stored messages

- You can read stored entries via the Cloudflare dashboard's KV preview, or use the admin Worker to list/retrieve messages.
```

---

### website/admin/index.html

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>SpecFlow Admin - Messages</title>
    <link rel="stylesheet" href="admin.css">
  </head>
  <body>
    <div class="wrap">
      <header class="admin-header">
        <h1>SpecFlow Admin</h1>
        <div class="token">
          <label>Admin token</label>
          <input id="token-input" placeholder="Paste ADMIN_TOKEN here" />
          <button id="save-token">Save</button>
        </div>
      </header>

      <main>
        <section class="controls">
          <button id="refresh">Refresh Messages</button>
        </section>

        <section class="content">
          <aside class="list">
            <ul id="messages-list"></ul>
          </aside>
          <section class="detail" id="detail">
            <div id="detail-inner">Select a message to view details</div>
          </section>
        </section>
      </main>

      <footer class="admin-footer">
        <small>Admin UI — messages stored in Cloudflare KV. Keep your token private.</small>
      </footer>
    </div>
    <script src="app.js"></script>
  </body>
</html>
```

---

### website/admin/admin.css

```css
:root{--bg:#f6f8fb;--card:#fff;--accent:#0f62fe;--muted:#6b7280}
*{box-sizing:border-box}
body{margin:0;font-family:Inter,system-ui,Segoe UI,Arial;background:var(--bg);color:#0b1220}
.wrap{max-width:1100px;margin:24px auto;padding:18px}
.admin-header{display:flex;align-items:center;justify-content:space-between;gap:12px}
.admin-header h1{margin:0}
.token{display:flex;gap:8px;align-items:center}
.token input{padding:8px;border-radius:6px;border:1px solid #ddd;width:360px}
.token button{padding:8px 12px;border-radius:6px;background:var(--accent);color:#fff;border:none}
.controls{margin:18px 0}
.controls button{padding:8px 12px;border-radius:6px;background:#fff;border:1px solid #ddd}
.content{display:grid;grid-template-columns:320px 1fr;gap:16px}
.list{background:var(--card);padding:10px;border-radius:8px;box-shadow:0 6px 18px rgba(12,18,26,0.04);height:60vh;overflow:auto}
.list ul{list-style:none;padding:0;margin:0}
.list li{padding:8px;border-bottom:1px solid #f0f2f6;cursor:pointer}
.list li:hover{background:#f4f7ff}
.list li .meta{font-size:12px;color:var(--muted)}
.detail{background:var(--card);padding:16px;border-radius:8px;box-shadow:0 6px 18px rgba(12,18,26,0.04);height:60vh;overflow:auto}
.detail pre{white-space:pre-wrap}
.actions{margin-top:12px}
.actions button{padding:8px 12px;border-radius:6px;margin-right:8px}

@media (max-width:800px){.content{grid-template-columns:1fr} .token input{width:160px}}
```

---

### website/admin/app.js

```javascript
const $ = sel => document.querySelector(sel)
const $$ = sel => Array.from(document.querySelectorAll(sel))

let ADMIN_TOKEN = ''
const base = '/api/admin/messages'

function setTokenFromInput(){
  const el = document.querySelector('#token-input')
  ADMIN_TOKEN = el ? el.value.trim() : ''
  const btn = document.querySelector('#save-token')
  if(ADMIN_TOKEN) btn.textContent = 'Saved'
  else btn.textContent = 'Save'
}

async function api(path, opts={}){
  const headers = opts.headers || {}
  if(ADMIN_TOKEN) headers['x-admin-token'] = ADMIN_TOKEN
  const res = await fetch(path, {...opts, headers})
  if(!res.ok) throw new Error(await res.text())
  return res.json()
}

async function loadList(){
  try{
    const data = await api(base)
    const ul = document.querySelector('#messages-list')
    ul.innerHTML = ''
    data.sort((a,b)=> new Date(b.created)-new Date(a.created))
    for(const item of data){
      const li = document.createElement('li')
      li.dataset.key = item.key
      li.innerHTML = `<strong>${item.name||'—'}</strong><div class="meta">${item.email||''} • ${new Date(item.created).toLocaleString()}</div>`
      li.addEventListener('click', ()=> showDetail(item.key))
      ul.appendChild(li)
    }
  }catch(err){
    alert('Error loading messages: '+err.message)
  }
}

async function showDetail(key){
  try{
    const item = await api(base+`/${encodeURIComponent(key)}`)
    const container = document.querySelector('#detail-inner')
    container.innerHTML = `
      <h3>${item.name||'—'}</h3>
      <div class="meta">${item.email||''} • ${new Date(item.created).toLocaleString()}</div>
      <hr/>
      <pre>${JSON.stringify(item.payload,null,2)}</pre>
      <div class="actions"><button id="delete-btn" data-key="${key}">Delete</button></div>
    `
    const del = document.querySelector('#delete-btn')
    if(del) del.addEventListener('click', ()=> deleteMessage(key))
  }catch(err){
    alert('Error loading message: '+err.message)
  }
}

async function deleteMessage(key){
  if(!confirm('Delete this message?')) return
  try{
    await api(base+`/${encodeURIComponent(key)}`, {method:'DELETE'})
    loadList()
    $('#detail').innerHTML = '<em>Deleted.</em>'
  }catch(err){
    alert('Error deleting message: '+err.message)
  }
}

function setup(){
  const save = document.querySelector('#save-token')
  if(save) save.addEventListener('click', ()=>{ setTokenFromInput(); loadList() })
  const tokenInput = document.querySelector('#token-input')
  if(tokenInput) tokenInput.addEventListener('keydown', e=>{ if(e.key==='Enter'){ setTokenFromInput(); loadList() } })
  const refresh = document.querySelector('#refresh')
  if(refresh) refresh.addEventListener('click', loadList)
  loadList()
}

window.addEventListener('DOMContentLoaded', setup)
```

---

### website/admin/run-local.ps1

```powershell
param(
  [switch]$StartWrangler
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$siteRoot = Resolve-Path (Join-Path $scriptDir "..")
$port = 8001

Write-Host "Serving site from: $siteRoot"
Write-Host "Admin UI will be available at http://127.0.0.1:$port/admin/"

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
  Write-Warning "Python not found in PATH. Install Python or serve files with another static server."
} else {
  Write-Host "Starting Python static server on port $port..."
  Start-Process -FilePath $python.Path -ArgumentList "-m","http.server","$port","--directory",$siteRoot
  Start-Sleep -Milliseconds 300
  Start-Process "http://127.0.0.1:$port/admin/"
}

if ($StartWrangler) {
  $wrangler = Get-Command wrangler -ErrorAction SilentlyContinue
  if (-not $wrangler) {
    Write-Warning "wrangler not found. Install it with: npm install -g wrangler"
  } else {
    $workerDir = Resolve-Path (Join-Path $scriptDir "..\worker\admin")
    Write-Host "Starting 'wrangler dev' for admin worker in: $workerDir"
    Start-Process -FilePath $wrangler.Path -ArgumentList "dev" -WorkingDirectory $workerDir
  }
}

Write-Host "Run 'Stop-Process -Name python' or close the server process windows to stop the servers."
```

---

### website/worker/index.js

```javascript
// Cloudflare Worker to store contact form submissions in a Cloudflare KV namespace.
// Bind a KV namespace with binding name `CONTACTS_KV` in `wrangler.toml`.

export default {
  async fetch(request, env) {
    if (request.method.toUpperCase() !== 'POST') {
      return new Response('Method not allowed', { status: 405 })
    }

    let data
    try {
      data = await request.json()
    } catch (err) {
      return new Response(JSON.stringify({ error: 'Invalid JSON' }), { status: 400, headers: { 'Content-Type': 'application/json' } })
    }

    const name = (data.name || '').trim()
    const email = (data.email || '').trim()
    const message = (data.message || '').trim()

    if (!name || !email || !message) {
      return new Response(JSON.stringify({ error: 'Missing required fields' }), { status: 400, headers: { 'Content-Type': 'application/json' } })
    }

    if (!env.CONTACTS_KV) {
      return new Response(JSON.stringify({ error: 'KV binding not configured' }), { status: 500, headers: { 'Content-Type': 'application/json' } })
    }

    // Create a record and store it in KV with a UUID key
    const id = (typeof crypto !== 'undefined' && crypto.randomUUID) ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(36).slice(2,9)}`
    const record = {
      id,
      name,
      email,
      message,
      created_at: new Date().toISOString()
    }

    try {
      await env.CONTACTS_KV.put(`contact:${id}`, JSON.stringify(record))
    } catch (err) {
      return new Response(JSON.stringify({ error: 'Failed to store message', detail: String(err) }), { status: 500, headers: { 'Content-Type': 'application/json' } })
    }

    return new Response(JSON.stringify({ ok: true, id }), { status: 200, headers: { 'Content-Type': 'application/json' } })
  }
}
```

---

### website/worker/wrangler.toml

```toml
name = "specflow-contact-worker"
type = "javascript"
# Replace with your Cloudflare Account ID
account_id = "YOUR_ACCOUNT_ID"
workers_dev = true

# To route the worker to a custom domain after publishing, add a route entry in the Cloudflare dashboard
# example:
# route = "specflow.tech/api/contact"

## KV namespace binding
## Create a KV namespace and replace the id below, or run the `wrangler kv:namespace create` command
[[kv_namespaces]]
binding = "CONTACTS_KV"
id = "YOUR_KV_NAMESPACE_ID"
```

---

### website/worker/admin/index.js

```javascript
// Admin Worker for reading contact submissions from CONTACTS_KV
// Protects endpoints with an ADMIN_TOKEN header

export default {
  async fetch(request, env) {
    const headerToken = request.headers.get('x-admin-token')
    if (!env.ADMIN_TOKEN || headerToken !== env.ADMIN_TOKEN) {
      return new Response(JSON.stringify({ error: 'unauthorized' }), { status: 401, headers: { 'Content-Type': 'application/json' } })
    }

    const url = new URL(request.url)
    const path = url.pathname.replace(/\/+$/, '')

    // GET /messages -> list recent messages (limit 100)
    if (request.method === 'GET' && path.endsWith('/messages')) {
      try {
        const list = await env.CONTACTS_KV.list({ prefix: 'contact:', limit: 100 })
        const keys = list.keys.map(k => k.name)
        const items = await Promise.all(keys.map(async key => {
          const v = await env.CONTACTS_KV.get(key)
          try { return JSON.parse(v) } catch { return { key, value: v } }
        }))
        return new Response(JSON.stringify({ items }), { headers: { 'Content-Type': 'application/json' } })
      } catch (err) {
        return new Response(JSON.stringify({ error: 'KV list error', detail: String(err) }), { status: 500, headers: { 'Content-Type': 'application/json' } })
      }
    }

    // GET /messages/:id -> fetch a single message
    const singleMatch = path.match(/\/messages\/(.+)$/)
    if (request.method === 'GET' && singleMatch) {
      const id = singleMatch[1]
      const key = `contact:${id}`
      const v = await env.CONTACTS_KV.get(key)
      if (!v) return new Response(JSON.stringify({ error: 'Not found' }), { status: 404, headers: { 'Content-Type': 'application/json' } })
      return new Response(v, { headers: { 'Content-Type': 'application/json' } })
    }

    // DELETE /messages/:id -> delete a message
    if (request.method === 'DELETE' && singleMatch) {
      const id = singleMatch[1]
      const key = `contact:${id}`
      await env.CONTACTS_KV.delete(key)
      return new Response(JSON.stringify({ ok: true }), { headers: { 'Content-Type': 'application/json' } })
    }

    return new Response('Not found', { status: 404 })
  }
}
```

---

### website/worker/admin/wrangler.toml

```toml
name = "specflow-contact-admin"
type = "javascript"
# Replace with your Cloudflare Account ID
account_id = "YOUR_ACCOUNT_ID"
workers_dev = true

[[kv_namespaces]]
binding = "CONTACTS_KV"
id = "YOUR_KV_NAMESPACE_ID"
```

---

### website/worker/admin/README_ADMIN.md

```markdown
# Admin Worker (KV) — inspect contact submissions

This admin Worker exposes a small JSON API to list, read, and delete contact submissions stored in the `CONTACTS_KV` namespace.

## Security
- The Worker expects an `x-admin-token` header containing the `ADMIN_TOKEN` secret. Set this before publishing.

## Endpoints
- `GET /messages` — returns up to 100 recent messages (array under `items`).
- `GET /messages/:id` — returns a single message JSON (the stored record).
- `DELETE /messages/:id` — deletes the message with the given id.

## Deploy

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

## Usage example (curl)

```powershell
curl -H "x-admin-token: YOUR_ADMIN_TOKEN_PLACEHOLDER" https://specflow.tech/api/admin/messages
curl -H "x-admin-token: YOUR_ADMIN_TOKEN_PLACEHOLDER" https://specflow.tech/api/admin/messages/<id>
```

## Notes
- Keep `ADMIN_TOKEN` secret and use a secure route (e.g., `admin.specflow.tech`) with Cloudflare access controls if desired.
- Consider adding Cloudflare Access or IP allowlist for the admin route in production.
```

---

## PowerShell commands for local development

```powershell
# 1. Clone / navigate to project
cd door-builder-app

# 2. Set up Python venv and install requirements
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3. Run Django migrations and start the backend
python manage.py migrate
python manage.py runserver
# Backend available at http://127.0.0.1:8000

# 4. In a new terminal, start the React frontend
cd frontend
npm install
npm run dev
# Frontend at http://localhost:5173 (proxies /api to Django)

# 5. In another terminal, serve the static website
cd website
python -m http.server 8001
# Open http://127.0.0.1:8001 for landing page, http://127.0.0.1:8001/admin/ for admin UI
```

---

## Cloudflare KV & Workers deployment

```powershell
# Install wrangler globally (if not installed)
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Create KV namespace (note the returned id)
cd website/worker
wrangler kv:namespace create "contacts_kv"
# If wrangler version differs, try: wrangler kv namespace create "contacts_kv"

# Edit wrangler.toml files to set account_id and KV id
# - website/worker/wrangler.toml
# - website/worker/admin/wrangler.toml

# Set admin token secret (for admin worker)
cd website/worker/admin
wrangler secret put ADMIN_TOKEN
# Enter a strong random value when prompted

# Publish contact worker
cd website/worker
wrangler publish

# Publish admin worker
cd website/worker/admin
wrangler publish

# Add routes in Cloudflare dashboard:
# specflow.tech/api/contact -> specflow-contact-worker
# specflow.tech/api/admin/* -> specflow-contact-admin
```

---

## Example curl commands

```powershell
# Submit a contact message
curl -X POST https://specflow.tech/api/contact `
  -H "Content-Type: application/json" `
  -d '{"name":"Jane Doe","email":"jane@example.com","message":"Hello!"}'

# List messages (admin)
curl -H "x-admin-token: YOUR_ADMIN_TOKEN_PLACEHOLDER" https://specflow.tech/api/admin/messages

# Get single message (admin)
curl -H "x-admin-token: YOUR_ADMIN_TOKEN_PLACEHOLDER" https://specflow.tech/api/admin/messages/<id>

# Delete message (admin)
curl -X DELETE -H "x-admin-token: YOUR_ADMIN_TOKEN_PLACEHOLDER" https://specflow.tech/api/admin/messages/<id>
```

---

## Smoke tests (expected responses)

| Endpoint | Expected |
|----------|----------|
| `POST /api/contact` | `{"ok":true,"id":"..."}` |
| `GET /api/admin/messages` (valid token) | `{"items":[...]}` |
| `GET /api/admin/messages` (no token) | `{"error":"unauthorized"}` 401 |
| `POST /api/estimate/` (Django) | `{"estimate":123.45}` |

---

## Notes on quotas and cost

- **Cloudflare Workers Free Tier**: 100,000 requests/day, 10ms CPU time/request.
- **KV Free Tier**: 100,000 reads/day, 1,000 writes/day, 1 GB storage.
- For production, consider upgrading to Workers Paid ($5/month) for higher limits.
- Use Cloudflare Access or IP allowlists to protect the admin endpoint in production.

---

## Edge cases

- If the admin secret is missing and the admin UI tries to call the admin worker, return a clear 401 with `{"error":"unauthorized"}`.
- If `wrangler` version differences exist, try both:
  - `wrangler kv:namespace create "contacts_kv"`
  - `wrangler kv namespace create "contacts_kv"`
  Run whichever matches your `wrangler -v`.

---

## Deliverable

After you generate all the files above, also provide:
1. A downloadable zip archive of the entire project (if supported), OR
2. A summary listing all file paths and confirmation that each was created.

Then ask: **"Do you want this committed to a new GitHub repo and pushed (I can open a PR describing the changes)?"**

---

# End of prompt
