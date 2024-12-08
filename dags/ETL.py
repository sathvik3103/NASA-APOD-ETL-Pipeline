from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.decorators import task
from datetime import datetime
from airflow.providers.postgres.hooks.postgres import PostgresHook
import json
from airflow.utils.dates import days_ago

# Define the basic parameters of the DAG, like schedule and start_date
with DAG(
    dag_id='NASA_APOD_POSTGRES',
    start_date=days_ago(1),
    schedule_interval='@daily',
    catchup=False
)as dag:
    
    # Step 1: Creating a Table. 
    @task
    def create_table():

        postgres_hook=PostgresHook(postgres_conn_id='my_postgres_connection')

        create_table_query="""
        CREATE TABLE IF NOT EXISTS apod_data (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            explanation TEXT,
            url TEXT,
            date DATE,
            media_type VARCHAR(50)
        );
        """
        postgres_hook.run(create_table_query)

    # Step 2: Extracting the NASA API Data.
    extract_apod = SimpleHttpOperator(
            task_id='extract_apod',
            http_conn_id='nasa_api', ## Connection ID Defined In Airflow For NASA API
            endpoint='planetary/apod', ## NASA API enpoint for APOD
            method='GET',
            data={"api_key":"{{ conn.nasa_api.extra_dejson.api_key}}"}, ## USe the API Key from the connection
            response_filter=lambda response:response.json() ## Convert response to json
        )

    # Step 3: Transforming the extracted data.
    @task
    def transform_apod_data(response):
        apod_data={
            'title': response.get('title', ''),
            'explanation': response.get('explanation', ''),
            'url': response.get('url', ''),
            'date': response.get('date', ''),
            'media_type': response.get('media_type', '')

        }
        return apod_data
    # Step 4: Loading the transformed data into Postgres SQL
    @task
    def load_data_to_postgres(apod_data):
        ## Initializing the PostgresHook
        postgres_hook=PostgresHook(postgres_conn_id='my_postgres_connection')

        ## Defining the SQL Insert Query

        insert_query = """
        INSERT INTO apod_data (title, explanation, url, date, media_type)
        VALUES (%s, %s, %s, %s, %s);
        """
        ## Executing the SQL Query

        postgres_hook.run(insert_query,parameters=(
            apod_data['title'],
            apod_data['explanation'],
            apod_data['url'],
            apod_data['date'],
            apod_data['media_type']
        ))
    # Step 6: Defining the task dependencies

    create_table() >> extract_apod 
    api_response=extract_apod.output
    transformed_data=transform_apod_data(api_response)
    load_data_to_postgres(transformed_data)

