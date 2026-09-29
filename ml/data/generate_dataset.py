"""
Dataset generator for AI Canteen Food Demand Prediction.
Generates 90 days of realistic multi-item historical sales data.
"""
import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DEFAULT_DATASET_PATH = os.path.join(ROOT_DIR, "ml", "data", "canteen_demand_dataset.csv")

def generate_canteen_dataset(output_path=None, num_days=90):
    if output_path is None:
        output_path = DEFAULT_DATASET_PATH
    random.seed(42)
    np.random.seed(42)

    food_items = [
        {"name": "Veg Biryani", "base_demand": 140, "std": 12, "rain_mult": 1.15, "fest_mult": 1.35, "holiday_mult": 0.65},
        {"name": "Chicken Biryani", "base_demand": 175, "std": 15, "rain_mult": 1.12, "fest_mult": 1.45, "holiday_mult": 0.70},
        {"name": "Masala Dosa", "base_demand": 125, "std": 10, "rain_mult": 0.85, "fest_mult": 1.20, "holiday_mult": 0.80},
        {"name": "Paneer Thali", "base_demand": 110, "std": 9, "rain_mult": 1.00, "fest_mult": 1.15, "holiday_mult": 0.50},
        {"name": "Chole Bhature", "base_demand": 130, "std": 11, "rain_mult": 1.05, "fest_mult": 1.30, "holiday_mult": 0.90},
        {"name": "Samosa & Chai", "base_demand": 220, "std": 18, "rain_mult": 1.35, "fest_mult": 1.50, "holiday_mult": 0.60},
        {"name": "Fried Rice", "base_demand": 115, "std": 10, "rain_mult": 1.02, "fest_mult": 1.25, "holiday_mult": 0.65},
        {"name": "Sandwich", "base_demand": 95, "std": 8, "rain_mult": 0.90, "fest_mult": 1.15, "holiday_mult": 0.75},
    ]

    weather_types = ["Sunny", "Sunny", "Sunny", "Rainy", "Cloudy", "Cold"]
    events_pool = ["None", "None", "None", "None", "College Fest", "Sports Meet", "Exam Period", "Workshop"]

    day_multipliers = {
        "Monday": 0.95,
        "Tuesday": 1.00,
        "Wednesday": 1.05,
        "Thursday": 1.02,
        "Friday": 1.20,
        "Saturday": 0.85,
        "Sunday": 0.75
    }

    start_date = datetime.now().date() - timedelta(days=num_days)
    records = []

    # Keep track of history per item to calculate previous_day and previous_week sales
    item_history = {item["name"]: [] for item in food_items}

    for day_offset in range(num_days):
        current_date = start_date + timedelta(days=day_offset)
        day_name = current_date.strftime("%A")
        is_weekend = day_name in ["Saturday", "Sunday"]

        # Randomize environmental conditions per day
        weather = random.choice(weather_types)
        
        # Determine holiday and special event
        if is_weekend:
            is_holiday = 1
            special_event = "Sports Meet" if random.random() < 0.25 else "None"
        else:
            is_holiday = 1 if random.random() < 0.08 else 0
            if is_holiday:
                special_event = "None"
            else:
                special_event = random.choice(events_pool)

        for item in food_items:
            item_name = item["name"]
            base = item["base_demand"]
            std = item["std"]

            # Multipliers
            day_mult = day_multipliers[day_name]
            weather_mult = item["rain_mult"] if weather == "Rainy" else (0.95 if weather == "Cold" else 1.0)
            
            if is_holiday:
                holiday_mult = item["holiday_mult"]
            else:
                holiday_mult = 1.0

            if special_event == "College Fest":
                event_mult = item["fest_mult"]
            elif special_event == "Sports Meet":
                event_mult = 1.25
            elif special_event == "Exam Period":
                event_mult = 1.15 if item_name in ["Samosa & Chai", "Sandwich"] else 0.88
            elif special_event == "Workshop":
                event_mult = 1.10
            else:
                event_mult = 1.0

            noise = np.random.normal(0, std)
            expected_quantity = base * day_mult * weather_mult * holiday_mult * event_mult + noise
            quantity_sold = max(20, int(round(expected_quantity)))

            # History for lag features
            history = item_history[item_name]
            if len(history) >= 1:
                prev_day = history[-1]
            else:
                prev_day = int(round(base * day_mult))

            if len(history) >= 7:
                prev_week_avg = int(round(np.mean(history[-7:])))
            elif len(history) > 0:
                prev_week_avg = int(round(np.mean(history)))
            else:
                prev_week_avg = int(round(base))

            history.append(quantity_sold)

            records.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "day_of_week": day_name,
                "weather": weather,
                "is_holiday": is_holiday,
                "special_event": special_event,
                "food_item": item_name,
                "previous_day_sales": prev_day,
                "previous_week_sales": prev_week_avg,
                "quantity_sold": quantity_sold
            })

    df = pd.DataFrame(records)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Successfully generated {len(df)} records across {num_days} days to {output_path}")
    print(df.head(5))
    return df

if __name__ == "__main__":
    generate_canteen_dataset()
