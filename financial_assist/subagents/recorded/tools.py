import uuid
from financial_assist.subagents.bigquery.tools import get_env_var, get_bq_client

def execute_sql_query(
    sql_query: str,
) -> str:
    
    client = get_bq_client()
    
    if not client:
        raise ValueError("BigQuery client is not available.")
    
    # Preprocess query
    sql_query = sql_query.replace("GENERATE_UUID()", f"'{str(uuid.uuid4())}'")
    sql_query = sql_query.replace("BQ_PROJECT_ID", get_env_var("BQ_PROJECT_ID"))
    sql_query = sql_query.replace("BQ_DATASET_ID", get_env_var("BQ_DATASET_ID"))
    
    print("======================")
    print(f"Executing query: {sql_query}")
    print("======================")
    
    # Execute the query
    try:
        query_job = client.query(sql_query)
        result = query_job.result()  # Wait for the job to complete
        

        return f"Query executed successfully. Job ID: {query_job.job_id}, Rows affected: {query_job.num_dml_affected_rows}"
        
    except Exception as e:
        print(f"Full error details: {e}")
        return f"Query execution failed: {str(e)}. Please check the query syntax and try again."
