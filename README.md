# ⚽ Football Stats

A data engineering project that processes football match data from a raw CSV file, cleans and validates it, loads it into a **PostgreSQL** database, and prepares views for analysis. The processed data can be further visualized in **Power BI**.  

This project was created to gain experience with **data handling (240k+ rows), Docker, PostgreSQL, and data engineering workflows**.  

Data source: Gábor, A. (2025). Club Football Match Data. Retrieved from https://github.com/xgabora/Club-Football-Match-Data-2000-2025/.

---

## 🚀 Tech Stack
- **Python** (ETL scripts with `pandas`)  
- **PostgreSQL** (data storage, views)  
- **Docker** (containerized setup)  
- **Power BI** (data visualization)  

---



## 📂 Project Structure
Football-Stats/  
│-- Data/ # Raw and processed CSV files  
│-- PostgreSQL/ # SQL scripts, schema definitions  
│-- Power-BI/ # Power BI dashboards and reports  
│-- src/ # Helper modules (cleaning, ETL functions)  
│-- .env # Environment variables (DB credentials etc.) You have to create it  
│-- docker-compose.yml # Docker setup for PostgreSQL  
│-- Dockerfile # Docker image build for Python environment  
│-- main.py # Main pipeline script  
│-- requirements.txt # Python dependencies  

---

## ⚡ Features
- Load football statistics from CSV (**240,000+ rows**).  
- Clean and validate raw data using **pandas**.  
- Insert teams and matches into PostgreSQL tables.  
- Automatically replace team names with IDs for consistency.  
- Create SQL **views** for easier data analysis.  
- Connect to **Power BI** for visualization.  

---

## 🔧 Installation & Setup

1. **Clone the repository**  
```bash
git clone https://github.com/szabilukacs/football-stats.git
cd football-stats
```

Create your .env file
```bash
DB_USER = ""
DB_PASS = ""
DB_HOST = ""
DB_PORT = ""
DB_NAME = ""
```

The script will:  
1. Load raw CSV data.  
2. Clean & validate it.  
3. Insert data into PostgreSQL tables.  
4. Create analysis-friendly views.  

After running, open **Power BI** (or another BI tool) to the PostgreSQL database and start building dashboards.  