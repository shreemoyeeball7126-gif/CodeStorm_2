# PERSON 3 — Surplus calculation, donation matching, and food-safety storage guidance.
#
# Preparation buffer policy
# -------------------------
# A minimal buffer is added on top of predicted demand so almost nothing is
# wasted, while still covering normal forecast error:
#   - Base buffer (a normal day):      3.8%
#   - Exam day (harder to predict):    4.2%
#   - Event day (footfall spikes):     4.1%
#   - Exam day + Event day:            4.5%   (capped here)
#
# Example: 438 predicted, normal day -> buffer 3.8% -> 454.6 -> 455 recommended
#          -> surplus = 455 - 438 = 17 meals.

from datetime import datetime, timedelta
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECIPIENT_FILE = ROOT / "Person_3_Surplus_Donation" / "recipients.csv"

BASE_BUFFER = 0.038
EXAM_DAY_ADD = 0.004
EVENT_DAY_ADD = 0.003
MAX_BUFFER = 0.045


def preparation_buffer(exam_day=0, event="None"):
    """Return the preparation buffer fraction (always within 3.8%-4.5%)."""
    buffer = BASE_BUFFER
    if int(exam_day):
        buffer += EXAM_DAY_ADD
    if event and str(event) != "None":
        buffer += EVENT_DAY_ADD
    return round(min(buffer, MAX_BUFFER), 4)


def recommended_preparation(predicted_demand, exam_day=0, event="None"):
    """Minimal-surplus recommended preparation quantity for a given predicted demand."""
    predicted_demand = max(0.0, float(predicted_demand))
    buffer = preparation_buffer(exam_day, event)
    return max(
        int(round(predicted_demand)),
        int(round(predicted_demand * (1 + buffer)))
    )


def calculate_surplus(recommended, predicted):
    return max(0, int(recommended) - int(round(predicted)))


import math


def donation_recommendation(surplus, max_recipients=4):
    """
    Allocate surplus meals across verified recipients (priority first, then distance).

    Small surpluses easily fit inside one recipient's capacity, which would mean
    only ever recommending a single destination. To spread the impact around,
    no single recipient is given more than half the surplus (or its own
    capacity, whichever is smaller) — so, whenever more than one verified
    recipient exists, at least two show up in the recommendation.
    """
    surplus = max(0, int(surplus))
    if surplus == 0:
        return []

    recipients = pd.read_csv(RECIPIENT_FILE)
    eligible = recipients[recipients["verified"].astype(bool)].copy()
    eligible = eligible.sort_values(
        ["priority", "distance_km"],
        ascending=[False, True]
    )

    per_recipient_cap = max(1, math.ceil(surplus / 2)) if surplus > 1 else surplus

    remaining = surplus
    allocations = []

    for _, row in eligible.iterrows():
        if remaining <= 0 or len(allocations) >= max_recipients:
            break

        capacity = int(row["capacity_meals"])
        # Cap every recipient except the very last one needed, so a single
        # recipient with plenty of spare capacity doesn't absorb everything.
        qty = min(remaining, capacity, per_recipient_cap)

        if qty > 0:
            allocations.append({
                "recipient": row["recipient_name"],
                "type": row["recipient_type"],
                "recommended_meals": qty,
                "capacity": capacity,
                "distance_km": float(row["distance_km"]),
                "priority": int(row["priority"])
            })
            remaining -= qty

    # If a cap-driven pass still leaves meals unassigned (e.g. every eligible
    # recipient was already used at max_recipients), top up existing
    # allocations in priority order using their remaining spare capacity.
    if remaining > 0 and allocations:
        used = {a["recipient"] for a in allocations}
        for _, row in eligible.iterrows():
            if remaining <= 0:
                break
            if row["recipient_name"] not in used:
                continue
            alloc = next(a for a in allocations if a["recipient"] == row["recipient_name"])
            spare = int(row["capacity_meals"]) - alloc["recommended_meals"]
            top_up = min(remaining, spare)
            if top_up > 0:
                alloc["recommended_meals"] += top_up
                remaining -= top_up

    return allocations


# ---------------------------------------------------------------------------
# Food safety / storage guidance for whatever surplus doesn't get redistributed
# same-day. Durations follow standard cooked-food holding guidance.
# ---------------------------------------------------------------------------

STORAGE_OPTIONS = [
    {
        "storage_method": "Room Temperature Holding",
        "storage_temperature": "20-25°C (ambient)",
        "max_storage_hours": 2,
        "notes": "Only safe for immediate, same-day distribution. Highest spoilage risk."
    },
    {
        "storage_method": "Refrigerated Storage",
        "storage_temperature": "2-5°C",
        "max_storage_hours": 72,
        "notes": "Best for next-day pickup. Chill within 30 minutes of preparation, keep sealed."
    },
    {
        "storage_method": "Frozen Storage",
        "storage_temperature": "-18°C or below",
        "max_storage_hours": 744,
        "notes": "Best for longer-term redistribution. Label containers with the preparation date."
    },
]


def _format_duration(hours):
    if hours < 24:
        return f"{hours} hours"
    days = hours // 24
    return f"{days} day{'s' if days != 1 else ''}"


def storage_safety_guidance(prepared_date, surplus_meals=0):
    """
    Return storage/food-safety options for surplus meals prepared on `prepared_date`.
    `prepared_date` can be a date string ("YYYY-MM-DD"), datetime, or pandas Timestamp.
    """
    prepared = pd.Timestamp(prepared_date)
    surplus_meals = max(0, int(surplus_meals))

    guidance = []
    for option in STORAGE_OPTIONS:
        hours = option["max_storage_hours"]
        safe_until = prepared + timedelta(hours=hours)
        guidance.append({
            "storage_method": option["storage_method"],
            "storage_temperature": option["storage_temperature"],
            "max_storage_duration": _format_duration(hours),
            "prepared_on": prepared.strftime("%Y-%m-%d"),
            "safe_to_consume_until": safe_until.strftime("%Y-%m-%d"),
            "notes": option["notes"],
            "surplus_meals": surplus_meals,
        })
    return guidance


if __name__ == "__main__":
    predicted = 438
    recommended = recommended_preparation(predicted)
    surplus = calculate_surplus(recommended, predicted)
    print("Predicted:", predicted)
    print("Recommended:", recommended)
    print("Surplus:", surplus)
    print(pd.DataFrame(donation_recommendation(surplus)))
    print()
    print(pd.DataFrame(storage_safety_guidance("2026-08-21", surplus)))
