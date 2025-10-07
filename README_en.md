# BMW Seller — ETL Project (English)

Project README for the "BMW Seller" ETL pipeline that processes car sales data.

## Overview
This project implements an ETL (Extract → Transform → Load) pipeline which reads raw CSV data (data/raw/BMW_sales_data_(2010-2024).csv), produces cleaned and summary datasets, saves them as CSV/Parquet files, and loads them into a SQLite database for analysis and visualization.

## Project structure
- data/raw/ - raw data files (example: BMW_sales_data_(2010-2024).csv)
- data/processed/ - processed / cleaned output files
- data/db/ - generated SQLite database files
- scripts/ - ETL and helper scripts
  - extract.py - validate/read raw data
  - transform_cleaned.py - clean and transform (add Car_ID, convert units, handle outliers, create features)
  - transform_summary.py - build aggregated summary (group by Region + Fuel_Type + Year)
  - create_table.py - create tables in SQLite
  - load.py - load CSV/Parquet into SQLite (cleaned + summary tables)
- notebooks/ - notebooks for EDA and visualization (EDA.ipynb, main.ipynb)
- utils/ - helper modules logger.py
- logs/ - runtime logs

> If any script or filename differs in your copy of the repository, adjust the run commands accordingly.

## Contract / Quick specification
- Input: data/raw/BMW_sales_data_(2010-2024).csv (raw CSV)
- Outputs:
  - cleaned CSV/Parquet: data/processed/bmw_cleaned.csv (or .parquet)
  - summary CSV/Parquet: data/processed/bmw_summary.csv
  - SQLite DB: data/db/bmw_sales.db (two tables: cleaned and summary)
- Error modes: missing required columns, corrupted rows, I/O errors
- Success: cleaned + summary files produced and data loaded into SQLite

## ETL steps (summary)
1. Extract
   - Read raw CSV
   - Validate schema, detect missing values, check duplicates
2. Transform (clean)
   - Add Car_ID (unique car identifier)
   - Convert distance from kilometers → miles (1 km = 0.621371 mile)
   - Convert price from USD → THB (USD→THB exchange rate should be configurable)
   - Handle outliers (IQR trimming, z-score, or configurable thresholds)
   - Create features: Car_Age (current_year - manufacture_year), Revenue (Price * Quantity or Price if per-unit)
   - Write cleaned output to data/processed/bmw_cleaned.csv (or Parquet)
3. Transform (summary)
   - Read cleaned data
   - Group by Region, Fuel_Type, and Year
   - Compute metrics: total_sales, total_revenue, average_price
   - Optionally express total_revenue in billions (USD)
   - Add Summary_ID and optionally list related Car_ID
   - Write summary to data/processed/bmw_summary.csv
4. Load
   - Create/connect to SQLite DB (data/db/bmw_sales.db)
   - Create two tables: cleaned and summary
   - Load CSV/Parquet into appropriate tables
5. Visualizations
   - Bar chart: total sales by continent/region
   - Line chart: average sales per year
   - Pie chart: share of total sales by car type

## Installation (Windows - cmd.exe)
1) Create and activate a virtual environment (recommended)

bat
python -m venv .venv
.venv\Scripts\activate


2) Install dependencies

bat
pip install -r requirements.txt


## Example run commands (Windows cmd)
bat
python scripts\extract.py --input data\raw\BMW_sales_data_(2010-2024).csv --output data\processed\raw_checked.csv

python scripts\transform_cleaned.py --input data\raw\BMW_sales_data_(2010-2024).csv --output data\processed\bmw_cleaned.csv --usd-to-thb 35.0

python scripts\transform_summary.py --input data\processed\bmw_cleaned.csv --output data\processed\bmw_summary.csv

python scripts\create_table.py --db data\db\bmw_sales.db

python scripts\load.py --db data\db\bmw_sales.db --cleaned data\processed\bmw_cleaned.csv --summary data\processed\bmw_summary.csv

## AWS migration & productionization guidance (summary)
- Storage: S3 for raw & processed (use Parquet for analytics)
- ETL: Glue (PySpark) for batch, Lambda+StepFunctions for event-driven, or containerized jobs on ECS/Fargate
- Query: Athena for serverless querying, Redshift for data warehouse
- DB: RDS/Aurora for transactional needs
- BI: QuickSight or host Dash/Streamlit on ECS/Fargate
- Security: use Secrets Manager/SSM, KMS, and least-privilege IAM roles
- IaC/CI: Terraform/CloudFormation/CDK and GitHub Actions or CodePipeline
