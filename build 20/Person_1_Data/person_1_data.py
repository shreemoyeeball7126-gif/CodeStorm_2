# PERSON 1 — Generate and validate 500 days of demand data.
#
# Rules encoded here:
#   - Attendance is always between 0 and 100 (clipped), averaging ~78-82%
#     (never clusters near the ceiling).
#   - Exam days push demand a bit higher than normal days.
#   - Event days also push demand a bit higher than normal days.
#   - Sunny days push demand higher (more footfall / fewer people skipping meals).
#   - meals_consumed can never exceed meals_prepared (prepared is always the
#     recommended-preparation quantity, so surplus is >= 0 by construction).

from datetime import date, timedelta
from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "Person_3_Surplus_Donation"))
from person_3_surplus_donation import recommended_preparation  # noqa: E402

SEED = 42
DAYS = 500
END_DATE = date(2026, 8, 21)
START_DATE = END_DATE - timedelta(days=DAYS - 1)

TOTAL_CAPACITY = 480          # max meals the mess can realistically serve
BASE_ATTENDANCE = 80.0        # center of attendance distribution (%)

WEATHER_CHOICES = ["Sunny", "Cloudy", "Rainy", "Hot"]
WEATHER_WEIGHTS = [0.43, 0.22, 0.23, 0.12]

# Direct effect of weather on attendance (percentage points)
WEATHER_ATTENDANCE_EFFECT = {"Sunny": 4, "Cloudy": -1, "Rainy": -9, "Hot": -7}

# Extra multiplicative demand boost on top of attendance-driven demand
WEATHER_DEMAND_BOOST = {"Sunny": 1.06, "Cloudy": 1.00, "Rainy": 0.97, "Hot": 0.95}
EXAM_DAY_DEMAND_BOOST = 1.09
EVENT_DAY_DEMAND_BOOST = 1.06

EVENT_CHOICES = ["Festival", "Sports Event", "Cultural Event", "Workshop"]
EVENT_PROB = 0.17          # ~85 / 500 days have an event
EXAM_DAY_PROB = 0.054      # ~27 / 500 days are exam days


def generate_dataset(seed=SEED, days=DAYS, end_date=END_DATE):
    rng = np.random.default_rng(seed)
    start_date = end_date - timedelta(days=days - 1)
    dates = [start_date + timedelta(days=i) for i in range(days)]

    rows = []
    for d in dates:
        day_of_week = d.strftime("%A")
        is_weekend = int(d.weekday() >= 5)

        weather = rng.choice(WEATHER_CHOICES, p=WEATHER_WEIGHTS)
        exam_day = int(rng.random() < EXAM_DAY_PROB)
        event = rng.choice(EVENT_CHOICES, p=[0.18, 0.30, 0.25, 0.27]) if rng.random() < EVENT_PROB else "None"

        # --- attendance ---
        attendance = BASE_ATTENDANCE
        attendance += WEATHER_ATTENDANCE_EFFECT[weather]
        attendance -= 14 if is_weekend else 0
        attendance += 3 if exam_day else 0          # more students on campus during exams
        attendance += 2 if event != "None" else 0    # events draw extra footfall
        attendance += rng.normal(0, 5)
        attendance = float(np.clip(attendance, 20, 100))

        # --- "true" expected demand before day-to-day noise ---
        expected_demand = (attendance / 100.0) * TOTAL_CAPACITY
        expected_demand *= WEATHER_DEMAND_BOOST[weather]
        if exam_day:
            expected_demand *= EXAM_DAY_DEMAND_BOOST
        if event != "None":
            expected_demand *= EVENT_DAY_DEMAND_BOOST

        # --- prepared quantity: minimal buffer over expected demand ---
        meals_prepared = recommended_preparation(expected_demand, exam_day, event)

        # --- actual consumption: expected demand + noise, capped at what was prepared ---
        noise = rng.normal(0, 8)
        meals_consumed = int(round(max(0, expected_demand + noise)))
        meals_consumed = min(meals_consumed, meals_prepared)

        surplus_meals = meals_prepared - meals_consumed

        rows.append({
            "date": d.isoformat(),
            "day_of_week": day_of_week,
            "is_weekend": is_weekend,
            "weather": weather,
            "exam_day": exam_day,
            "event": event,
            "attendance_pct": round(attendance, 1),
            "meals_prepared": meals_prepared,
            "meals_consumed": meals_consumed,
            "surplus_meals": surplus_meals,
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = generate_dataset()

    assert len(df) == DAYS
    assert df["attendance_pct"].between(0, 100).all()
    assert (df["meals_consumed"] <= df["meals_prepared"]).all()
    assert (df["surplus_meals"] >= 0).all()

    out_path = Path(__file__).resolve().parent / "demand_data.csv"
    df.to_csv(out_path, index=False)

    print(f"Wrote {len(df)} rows to {out_path}")
    print("Date range:", df["date"].min(), "to", df["date"].max())
    print("Attendance mean/min/max:", round(df["attendance_pct"].mean(), 1),
          df["attendance_pct"].min(), df["attendance_pct"].max())
    print("Mean consumed (exam vs normal):")
    print(df.groupby("exam_day")["meals_consumed"].mean())
    print("Mean consumed by weather:")
    print(df.groupby("weather")["meals_consumed"].mean())
    print("Mean consumed (event vs none):")
    print(df.assign(has_event=df["event"] != "None").groupby("has_event")["meals_consumed"].mean())
