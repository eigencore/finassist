import uuid

from typing import Dict, Any

from google.adk.tools.tool_context import ToolContext
from google.adk.tools.function_tool import FunctionTool


from .utils.utils import get_env_var
from .subagents.bigquery.tools import get_bq_client


def create_record(
    entity: str,
    data: Dict[str, Any],
    tool_context: ToolContext = None
) -> Dict[str, Any]:
    """
    Create a new record in BQ table for the specified entity.
    
    Args:
        entity: The entity to create a record for (e.g., "transactions", "accounts")
        data: Dictionary with the data to insert
        tool_context: ToolContext object for the agent tool (optional)
        
    Returns:
        Diccionario con los resultados de la operación
    """
    try:
        # Get the environment variables for project and dataset
        project_id = get_env_var("BQ_PROJECT_ID")
        dataset_id = get_env_var("BQ_DATASET_ID")
        
        # Validate entity
        if entity not in ["transactions", "accounts"]: # So far only these two entities are supported
            return {
                "success": False,
                "error": f"Invalid entity: {entity}. Must be 'transactions' or 'accounts'."
            }
        
        # Validate data
        if not data:
            return {
                "success": False,
                "error": "No data provided for insertion"
            }
        
        # Table name based on entity
        table_name = f"`{project_id}.{dataset_id}.{entity}`"
        
        # Process the data
        processed_data = {}
        for key, value in data.items():
            # Manejamos valores automáticos
            if value == "auto":
                if key in ["transaction_id", "account_id"]: # TODO: Improve the logic for each entity
                    processed_data[key] = str(uuid.uuid4())
                elif key in ["recorded_date", "last_updated"]:
                    # BQ can handle CURRENT_TIMESTAMP() directly?
                    processed_data[key] = "CURRENT_TIMESTAMP()"
            else:
                processed_data[key] = value
        
        # Build the SQL query
        fields = []
        values = []
        
        for key, value in processed_data.items():
            fields.append(key)
            
            # Formateamos los valores según su tipo
            if value == "CURRENT_TIMESTAMP()":
                values.append("CURRENT_TIMESTAMP()")
            elif isinstance(value, (int, float)):
                values.append(str(value))
            elif isinstance(value, bool):
                values.append("true" if value else "false")
            elif isinstance(value, str) and key.endswith("_date"):
                # Asumimos que campos que terminan en _date son fechas
                values.append(f"DATE '{value}'")
            elif isinstance(value, str):
                # Escapamos comillas simples en strings
                escaped_value = value.replace("'", "''")
                values.append(f"'{escaped_value}'")
            else:
                values.append("NULL")
        
        # Construimos la consulta SQL final
        sql_query = f"""
        INSERT INTO {table_name}
        ({', '.join(fields)})
        VALUES
        ({', '.join(values)})
        """
        
        # Mostramos la consulta para depuración
        print(f"Executing SQL INSERT: {sql_query}")
        
        # Ejecutamos la consulta
        client = get_bq_client()
        query_job = client.query(sql_query)
        query_job.result()  # Esperamos a que termine
        
        # Determinamos qué tipo de ID devolver basado en la entidad
        id_field = "transaction_id" if entity == "transactions" else "account_id"
        entity_id = processed_data.get(id_field)
        
        # Preparamos la respuesta
        result = {
            "success": True,
            "operation_type": "CREATE",
            "entity": entity,
            "sql_query": sql_query,
            "results": {
                "inserted_row_count": query_job.num_dml_affected_rows
            },
            "status_message": f"{entity.capitalize()} created successfully"
        }
        
        # Añadimos el ID si está disponible
        if entity_id:
            result["results"][id_field] = entity_id
        
        return result
        
    except Exception as e:
        import traceback
        error_msg = f"Error creating {entity} record: {str(e)}"
        print(error_msg)
        print(traceback.format_exc())
        
        return {
            "success": False,
            "error": error_msg
        }
        

def execute_crud_operation(
    operation_data: Dict[str, Any],
    tool_context: ToolContext = None
) -> Dict[str, Any]:
    """
    Ejecuta una operación CRUD en la base de datos según los datos estructurados.
    
    Esta herramienta procesa directamente operaciones financieras sin necesidad 
    de generar SQL manualmente. Por ahora solo soporta operaciones CREATE (INSERT).
    
    Args:
        operation_data: Objeto JSON con la estructura de la operación.
            Debe contener:
            - operation: Por ahora solo "CREATE"
            - entity: "transactions" o "accounts"
            - data: Campos específicos para la operación
        tool_context: Contexto de la herramienta (opcional).
        
    Returns:
        Diccionario con los resultados de la operación.
        
    Ejemplo:
        Para registrar una transacción:
        {
          "operation": "CREATE",
          "entity": "transactions",
          "data": {
            "transaction_id": "auto",
            "user_id": "user_001",
            "amount": 5,
            "currency": "USD",
            "establishment": "Netflix",
            ...otros campos...
          }
        }
    """
    try:
        # Validar estructura básica
        if not isinstance(operation_data, dict):
            return {
                "success": False,
                "error": "Invalid input: operation_data must be a dictionary"
            }
        
        operation = operation_data.get("operation", "").upper()
        entity = operation_data.get("entity", "").lower()
        data = operation_data.get("data", {})
        
        # Validar operación y entidad
        if not operation or not entity:
            return {
                "success": False,
                "error": "Missing required fields: operation and entity"
            }
        
        # Por ahora, solo implementamos CREATE
        if operation == "CREATE":
            return create_record(entity, data, tool_context)
        else:
            return {
                "success": False,
                "error": f"Operation '{operation}' not yet implemented. Only CREATE is supported at this time."
            }
    
    except Exception as e:
        import traceback
        error_msg = f"Error executing CRUD operation: {str(e)}"
        print(error_msg)
        print(traceback.format_exc())
        
        return {
            "success": False,
            "error": error_msg
        }

# Crear la herramienta para usarla en tu agente
crud_service_tool = FunctionTool(
    func=execute_crud_operation
)