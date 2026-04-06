from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()
DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL) if DB_URL else None


def export_all():
    if not engine:
        print("⚠️ No DB configured, skipping export")
        return

    try:
        with engine.connect() as conn:

            pd.read_sql(text("""
                SELECT train_no, AVG(delay_mins) AS avg_delay
                FROM live_status
                GROUP BY train_no
            """), conn).to_csv("train_master.csv", index=False)

        print("✅ Exported DB data to CSV")

    except Exception as e:
        print("⚠️ Export failed:", e)