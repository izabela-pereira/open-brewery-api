# Open Brewery API full extraction
Open Brewery API full extraction, including data transformation and delta file and delta table delivery, considering medallion architecture. The project was developed using Azure Cloud, Databricks (with Python and Pyspark) and dbt for data quality tests. 

# Introduction
This project was developed considering the medallion architecture, using Microsoft Azure Cloud as the main environment, with resources as ADLS Gen2 for storage, Azure Data Factory for pipeline management and Databricks platform for developing and validating code. Databricks Unity Catalog was used via Databricks integration with dbt cloud to implement testing on the table created as a silver layer product, after transformation.

## Architecture Proposal
The architecture proposal considered practicality, performance (cloud usage guarantees scalability and high availability) and easy to integrate tools.

<img width="1464" height="529" alt="image" src="https://github.com/user-attachments/assets/058a9c62-f603-4003-9400-d1ae22f7c94a" />

Microsoft Azure was the chosen cloud because of its possibility to use a free account and high information availability to help understand the environment as well as the possibility to work with Databricks internally. However, the free account brings some limitations as the inability to start compute clusters on Databricks (there is the possibility to work with serverless compute) and on Azure Data Factory.

dbt Cloud was the chosen tool for testing because it is one of the most widely used tools for data projects nowadays and it has a lot of information available online. Also, it is easily connected to Databricks as it has a connector that allows using Unity Catalog.

Apache Airflow was chosen because it is easy to set up and use, provides reliable workflow orchestration, and includes strong monitoring and alerting through its web UI and integrations.

### Azure Resource creation
The resources created on Azure Cloud were:
  - Group Resource: needed to group the other resources created for the project. Easy to create, demands only for an Azure valid subscription;
  - ADLS Gen2 storage: storage containers for each layer. It demands a storage account, created inside the group resource, with recomended GRS storage. The account followed most of the deafult configuration and three containers were created inside de Blob (storage account) that are  'bronze-layer', 'silver-layer' and 'gold-layer';
  - Azure Data Factory (ADF): the ADF creation demands only for a resource group. Most of the configuration was set as default. After created, de ADF Studio is available and it makes possible to create pipelines and schedules for this pipelines. The pipeline creation will be described later in this README file.
  - Databricks Workspace: the Databricks Workspace creation demands only for a resource group

Ps: the .json files with all the resources configuration are available with the author.

### dbt Cloud and Databricks integration

# API Extraction and Exploratory Data Analysis
## API Extraction
The data was extracted from [Open Brewery API](https://www.openbrewerydb.org/) and considered the page number and per_page parameters to guarantee complete extraction and optimization.

## Exploratory Data Analysis
Before starting the code development for transformation, an exploratory data analysis was conducted to understand data patterns and quality. This notebook used the bronze layer extraction as the source, since the data was extracted as-is, and it is also available in this repository.

# Medallion architecture implementation
The project followed medallion architecture as detailed bellow:

### Bronze Layer
The bronze layer data was stored as-is, maintaining its original format as **JSON** for auditability, with no transformations. The bronzelayer notebook is responsible for the data extraction and storage in the ADLS Gen2 bronze layer.

### Silver Layer
In the silver layer, the transformations were made considering the exploratory analysis conducted with the bronze layer data. The transformations and their purposes are described below:
1. **state_province** column was **dropped** since its data was identical to the state column when records were compared;;
2. **duplicates were removed**;
3. **null** values were **replaced** in the columns where they were present
  - The values were replaced by **zero** in latitude and longitude **(type double)** and by **NA** in the other columns **(type string).**
4. **Standardization of string values**
  - Columns **country** and **state** were not stardardized, showing differences in capitalization and containing blank spaces. Column country had its values standardized using the trim and initcap functions, while state passed through trim and upper functions.
  - A **dat_load** column was added to guarantee data extraction traceability and to retain this information for future data quality tests.
5. The data was saved in the ADLS Gen2 silver layer storage in **delta format**, partitioned by **location** using country and state, since using city would result in partitions that were too small and not meaningful.
6. A table was created with the data in Unity Catalog to be used by **dbt** for data quality tests.
**IMPORTANT:** During the creation of the silver layer dataset, the schema was defined manually because the **address_3** column was omitted by Spark. This likely occurred because the column contains a large number of null values.

### Gold Layer
In the gold layer, the data was grouped by location and brewery type to deliver the number of each type of brewery in each city. The data was saved in the ADLS Gen2 gold layer storage in **delta format**, and a table was created to improve querying and visualization.

# Developing
## Databricks notebooks
## ADF Pipeline and schedulation
- Airflow
## Data Quality test with dbt
##Monitoring/Alerting/Error handling
