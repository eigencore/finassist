from finassist.utils.database import get_user_context_info

def main():
    user_id = "user_001"  # Replace with the actual user ID you want to query
    try:
        user_info = get_user_context_info(user_id)
        print("User Context Information:")
        print(user_info.replace("{", "{{").replace("}", "}}"))  # Format for better readability
    except Exception as e:
        print(f"An error occurred: {e}")
        

if __name__ == "__main__":
    main()