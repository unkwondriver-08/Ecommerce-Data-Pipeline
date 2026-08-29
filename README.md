# 🛒 E-commerce Data Integration & Insights Pipeline

An end-to-end **E-commerce Data Engineering and Analytics project** built to transform raw transactional data into clean, analysis-ready datasets and generate meaningful business insights.

The project covers the complete data workflow — **data ingestion, data cleaning, transformation, integration, data modeling, analytical metrics, and visualization** — using a real-world Brazilian e-commerce dataset.

---

## 📌 Project Overview

E-commerce platforms generate data across multiple business processes such as:

* Customers
* Orders
* Products
* Sellers
* Payments
* Reviews
* Order items
* Geolocation

These datasets are stored separately and contain inconsistencies, missing values, duplicate records, and relationships that need to be properly integrated before meaningful analysis can be performed.

This project builds a scalable pipeline to:

> **Raw Data → Data Cleaning → Data Transformation → Data Integration → Data Modeling → Business Analytics → Insights**

The final objective is to understand **sales performance, customer behavior, product performance, seller performance, delivery experience, and customer satisfaction.**

---

## 🎯 Objectives

* Build an end-to-end **ETL/ELT data pipeline**
* Clean and standardize raw e-commerce datasets
* Integrate multiple relational datasets
* Perform data quality and consistency checks
* Create an analytical data model
* Calculate important e-commerce KPIs
* Analyze customer and order behavior
* Identify high-performing products and sellers
* Analyze delivery performance and customer reviews
* Generate actionable business insights
* Prepare the pipeline for scalable processing using **PySpark and GCP**

---

## 🗂️ Dataset

The project uses the **Brazilian E-Commerce Public Dataset by Olist**, containing approximately 100K orders placed between **2016 and 2018**.

### Main datasets

| Dataset              | Description                                   |
| -------------------- | --------------------------------------------- |
| Customers            | Customer information and location             |
| Orders               | Order lifecycle and timestamps                |
| Order Items          | Products purchased in each order              |
| Products             | Product attributes                            |
| Sellers              | Seller information and location               |
| Payments             | Payment methods and transaction values        |
| Reviews              | Customer ratings and review information       |
| Geolocation          | Brazilian zip-code geolocation data           |
| Category Translation | Portuguese → English product category mapping |

---

## 🏗️ Project Architecture

```text
                    ┌─────────────────────┐
                    │    Raw CSV Data     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Data Ingestion     │
                    │   & Validation      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Data Cleaning     │
                    │ Missing / Duplicate │
                    │  / Data Types       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Transformation &    │
                    │    Integration      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Data Modeling     │
                    │ Fact & Dimension    │
                    │      Tables         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Business Analytics  │
                    │   & KPI Generation  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Insights &          │
                    │ Visualization       │
                    └─────────────────────┘
```

---

## 🛠️ Tech Stack

### Data Engineering

* **Python**
* **PySpark**
* Apache Spark

### Data Analysis

* **Pandas**
* **NumPy**
* SQL

### Cloud & Big Data

* **Google Cloud Platform (GCP)**
* Google Cloud Storage
* Dataproc

### Visualization

* Power BI / Python visualization

### Development & Version Control

* Jupyter Notebook
* Git
* GitHub

---

## 📁 Project Structure

```text
Ecommerce Data Pipeline/
│
├── Data/
│   ├── raw/
│   │   └── *.csv
│   │
│   └── Processed/
│       └── .gitkeep
│
├── Notebooks/
│   ├── 01_data_inspection.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_data_transformation.ipynb
│   ├── 04_data_integration.ipynb
│   └── 05_business_analysis.ipynb
│
├── src/
│   ├── ingestion/
│   ├── cleaning/
│   ├── transformation/
│   └── analytics/
│
├── docs/
│   ├── data_inspection_notes.md
│   └── data_relationships.md
│
├── README.md
└── .gitignore
```

> The project structure will evolve as the pipeline moves from exploratory analysis toward a production-style implementation.

---

# 🔄 Data Pipeline

## 1. Data Ingestion

Raw CSV files are loaded into the pipeline and inspected for:

* Number of records
* Number of columns
* Data types
* Missing values
* Duplicate records
* Unique identifiers
* Date/time fields

---

## 2. Data Cleaning

The cleaning stage focuses on improving data quality through:

* Handling missing values
* Removing duplicate records
* Correcting data types
* Standardizing column names
* Parsing date/time columns
* Handling inconsistent categorical values
* Validating primary and foreign-key relationships

---

## 3. Data Transformation

The cleaned datasets are transformed into analysis-ready structures.

Examples include:

* Calculating order-level revenue
* Calculating item-level revenue
* Creating delivery duration
* Creating purchase month/year
* Standardizing product categories
* Aggregating customer-level metrics
* Aggregating seller-level metrics

---

## 4. Data Integration

The individual datasets are connected using their relational keys.

Example:

```text
Customers
    │
    │ customer_id
    ▼
Orders
    │
    │ order_id
    ├──────────────► Order Items
    │                    │
    │                    │ product_id
    │                    ▼
    │                 Products
    │
    ├──────────────► Payments
    │
    └──────────────► Reviews

Order Items
    │
    └──────────────► Sellers
```

This creates a unified view of the customer journey from **purchase → payment → delivery → review**.

---

# 📊 Business Metrics & KPIs

The project focuses on several important e-commerce metrics.

### 💰 Sales Performance

* Total Revenue
* Total Orders
* Average Order Value (AOV)
* Revenue by Month
* Revenue by Product Category
* Revenue by Seller
* Revenue Growth

### 👥 Customer Analytics

* Total Customers
* Repeat Customers
* Customer Purchase Frequency
* Customer Lifetime Value indicators
* Revenue by Customer Location
* New vs Returning Customers

### 📦 Product Analytics

* Best-selling Products
* Best-performing Categories
* Revenue by Category
* Average Product Price
* Product Demand

### 🚚 Delivery Analytics

* Average Delivery Time
* Estimated vs Actual Delivery Time
* Late Delivery Rate
* Delivery Performance by Location

### ⭐ Customer Satisfaction

* Average Review Score
* Review Score Distribution
* Review Score vs Delivery Time
* Review Score by Product Category
* Review Score vs Order Experience

### 🏪 Seller Analytics

* Revenue by Seller
* Orders by Seller
* Seller Performance
* Seller Delivery Performance
* Seller Review Ratings

---

# 📈 Key Business Questions

The analysis aims to answer questions such as:

1. How has e-commerce revenue changed over time?
2. Which product categories generate the most revenue?
3. Which categories have the highest demand?
4. Which sellers contribute the most revenue?
5. What is the average customer order value?
6. What percentage of customers make repeat purchases?
7. Which regions generate the highest sales?
8. How long does it take for orders to reach customers?
9. How does delivery performance affect customer satisfaction?
10. Which product categories receive the highest ratings?
11. What factors are associated with poor customer reviews?
12. Which sellers perform best across revenue, delivery, and ratings?

---

# 🧠 Data Modeling

A dimensional modeling approach is planned for the analytical layer.

### Fact Tables

```text
Fact Orders
Fact Order Items
Fact Payments
Fact Reviews
```

### Dimension Tables

```text
Dim Customer
Dim Product
Dim Seller
Dim Date
Dim Location
```

This structure makes the data easier to query and supports efficient analytical workloads.

---

# 🔍 Data Quality Checks

The pipeline includes checks for:

* Null values
* Duplicate records
* Invalid dates
* Invalid numeric values
* Referential integrity
* Unexpected categorical values
* Duplicate primary keys
* Missing foreign-key relationships

Example:

```text
Orders
   │
   ├── customer_id → Customers.customer_id
   │
   └── order_id → Order Items.order_id
```

These checks help ensure that downstream analysis is based on reliable data.

---

# ☁️ Cloud Implementation

The pipeline is designed with **Google Cloud Platform** in mind.

Planned architecture:

```text
Local / Source Data
        │
        ▼
Google Cloud Storage
        │
        ▼
Google Cloud Dataproc
        │
        ▼
PySpark ETL
        │
        ▼
Processed Data
        │
        ▼
Analytical Layer
        │
        ▼
Power BI / Analytics
```

The cloud implementation allows the same processing workflow to be adapted for larger datasets and distributed computing environments.

---

# 📌 Current Progress

* [x] Dataset collected
* [x] Raw data structure created
* [x] Dataset inspection completed
* [x] Missing-value analysis
* [x] Data relationship analysis
* [x] Initial project structure
* [x] Git repository initialized
* [ ] Data cleaning pipeline
* [ ] Data transformation pipeline
* [ ] Dataset integration
* [ ] Analytical data model
* [ ] PySpark implementation
* [ ] Business KPI analysis
* [ ] Visualization dashboard
* [ ] GCP / Dataproc implementation
* [ ] Final insights & documentation

---

# 📚 Learning Outcomes

Through this project, I am developing practical experience in:

* End-to-end data pipelines
* ETL/ELT concepts
* Data cleaning and validation
* Relational data integration
* SQL-based analytics
* PySpark
* Distributed data processing
* Data modeling
* Business KPI development
* Cloud data engineering
* Git/GitHub project management

---

# 🚀 Future Improvements

Future versions of the project may include:

* Automated pipeline orchestration
* Incremental data processing
* Partitioned datasets
* Spark optimization
* Data quality automation
* Cloud-native ETL
* Pipeline monitoring
* Automated dashboard refresh
* Advanced customer segmentation
* Predictive analytics
* Customer churn prediction
* Demand forecasting

---

## 👨‍💻 Author

**Girdhari Kumar**

B.Tech — Industrial Design
Minor — Computer Science & Engineering

Focused on **Data Analytics, Data Engineering, SQL, Python, PySpark, and Business Intelligence**.

---

## ⭐ Project Goal

> Build a production-style e-commerce data pipeline that transforms raw, disconnected datasets into reliable analytical data and actionable business insights.
