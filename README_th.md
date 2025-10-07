# BMW Seller — ETL โปรเจ็ค (ภาษาไทย)

เอกสารสำหรับโปรเจ็ค "BMW Seller" — ETL สำหรับข้อมูลการขายรถยนต์

## ภาพรวม
โปรเจ็คนี้เป็น pipeline แบบ ETL (Extract → Transform → Load) ที่อ่านข้อมูลดิบจากไฟล์ CSV (`data/raw/BMW_sales_data_(2010-2024).csv), ทำความสะอาดและสร้างชุดข้อมูลสรุป แล้วบันทึกเป็นไฟล์ CSV/Parquet พร้อมโหลดลงฐานข้อมูล SQLite เพื่อใช้วิเคราะห์และสร้าง visualization

## โครงสร้างโปรเจ็ค
- data/raw/ - ไฟล์ข้อมูลดิบ (ตัวอย่าง: `BMW_sales_data_(2010-2024).csv)
- data/processed/ - ไฟล์ผลลัพธ์ที่ผ่านการแปลง/clean แล้ว
- data/db/ - ไฟล์ฐานข้อมูล SQLite ที่สร้างขึ้น
- scripts/ - สคริปต์ ETL และช่วยงาน
  - extract.py - ตรวจสอบ/อ่านข้อมูลดิบ
  - transform_cleaned.py - ทำความสะอาดและแปลงข้อมูล (เพิ่ม Car_ID, แปลงหน่วย, จัดการ outliers, สร้างฟีเจอร์)
  - transform_summary.py - สร้างข้อมูลสรุป (group by Region + Fuel_Type + Year)
  - create_table.py - สร้างตารางใน SQLite
  - load.py - โหลด CSV/Parquet ลงใน SQLite (ตาราง cleaned และ summary)
- notebooks/ - โน้ตบุ๊กสำหรับ EDA และ visualization (EDA.ipynb, main.ipynb)
- utils/ - โมดูลช่วยเหลือ logger.py
- logs/ - บันทึกการรัน

## สเป็คสั้น ๆ
- Input: data/raw/BMW_sales_data_(2010-2024).csv (CSV ดิบ)
- Outputs:
  - cleaned CSV/Parquet: data/processed/bmw_cleaned.csv
  - summary CSV/Parquet: data/processed/bmw_summary.csv
  - SQLite DB: data/db/bmw_sales.db (ตาราง cleaned, summary)

## ขั้นตอน ETL (สรุป)
1. Extract: อ่าน CSV ดิบ, ตรวจสอบ schema, missing values, duplicate
2. Transform (clean): เพิ่ม Car_ID, แปลง km→miles, แปลงราคา USD→THB (configurable), จัดการ outliers, สร้าง Car_Age และ Revenue, บันทึก cleaned
3. Transform (summary): group by Region, Fuel_Type, Year คำนวณ total_sales, total_revenue, average_price เพิ่ม Summary_ID บันทึก summary
4. Load: สร้าง/เชื่อม SQLite และโหลดข้อมูลลงตาราง cleaned และ summary
5. Visualization: สร้าง bar/line/pie charts สำหรับการนำเสนอ

## ตัวอย่างคำสั่ง (Windows cmd)
bat
python scripts\transform_cleaned.py --input data\raw\BMW_sales_data_(2010-2024).csv --output data\processed\bmw_cleaned.csv --usd-to-thb 35.0
python scripts\transform_summary.py --input data\processed\bmw_cleaned.csv --output data\processed\bmw_summary.csv
python scripts\create_table.py --db data\db\bmw_sales.db
python scripts\load.py --db data\db\bmw_sales.db --cleaned data\processed\bmw_cleaned.csv --summary data\processed\bmw_summary.csv

## แนวทางนำไปพัฒนาใน AWS (สรุป)
- เก็บ raw/processed ใน S3 (ใช้ Parquet สำหรับงานวิเคราะห์)
- ใช้ AWS Glue (PySpark) สำหรับ batch ETL ขนาดกลาง-ใหญ่, หรือ Lambda+StepFunctions สำหรับงานเล็ก/event-driven
- ใช้ Athena สำหรับ query แบบ serverless, หรือ Redshift สำหรับ data warehouse
- เก็บ secrets ใน Secrets Manager/SSM และเปิดใช้ KMS/SSE สำหรับ S3
- ใช้ IaC (Terraform/CloudFormation/CDK) และ CI (GitHub Actions / CodePipeline)
