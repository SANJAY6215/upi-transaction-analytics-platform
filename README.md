# UPI Transaction Analytics Platform

A complete **Data Engineering and Analytics project** that processes UPI transaction data using an ETL pipeline and visualizes insights through an interactive dashboard.

---

## 🚀 Project Overview

This project simulates a **UPI transaction analytics system** used by fintech companies to analyze transaction patterns, detect suspicious transactions, and monitor merchant performance.

The system performs:

- Data extraction
- Data transformation
- Data loading into PostgreSQL
- Automated workflow orchestration using Apache Airflow
- Interactive analytics dashboard using Streamlit

---

## 🏗️ Architecture

Airflow DAG  
↓  
Python ETL Pipeline  
↓  
PostgreSQL Data Warehouse (Docker)  
↓  
Streamlit Analytics Dashboard  

---

## 🛠️ Tech Stack

- Python
- PostgreSQL
- Docker
- Apache Airflow
- Streamlit
- Pandas
- SQLAlchemy
- Git & GitHub

---

## 📊 Features

### Transaction Analytics
- Total transaction monitoring
- Merchant transaction rankings
- Transaction status analysis

### Fraud Detection
- Identifies suspicious transactions
- Displays fraud transactions in dashboard

### Merchant Insights
- Top merchants by number of transactions
- Merchant performance analytics

### Automated Data Pipeline
- Airflow DAG schedules ETL workflow
- Data loaded into PostgreSQL warehouse

---

## 📂 Project Structure


upi-transaction-analytics-platform
│
├── airflow/
│ └── upi_pipeline_dag.py
│
├── dashboard/
│ └── dashboard.py
│
├── etl/
│ ├── extract/
│ ├── transform/
│ └── load/
│
├── docker/
│ └── docker-compose.yml
│
├── main.py
├── requirements.txt
└── README.md


---

## ⚙️ How to Run the Project

### 1️⃣ Start Docker Services

```bash
docker compose -f docker/docker-compose.yml up -d
2️⃣ Run ETL Pipeline
python main.py
3️⃣ Launch Analytics Dashboard
streamlit run dashboard/dashboard.py

Open browser:

http://localhost:8501
📈 Dashboard Insights

The dashboard provides:

Transaction trends

Merchant transaction rankings

Fraud transaction detection

Real-time analytics visualization

🎯 Future Improvements

Real-time transaction streaming using Kafka

Machine learning based fraud detection

Advanced analytics dashboard

Cloud deployment (AWS / GCP)

👨‍💻 Author

Sanjay B


---

# 2️⃣ Add README to Git

Run:

```bash
git add README.md
3️⃣ Commit
git commit -m "Added project README"
4️⃣ Push to GitHub
git push origin main

