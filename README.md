# Open Brewery API full extraction
Open Brewery API full extraction, including data transformation and delta file and delta table delivery, considering medallion architecture. The project was developed using Azure Cloud, Databricks (with Python and Pyspark) and dbt for data quality tests. 

# Introduction
This project was developed considering the medallion architecture, using Microsoft Azure Cloud as the main environment, with resources as ADLS Gen2 for storage, Azure Data Factory for pipeline management and Databricks platform for developing and validating code. Databricks Unity Catalog was used via Databricks integration with dbt cloud to implement testing on the table created as a silver layer product, after transformation.

## Architecture Proposal
The architecture proposal considered practicality, performance (cloud usage guarantees scalability and high availability) and easy to integrate tools.

Microsoft Azure was the chosen cloud because of its possibility to use a free account and high information availability to help understand the environment as well as the possibility to work with Databricks internally. However, the free account brings some limitations as the inability to start compute clusters on Databricks (there is the possibility to work with serverless compute) and on Azure Data Factory.

dbt Cloud was the chosen tool for testing because it is one of the most widely used tools for data projects nowadays and it has a lot of information available online. Also, it is easily connected to Databricks as it has a connector that allows using Unity Catalog.

<img width="1464" height="529" alt="image" src="https://github.com/user-attachments/assets/058a9c62-f603-4003-9400-d1ae22f7c94a" />

# API Extraction and Exploratory Data Analysis
## API Extraction
The data was extracted from [Open Brewery API](https://www.openbrewerydb.org/) and considered the page number and per_page parameters to guarantee complete extraction and optimization.

## Exploratory Data Analysis
Before starting the code development for transformation, a exploratory data analysis was conducted to understand data pattern and quality. This notebook used bronze layer extraction as the source, since the data was extracted as it is, is also available in this repository.
