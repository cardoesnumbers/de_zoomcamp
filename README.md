# Repository for the Data Engineering Zoomcamp 2026


DataTalks 9-week zoomcamp (Jan–Mar 2026).


For more information: https://github.com/DataTalksClub/data-engineering-zoomcamp


## Why?

I decided to take on this course because it seems like a natural continuation of the work I have been doing with data as data/business analyst, that is, making sure it flows across different stages to fulfill a purpose; without breaking on the way there. The possibility of learning use cases of additional tools primarily designed with this process (the moving of data) in mind was just to good to pass as it aligns directly with my interest both working with data and optimizing processes (thats the engineer in me speaking).




## Progress so far:

**Module 1: Containerization and Infrastructure as Code**
+ Docker and Docker Compose  
+ Running PostgreSQL with Docker
+ Infrastructure setup with Terraform
+ Introduction to GCP 


Comments and homework for this module can be found [here](w1_docker_terraform/w1_homework/README.md).


**Module 2: Workflow Orchestration**
+ Introduction to Workflow Orchestration
+ Getting Started With Kestra
+ Hands-On Coding Project: Build ETL Data Pipelines with Kestra

Comments and homework for this module right [here](w2_kestra/README.md).


Additionally, in this module I tested Github secrets built-in protection (**GitGuardian**) which sent a message soon after my secrets were exposed. Secrets were rotated, that is, new were created and exposed ones were revoked. Section showing the secret was also removed from compromised file. Old dead secret kept (for now?) in commit history.

**Module 3: Data Warehousing**

+ Introduction to BigQuery
+ Partitioning, clustering, and best practices
+ Machine learning in BigQuery


Comment and homework [here](w3_dw/README.md)


**Module 4: Analytics Engineering** 


+ Analytics Engineering and Data Modeling
+ dbt (data build tool) with DuckDB & BigQuery
+ Testing, documentation, and deployment

Comment and homework [here](w4_ae/README.md)

**Module 5: Data Platforms**

+ Building end-to-end data pipelines with Bruin
+ Data ingestion, transformation, and quality
+ Deployment to cloud (BigQuery)

Comment and homework [here](w5_bruin/README.md)


## Next up

- Module 5: Batch Processing (Spark, DataFrames and SQL, Internals of GroupBy and Joins)
- Module 6: Streaming (Kafka Streams and KSQL, Schema management with Avro)
- Final Project
