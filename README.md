# Age-Calculator
this is my mini project of Academics.

A full-stack age calculator built with Python, Flask, HTML, CSS, and JavaScript. It calculates calendar age, total elapsed days, weeks, months, and the days until the next birthday. Birth dates are not stored.

## Run locally

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000.

## Run tests

```powershell
python -m unittest discover -s tests -v
```

## API

`POST /api/calculate`

Request body:

```json
{"birth_date": "2000-01-01"}
```

The JSON response includes the age in years, months, and days, total elapsed time, and the next birthday. Invalid and future birth dates return HTTP 400.
