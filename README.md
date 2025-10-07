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

# API Extraction and Exploratory Data Analysis
## API Extraction
The data was extracted from [Open Brewery API](https://www.openbrewerydb.org/) and considered the page number and per_page parameters to guarantee complete extraction and optimization.

## Exploratory Data Analysis
Before starting the code development for transformation, an exploratory data analysis was conducted to understand data patterns and quality. This notebook used the bronze layer extraction as the source, since the data was extracted as-is, and it is also available in this repository.

# Medallion architecture implementation
The project followed medallion architecture as detailed bellow:

### Bronze Layer
The bronze layer data was stored as-is, maintaining its original format as **JSON** for auditability, with no transformations. 

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
6. A delta table was created with the data in Unity Catalog to be used by **dbt** for data quality tests.

**IMPORTANT:** During the creation of the silver layer dataset, the schema was defined manually because the **address_3** column was omitted by Spark. This likely occurred because the column contains a large number of null values.

### Gold Layer
In the gold layer, the data was grouped by location and brewery type to deliver the number of each type of brewery in each city. The data was saved in the ADLS Gen2 gold layer storage in **delta format**, and a delta table was created to improve querying and visualization.

# Developing
The entire project was developed using Databricks, as it is a comprehensive platform that offers scalability, efficiently handles datasets of all sizes, and allows workloads to scale as needed. In addition, Databricks provides a wide range of connectors to various data sources and other platforms, such as dbt, simplifying data integration.

## Databricks
After creating a Databricks workspace using the resource group initially created, a credential was created for the project, as well as three external connections with ADLS Gen2 storage containers, so that the data could be stored and accessed by the notebooks. 

### Databricks notebooks
- bronzelayer - responsible for the data extraction and storage in the ADLS Gen2 bronze-layer in JSON format;
- silverlayer - responsible for data transformation and storage in the ADLS Gen2 silver-layer in delta format as well as the creation of a delta table for dbt-conducted data quality tests;
- goldlayer - responsible for the data aggregation and storage in the ADLS Gen2 gold-layer in delta format, as well as the creation of a delta table for querying and better visualization.

### Databricks and dbt
Databricks offers several connectors in its Marketplace tab, including **dbt connector**. A connection was created, and tests were developed using **dbt Cloud**. Evidence can be found in **dbt** folder of this project. 

### Databricks jobs
Two different jobs were created in Databricks: one **including dbt**, which unfortunately **failed** and remains as a technical debt, and another **without dbt tests** which ran  **successfully**. Both evidences can be found in **databricks/jobs** folder of this project.

## dbt tests
dbt was the chosen tool for conducting data quality tests. 
dbt Cloud Studio was used for creating and validating tests, and the **model** (including implemented tests), the **macro** of a custom test, and **evidence** of execution can be found in **dbt** folder of this project.
Of the tests implemented, two failed while all others passed.
- **test_table_not_empty** (custom test) failed and couldn't be fixed within the project deadline; it also remains as a technical debt. 
- **test accepted values**, applied to **brewery_type** column, failed because the dataset includes values different from those listed as valid in the API documentation for the field.

## ADF Pipeline and Scheduling / Apache Airflow
As proposed initially, an Azure Data Factory (ADF) pipeline was created; however the free account doesn´t allow the creation of custom clusters to run it, and it is still not possible to use serverless clusters. Evidence of the pipeline creation is available in **datafactory/pipeline_trigger** of this project.

A trigger was also created to schedule ADF pipeline runs, since it wasn´t possible to set up an integration with **Apache Airflow**, as initially suggested. Airflow integration with ADF does exist, but it is also not available for free accounts.

Despite the fact that Airflow connection was not possible, a DAG model was created following the official documentation as an example, and it is available in the **airflow** folder of this project.

# Monitoring/Alerting/Error handling

