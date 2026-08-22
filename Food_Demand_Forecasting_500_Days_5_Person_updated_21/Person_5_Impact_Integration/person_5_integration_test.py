from pathlib import Path
import pickle
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "Person_3_Surplus_Donation"))
sys.path.insert(0, str(ROOT / "Person_5_Impact_Integration"))

from person_3_surplus_donation import (
    recommended_preparation,
    calculate_surplus,
    donation_recommendation,
    preparation_buffer,
    storage_safety_guidance,
)
from person_5_impact import calculate_impact

df = pd.read_csv(ROOT / "Person_1_Data" / "demand_data.csv")

assert len(df) == 500
assert df["attendance_pct"].between(0, 100).all()
assert (df["meals_consumed"] <= df["meals_prepared"]).all()
assert (df["surplus_meals"] >= 0).all()
print("PASS: 500-day dataset")

with open(ROOT / "Person_2_ML" / "demand_model.pkl", "rb") as f:
    bundle = pickle.load(f)

sample = pd.DataFrame([{
    "day_of_week": "Monday",
    "is_weekend": 0,
    "weather": "Sunny",
    "exam_day": 0,
    "event": "None",
    "attendance_pct": 86,
    "lag_1_consumed": 400,
    "rolling_7_consumed": 395
}])

prediction = max(0, float(bundle["model"].predict(sample)[0]))
recommended = recommended_preparation(prediction)
surplus = calculate_surplus(recommended, prediction)

assert prediction >= 0
assert recommended >= round(prediction)
assert surplus >= 0
print("PASS: ML + minimal surplus")

allocations = donation_recommendation(surplus)
assert isinstance(allocations, list)
print("PASS: Donation recommendation")

# --- Donations should spread across multiple recipients, not just one ---
multi_alloc = donation_recommendation(17)
assert len(multi_alloc) >= 2
assert sum(a["recommended_meals"] for a in multi_alloc) == 17
print("PASS: donation recommendation spreads across multiple recipients")

impact = calculate_impact(surplus)
assert impact["meals_redistributed"] >= 0
print("PASS: Impact calculation")

# --- Preparation buffer must always stay within 3.8%-4.5% ---
assert preparation_buffer(0, "None") == 0.038
assert preparation_buffer(1, "None") == 0.042
assert preparation_buffer(0, "Festival") == 0.041
assert preparation_buffer(1, "Festival") == 0.045
for exam in (0, 1):
    for event in ("None", "Festival", "Sports Event"):
        b = preparation_buffer(exam, event)
        assert 0.038 <= b <= 0.045
print("PASS: buffer always within 3.8%-4.5%")

# --- Original worked example must still hold exactly ---
assert recommended_preparation(438) == 455
assert calculate_surplus(455, 438) == 17
print("PASS: 438 -> 455 -> 17 example")

# --- Storage guidance must extend out to 2026-09-21 for the last data date ---
storage = storage_safety_guidance("2026-08-21", 17)
frozen = [s for s in storage if s["storage_method"] == "Frozen Storage"][0]
assert frozen["safe_to_consume_until"] == "2026-09-21"
print("PASS: storage guidance dates (frozen safe until 2026-09-21)")

print("ALL TESTS PASSED.")
