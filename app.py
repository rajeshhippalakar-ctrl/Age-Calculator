from datetime import date

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


def days_in_month(year, month):
    if month == 12:
        return 31
    return (date(year, month + 1, 1) - date(year, month, 1)).days


def anniversary_for_year(birth_date, year):
    day = min(birth_date.day, days_in_month(year, birth_date.month))
    return date(year, birth_date.month, day)


def add_months(value, months):
    month_index = value.month - 1 + months
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    return date(year, month, min(value.day, days_in_month(year, month)))


def _next_birthday(birth_date, today):
    this_year = anniversary_for_year(birth_date, today.year)
    if this_year >= today:
        return this_year
    return anniversary_for_year(birth_date, today.year + 1)


def calculate_age(birth_date, today=None):
    today = today or date.today()
    if birth_date > today:
        raise ValueError("Birth date cannot be in the future.")

    years = today.year - birth_date.year
    last_birthday = anniversary_for_year(birth_date, today.year)
    if last_birthday > today:
        years -= 1
        last_birthday = anniversary_for_year(birth_date, today.year - 1)

    months = 0
    month_mark = last_birthday
    while months < 11:
        next_month = add_months(last_birthday, months + 1)
        if next_month > today:
            break
        months += 1
        month_mark = next_month

    total_days = (today - birth_date).days
    next_birthday = _next_birthday(birth_date, today)
    return {
        "years": years,
        "months": months,
        "days": (today - month_mark).days,
        "total_days": total_days,
        "total_weeks": total_days // 7,
        "total_months": years * 12 + months,
        "next_birthday": next_birthday.isoformat(),
        "days_until_birthday": (next_birthday - today).days,
    }


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/calculate")
def calculate():
    payload = request.get_json(silent=True) or {}
    raw_birth_date = payload.get("birth_date", "")
    try:
        birth_date = date.fromisoformat(raw_birth_date)
        result = calculate_age(birth_date)
    except (TypeError, ValueError):
        return jsonify({"error": "Enter a valid birth date that is not in the future."}), 400

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)