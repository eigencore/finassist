import uuid

from financial_assist.subagents.bigquery.tools import get_bq_client
from financial_assist.utils.utils import get_env_var 

import uuid

from financial_assist.subagents.bigquery.tools import get_bq_client
from financial_assist.utils.utils import get_env_var 

def execute_sql(query: str):
    """
    Execute a SQL query on BigQuery.
    
    Args:
        query (str): The SQL query to execute.
    
    Returns:
        str: Success or error message with more details
    """
    client = get_bq_client()
    
    if not client:
        raise ValueError("BigQuery client is not available.")
    
    # Preprocess query
    query = query.replace("GENERATE_UUID()", f"'{str(uuid.uuid4())}'")
    query = query.replace("BQ_PROJECT_ID", get_env_var("BQ_PROJECT_ID"))
    query = query.replace("BQ_DATASET_ID", get_env_var("BQ_DATASET_ID"))
    
    print("======================")
    print(f"Executing query: {query}")
    print("======================")
    
    # Execute the query
    try:
        query_job = client.query(query)
        result = query_job.result()  # Wait for the job to complete
        
        # Get more details about the job
        print(f"Job ID: {query_job.job_id}")
        print(f"Job State: {query_job.state}")
        print(f"Rows affected: {query_job.num_dml_affected_rows}")
        print(f"Job errors: {query_job.errors}")
        
        return f"Query executed successfully. Job ID: {query_job.job_id}, Rows affected: {query_job.num_dml_affected_rows}"
        
    except Exception as e:
        print(f"Full error details: {e}")
        return f"Query execution failed: {str(e)}. Please check the query syntax and try again."