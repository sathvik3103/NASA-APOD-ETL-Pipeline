## Project Overview: Airflow ETL pipeline with Postgres and API integration in Astro Cloud and AWS
This project involves creating an ETL (Extract, Transform, Load) pipeline using **Apache Airflow**. The pipeline extracts **data from an external API (in this case, NASA's Astronomy Picture of the Day (APOD) API)**, transforms the data, and loads it into a Postgres database. The entire workflow is orchestrated by Airflow to allow scheduling, monitoring, and managing workflows.

The project also leverages **Docker** to run Airflow and Postgres as services, ensuring an isolated and reproducible environment. We also utilize Airflow hooks and operators to handle the ETL process efficiently.

### Key Components of the Project:

**Airflow for Orchestration:** to define, schedule, and monitor the entire ETL pipeline. Also to manage task dependencies, ensuring that the process runs sequentially and reliably.

**Airflow DAG (Directed Acyclic Graph):** to define the workflow, which includes tasks like data extraction, transformation, and loading.

**Postgres Database:** to store the extracted and transformed data. Postgres is hosted in a **Docker** container, making it easy to manage and ensuring data persistence through Docker volumes. We interact with Postgres using Airflow’s PostgresHook and PostgresOperator.

**NASA API (Astronomy Picture of the Day):** The external API used in this project is NASA’s APOD API, which provides data about the astronomy picture of the day, including metadata like the title, explanation, and the URL of the image. We also use Airflow’s SimpleHttpOperator to extract data from the API.

### Objectives of the Project:

**Extract Data:** The pipeline extracts astronomy-related data from NASA’s APOD API on a scheduled basis (daily, in this case).

**Transform Data:** Transformations such as filtering or processing the API response are performed to ensure that the data is in a suitable format before being inserted into the database.

**Load Data into Postgres:** The transformed data is loaded into a Postgres database. The data can be used for further analysis, reporting, or visualization.

### Architecture and Workflow:
The ETL pipeline is orchestrated in Airflow using a DAG (Directed Acyclic Graph). The pipeline consists of the following stages:

1. Extract (E):
The SimpleHttpOperator is used to make HTTP GET requests to NASA’s APOD API.
The response is in JSON format, containing fields like the title of the picture, the explanation, and the URL to the image.
2. Transform (T):
The extracted JSON data is processed in the transform task using Airflow’s TaskFlow API (with the @task decorator).
This stage involves extracting relevant fields like title, explanation, url, and date and ensuring they are in the correct format for the database.
3. Load (L):
The transformed data is loaded into a Postgres table using PostgresHook.
If the target table doesn’t exist in the Postgres database, it is created automatically as part of the DAG using a create table task.

**Postgres hosted on AWS RDS:**

![Postgres hosted on AWS RDS](https://github.com/user-attachments/assets/34184d85-5d1b-4dad-b21a-9f9d44c2bee3)

**Viewing this Postgres SQL table using DBeaver:**
![Postgres SQL table from AWS](https://github.com/user-attachments/assets/5fb0f9fd-273f-4dd9-8231-9c02ef082a8d)

**Airflow UI output:**
![Airflow UI](https://github.com/user-attachments/assets/47b8e60b-d359-4263-81f0-0093fd827025)

