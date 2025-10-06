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
The bronze layer data was stored as-is, mainteining its original format, as json file for auditability, and with no transformation. The 'bronzelayer' notebook is responsible for the data extraction and storage in the bronze layer ADLS Gen2 bronze layer.

### Silver Layer

### Gold Layer

# Developing
## Databricks notebooks
## ADF Pipeline and schedulation
- Airflow
