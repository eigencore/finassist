from google.cloud import bigquery
from finassist.utils.utils import get_var_env

bq_client = None  # <-- Añade esta línea
bq_dataset = None  # <-- Y esta si usas get_bq_dataset

def get_bq_client():
    """Get BigQuery client."""
    global bq_client
    if bq_client is None:
        bq_client = bigquery.Client(project=get_var_env("BQ_PROJECT_ID"))
    return bq_client

def get_bq_dataset():
    """Get BigQuery dataset."""
    global bq_dataset
    if bq_dataset is None:
        bq_dataset = get_bq_client().dataset(get_var_env("BQ_DATASET_ID"))
    return bq_dataset

def get_user_context_info(user_id: str) -> str:
    """
    Get user context information from BigQuery.

    Returns:
        dict with user info and account list.
    """
    client = get_bq_client()
    dataset_id = get_var_env("BQ_DATASET_ID")
    project_id = get_var_env("BQ_PROJECT_ID")

    users_table = f"`{project_id}.{dataset_id}.users`"
    accounts_table = f"`{project_id}.{dataset_id}.accounts`"

    # Primero verificar si el usuario existe
    user_query = f"""
    SELECT
        user_id,
        full_name,
        preferred_currency,
        language,
        timezone
    FROM {users_table}
    WHERE user_id = @user_id
    """

    user_job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id)
        ]
    )

    user_job = client.query(user_query, job_config=user_job_config)
    user_results = list(user_job.result())

    if not user_results:
        return str({
            "error": "User not found."
        })

    user_row = user_results[0]

    # Luego obtener las cuentas del usuario
    accounts_query = f"""
    SELECT
        account_id,
        account_name,
        account_type,
        institution,
        currency,
        balance
    FROM {accounts_table}
    WHERE user_id = @user_id
    """

    accounts_job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id)
        ]
    )

    accounts_job = client.query(accounts_query, job_config=accounts_job_config)
    accounts_results = list(accounts_job.result())

    # Construir la respuesta
    return str({
        "user_id": user_row.user_id,
        "full_name": user_row.full_name,
        "preferred_currency": user_row.preferred_currency,
        "language": user_row.language,
        "timezone": user_row.timezone,
        "accounts": [
            {
                "account_id": acc.account_id,
                "account_name": acc.account_name,
                "account_type": acc.account_type,
                "institution": acc.institution,
                "currency": acc.currency,
                "balance": float(acc.balance) if acc.balance is not None else None,
            }
            for acc in accounts_results
        ]
    })