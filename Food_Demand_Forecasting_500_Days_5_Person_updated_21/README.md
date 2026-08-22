# Food Demand Forecasting — 5 Person Project

This version contains **500 days of data**.

- Start date: 2025-04-09
- End date: 2026-08-21
- Total rows: 500
- Attendance is always 0–100%, averaging around 75% (never clustered near the ceiling).

## Demand drivers

- **Exam days** → predicted demand is boosted above a normal day.
- **Event days** (Festival / Sports Event / Cultural Event / Workshop) → predicted demand is boosted above a day with no event.
- **Sunny weather** → predicted demand is boosted above other weather conditions.

## Minimal-surplus preparation buffer

A small buffer is added on top of predicted demand, scaled between **3.8% and 4.5%**
depending on the day:

| Day type                  | Buffer |
|----------------------------|--------|
| Normal day                 | 3.8%   |
| Exam day                   | 4.2%   |
| Event day                  | 4.1%   |
| Exam day + Event day       | 4.5%   |

Example: 438 predicted → 455 recommended (3.8% buffer) → 17 surplus.

## Surplus donation

Surplus is matched to verified recipients (by priority, then distance), across a
wider set of destination types: campus pantry, community kitchen, community food
program, shelter homes, old age homes, a street outreach program, and an animal
shelter. Each recommendation lists recipient, type, recommended meals, capacity,
distance, and priority.

## Food safety & storage

For any surplus that can't be redistributed the same day, the project recommends
a storage method, temperature, maximum storage duration, and the exact
safe-to-consume-until date, computed from the preparation date:

| Method                | Temperature       | Max duration |
|------------------------|-------------------|--------------|
| Room temperature       | 20–25°C           | 2 hours      |
| Refrigerated           | 2–5°C             | 3 days       |
| Frozen                 | -18°C or below    | 31 days      |

## Run

pip install -r requirements.txt

streamlit run Person_4_Dashboard/app.py

To regenerate the dataset:

python Person_1_Data/person_1_data.py

To retrain the model:

python Person_2_ML/person_2_ml.py

For integration testing:

python Person_5_Impact_Integration/person_5_integration_test.py
