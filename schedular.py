from apscheduler.schedulers.blocking import BlockingScheduler
from simulator import run_simulation
from export import export_all
from datetime import datetime
import pytz

ist = pytz.timezone('Asia/Kolkata')

def run_pipeline():
    run_simulation()

    try:
        export_all()
    except Exception as e:
        print("⚠️ Export skipped:", e)

    print("✅ Pipeline complete!\n")


scheduler = BlockingScheduler()
scheduler.add_job(run_pipeline, 'interval', minutes=5)

print(f"🚀 Started at {datetime.now(ist).strftime('%H:%M:%S')}")
print("⏰ Running every 5 minutes...\n")

run_pipeline()
scheduler.start()