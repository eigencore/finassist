async def add_transaction(
    data_transaction: str,
):
    """This tool is used to add a transaction to the database.

    Args:
        data_transaction (str): A string in JSON format containing the transaction details.
    Returns:
        dic: An dictionary containing the result of the operation.
    """
    
    try:
        print("="*50)
        print("Adding transaction:", data_transaction)
        print("="*50)
        return {
            "status": "success",
            "message": "Transaction added successfully.",
            "transaction_id": "12345",  # This would be generated by the database in a real scenario
        }
    except Exception as e:
        print("Error adding transaction:", e)
        return {
            "status": "error",
            "message": str(e),
        }