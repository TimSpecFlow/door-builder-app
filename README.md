Door Builder - Django Starter

Minimal Django starter for the Door Builder app.

What you get:
- Django project `door_builder`
- App `catalog` with a small `estimate` API endpoint
- `requirements.txt` and `.gitignore`

Quick start (PowerShell):

```powershell
cd "c:\Users\obrie\Python\door-builder-app"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

API example (POST JSON to estimate):

POST http://127.0.0.1:8000/api/estimate/

Body:
```
{
  "width": 36,
  "height": 80,
  "material": "wood",
  "hardware": ["hinges","handle"]
}
```

Response:
```
{ "estimate": 123.45 }
```

Next steps: create a React frontend or Django templates, add Stripe integration, and expand product models.
