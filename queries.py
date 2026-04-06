from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()
engine = create_engine(os.getenv("DB_URL"))

def run_query(title, sql):
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)
    with engine.connect() as conn:
        df = pd.read_sql(text(sql), conn)
        print(df.to_string(index=False))

# ── Query 1: Current Risk Leaderboard ────────────────────────
run_query("Top 10 Highest Risk Trains Right Now", """
    SELECT 
        t.train_name,
        t.source,
        t.destination,
        rs.risk_score,
        rs.risk_label,
        ls.delay_mins,
        ls.current_station,
        ls.status
    FROM risk_scores rs
    JOIN trains t ON rs.train_no = t.train_no
    JOIN live_status ls ON rs.train_no = ls.train_no
    WHERE rs.calculated_at = (
        SELECT MAX(calculated_at) FROM risk_scores
    )
    ORDER BY rs.risk_score DESC
    LIMIT 10
""")

# ── Query 2: Average Delay by Route ──────────────────────────
run_query("Average Delay by Route", """
    SELECT 
        t.train_name,
        t.source || ' → ' || t.destination AS route,
        ROUND(AVG(ls.delay_mins), 1) AS avg_delay_mins,
        MAX(ls.delay_mins)            AS max_delay_mins,
        MIN(ls.delay_mins)            AS min_delay_mins,
        COUNT(*)                      AS total_records
    FROM live_status ls
    JOIN trains t ON ls.train_no = t.train_no
    GROUP BY t.train_name, t.source, t.destination
    ORDER BY avg_delay_mins DESC
""")

# ── Query 3: Risk Distribution ────────────────────────────────
run_query("Risk Distribution Across Network", """
    SELECT 
        risk_label,
        COUNT(*)                                    AS train_count,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) 
            OVER (), 1)                           AS percentage
    FROM risk_scores
    WHERE calculated_at = (
        SELECT MAX(calculated_at) FROM risk_scores
    )
    GROUP BY risk_label
    ORDER BY train_count DESC
""")

# ── Query 4: Delay Trend Over Time ───────────────────────────
run_query("Network Average Delay Trend (Last 10 Runs)", """
    SELECT 
        TO_CHAR(recorded_at, 'HH24:MI') AS time,
        ROUND(AVG(delay_mins), 1)        AS avg_network_delay,
        MAX(delay_mins)                  AS max_delay,
        COUNT(DISTINCT train_no)         AS trains_tracked
    FROM live_status
    GROUP BY recorded_at
    ORDER BY recorded_at DESC
    LIMIT 10
""")

# ── Query 5: On Time vs Delayed ───────────────────────────────
run_query("On Time vs Delayed Performance", """
    SELECT 
        status,
        COUNT(*)                                     AS count,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) 
            OVER (), 1)                            AS percentage
    FROM live_status
    GROUP BY status
    ORDER BY count DESC
""")

# ── Query 6: Most Consistently Delayed Trains ────────────────
run_query("Most Consistently Delayed Trains", """
    SELECT 
        t.train_name,
        ROUND(AVG(ls.delay_mins), 1)  AS avg_delay,
        COUNT(CASE WHEN ls.delay_mins > 30 
            THEN 1 END)             AS times_over_30mins,
        COUNT(*)                      AS total_snapshots
    FROM live_status ls
    JOIN trains t ON ls.train_no = t.train_no
    GROUP BY t.train_name
    HAVING COUNT(*) > 1
    ORDER BY avg_delay DESC
    LIMIT 10
""")