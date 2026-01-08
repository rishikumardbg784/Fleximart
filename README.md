# FlexiMart Data Architecture Project

**Student:** [Your Name]
**ID:** [Your ID]

## Overview
This repository contains a comprehensive data solution for FlexiMart, an e-commerce platform. It demonstrates the full data lifecycle:
1.  **ETL:** Cleaning "dirty" CSV data (formatting phones, fixing dates) and loading it into MySQL.
2.  **NoSQL:** Designing a MongoDB schema to handle flexible product attributes and nested reviews.
3.  **Data Warehousing:** Implementing a Star Schema for OLAP analytics to answer high-level business questions.

## Repository Structure
* `data/`: Contains raw CSV datasets (Customers, Products, Sales).
* `part1-database-etl/`: Python ETL script and Relational Schema docs.
* `part2-nosql/`: MongoDB operations and trade-off analysis.
* `part3-datawarehouse/`: Star Schema SQL scripts and analytics queries.

## Key Learnings
* **Data Quality is Critical:** Writing the Python regex to clean phone numbers taught me that real-world data is rarely perfect.
* **OLTP vs OLAP:** I learned that while 3NF is great for transactions, it is terrible for analytics. The Star Schema (Part 3) made writing reports much easier.