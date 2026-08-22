# PERSON 5 — Impact calculation.

MEAL_WEIGHT_KG = 0.40
MEAL_COST_INR = 60.0
CO2E_PER_KG_FOOD = 2.5


def calculate_impact(surplus_meals):
    meals = max(0, int(surplus_meals))
    return {
        "meals_redistributed": meals,
        "food_saved_kg": round(meals * MEAL_WEIGHT_KG, 2),
        "estimated_value_inr": round(meals * MEAL_COST_INR, 2),
        "estimated_co2e_avoided_kg": round(
            meals * MEAL_WEIGHT_KG * CO2E_PER_KG_FOOD, 2
        )
    }


if __name__ == "__main__":
    print(calculate_impact(17))
