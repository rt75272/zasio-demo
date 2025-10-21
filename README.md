# Zasio Implementation Demo

A tiny Flask web app that:
- Shows an implementation plan on the home page
- Lets you upload a CSV and validates it using a simple Python validator

## Run locally

Prereqs: Python 3.12+

```bash
# optional: use your existing venv in ./zasio or create a new one
python3 -m venv .venv
source .venv/bin/activate

pip install -r zasio_app/requirements.txt
python -m zasio_app.app
```

Then open http://127.0.0.1:5000

## Deploy to Render

1. Push this repo to GitHub
2. Create a new Web Service in Render, link your repo
3. Use these settings:
   - Build Command: `pip install -r zasio_app/requirements.txt`
   - Start Command: `gunicorn zasio_app.app:app`

Alternatively, select "Use render.yaml" and Render will auto-detect `render.yaml` from the repo.

## Deploy to Heroku (optional)

The included `Procfile` works with Heroku out-of-the-box:

```bash
heroku create
heroku buildpacks:set heroku/python
heroku config:set PYTHON_VERSION=3.12.0
git push heroku main
```

## CSV format

Required columns: `Record_ID, Category, Retention_Years, Owner`.

Example row:

```
Record_ID,Category,Retention_Years,Owner
1001,Contracts,7,Legal
```

Sample file to try: `zasio_app/examples/sample.csv`
