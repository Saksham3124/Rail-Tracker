import random
import os
from datetime import datetime
import pytz
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from train_list import TRAINS

# ------------------ SETUP ------------------

load_dotenv()

DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL) if DB_URL else None

ist = pytz.timezone('Asia/Kolkata')

# Per-train base delay profile (train_no -> base delay in minutes)
# Trains with higher numbers tend to be longer routes = more delay variance
TRAIN_DELAY_PROFILE = {
    train["train_no"]: 10 + (int(str(train["train_no"])[-1]) * 5)
    for train in TRAINS
}

# ------------------ HELPERS ------------------

def simulate_delay(train_no):
    """Simulate a delay for a given train based on its delay profile."""
    base = TRAIN_DELAY_PROFILE.get(train_no, 20)
    return max(0, int(base * random.uniform(0.5, 1.8)))

def calculate_risk(delay):
    """Classify delay into risk level."""
    if delay > 60:
        return "HIGH"
    elif delay > 30:
        return "MEDIUM"
    return "LOW"

def get_station(train):
    return train["source"]

# ------------------ CORE ------------------

def run_simulation():
    print(f"\n🚂 Simulation at {datetime.now(ist).strftime('%H:%M:%S')}")

    records = []

    for train in TRAINS:
        delay = simulate_delay(train["train_no"])
        station = get_station(train)
        risk = calculate_risk(delay)

        record = {
            "train_no": train["train_no"],
            "train_name": train["train_name"],
            "station": station,
            "delay_mins": delay,
            "risk_label": risk,
            "timestamp": datetime.now(ist)
        }
        records.append(record)
        print(f"{train['train_name']:<25} | {delay:>3} min | {risk}")

    # ------------------ DB STORAGE ------------------

    if engine:
        try:
            with engine.connect() as conn:
                for r in records:
                    conn.execute(text("""
                        INSERT INTO live_status
                        (train_no, current_station, delay_mins, status, recorded_at)
                        VALUES (:train_no, :station, :delay, :status, :time)
                    """), {
                        "train_no": r["train_no"],
                        "station": r["station"],
                        "delay": r["delay_mins"],
                        "status": r["risk_label"],
                        "time": r["timestamp"]
                    })
                conn.commit()
            print("✅ Data stored in DB")
        except Exception as e:
            print("⚠️ DB failed:", e)

    # ------------------ CSV BACKUP (LIMITED HISTORY) ------------------

    df = pd.DataFrame(records)
    os.makedirs("data", exist_ok=True)
    file_path = "data/train_history.csv"

    if os.path.exists(file_path):
        old_df = pd.read_csv(file_path)
        old_df["timestamp"] = pd.to_datetime(old_df["timestamp"])
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        combined_df = pd.concat([old_df, df], ignore_index=True)
        combined_df = combined_df.sort_values("timestamp", ascending=True)

        # Keep only last 10 records per train
        combined_df = (
            combined_df.groupby("train_no", group_keys=False)
            .tail(10)
        )
        combined_df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, index=False)

    print("✅ CSV updated")
    print(f"📊 Records added: {len(df)}")

# ------------------ RUN ------------------

if __name__ == "__main__":
    run_simulation()
