# 🚆 Real-time railway delay simulation pipeline with Power BI dashboard for risk analysis and trend monitoring.

## 📌 Overview

Railway Delay Tracker is a real-time simulation-based data pipeline that monitors train delays, classifies risk levels, and visualizes insights through an interactive Power BI dashboard.

The project demonstrates an end-to-end workflow:
**Data Simulation → Storage → Processing → Visualization**

---

## ⚙️ Features

* 🚂 Simulates real-time train delays
* ⚠️ Classifies risk levels (HIGH / MEDIUM / LOW)
* 📊 Maintains historical time-series dataset
* 📈 Interactive Power BI dashboard
* 🔄 Automated pipeline using scheduler (runs every 5 minutes)

---

## 🏗️ Project Architecture

```
Scheduler → Simulator → CSV / DB → Power BI Dashboard
```

* **Simulator** → Generates delay data
* **CSV Storage** → Maintains historical records
* **(Optional) Database** → Structured storage
* **Power BI** → Visualization & insights

---

## 📁 Project Structure

```
railway-tracker/
│
├── simulator.py        # Generates train delay data
├── scheduler.py        # Runs pipeline every 5 minutes
├── train_list.py       # Train metadata
├── export.py           # Aggregated exports (optional)
│
├── data/
│   └── train_history.csv   # Time-series dataset
│
├── dashboard.pbix      # Power BI dashboard
├── Dashboard.png       # Dashboard preview
│
├── .gitignore
└── README.md
```

---

## 📊 Dashboard

![Dashboard](Dashboard.png)

### Insights provided:

* 📈 Delay trend over time
* ⚠️ Risk distribution of trains
* 🚂 Top delayed trains
* 📋 Live train status (latest snapshot)

---

## 🧠 Key Concepts Used

* Time-series data handling
* Data pipeline design
* Risk classification logic
* Data aggregation & filtering
* Dashboard design principles

---

## 🛠️ Tech Stack

* **Python**

  * pandas
  * datetime
  * apscheduler
* **Power BI**
* **Git & GitHub**

---

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/railway-delay-tracker.git
cd railway-delay-tracker
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run scheduler

```bash
python scheduler.py
```

---

## 📌 Notes

* Data is stored in `train_history.csv`
* Only last 10 records per train are retained
* Dashboard updates dynamically with new data

---

## 🚀 Future Improvements

* Real API integration (live railway data)
* Deployment on cloud (AWS / GCP)
* Stream processing (Kafka / Spark)
* Advanced predictive analytics

---

## 👤 Author

**Saksham**

---

## ⭐ If you found this useful

Give it a star ⭐ on GitHub!
