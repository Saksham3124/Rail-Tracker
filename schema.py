from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
engine = create_engine(os.getenv("DB_URL"))

schema_sql = """
CREATE TABLE IF NOT EXISTS live_status (
    id SERIAL PRIMARY KEY,
    train_no VARCHAR(10),
    current_station VARCHAR(100),
    delay_mins INTEGER,
    status VARCHAR(50),
    recorded_at TIMESTAMP DEFAULT NOW()
);
"""

with engine.connect() as conn:
    conn.execute(text(schema_sql))
    conn.commit()

print("✅ Tables created")