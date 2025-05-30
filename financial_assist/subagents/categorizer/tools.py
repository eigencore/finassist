import os
import uuid
from datetime import datetime
from google.adk.models.lite_llm import LiteLlm, LlmRequest

from financial_assist.subagents.bigquery.tools import get_bq_client
from financial_assist.utils.utils import get_env_var


async def get_create_category_sql_query(
    user_id: str,
    name: str,
    description: str,
    icon_reference: str,
) -> str:
    prompt_template = """
You are a BigQuery SQL expert that generates SQL to insert new categories into a BigQuery database.

This is the database schema:
CREATE TABLE `BQ_PROJECT_ID.BQ_DATASET_ID.categories` (
  category_id STRING NOT NULL,
  user_id STRING NOT NULL,
  name STRING NOT NULL,
  icon_reference STRING,
  system_default BOOLEAN NOT NULL,
  description STRING NOT NULL,
  is_active BOOLEAN NOT NULL,
  created_at TIMESTAMP NOT NULL
);

Given the following information, generate a SQL INSERT statement to add a new category:
- category_id: GENERATE_UUID()
- user_id: {USER_ID}
- name: {NAME}
- description: {DESCRIPTION}
- icon_reference: {ICON_REFERENCE}
- system_default: true
- is_active: true
- created_at: CURRENT_TIMESTAMP()

Example SQL:
```sql
INSERT INTO `BQ_PROJECT_ID.BQ_DATASET_ID.categories`
(category_id, user_id, name, icon_reference, system_default, description, is_active, created_at)
VALUES
('cat_001', 'user_001', 'Food & Dining', '🍽️', false, 'Restaurant and food expenses', true, CURRENT_TIMESTAMP());
```
   """

    llm_model = LiteLlm(
        model=os.getenv("BASELINE_NL2SQL_MODEL"),
    )

    prompt = prompt_template.format(
        USER_ID=user_id,
        NAME=name,
        DESCRIPTION=description,
        ICON_REFERENCE=icon_reference,
    )

    # ✅ Crear LlmRequest con estructura completa
    from google.genai import types

    llm_request = LlmRequest(
        contents=[
            types.Content(
                parts=[types.Part.from_text(text=prompt)],
                role="user"
            )
        ],
        config=types.GenerateContentConfig(
            max_output_tokens=512,
            temperature=0.1,
            tools=[]
        )
    )

    response_generator = llm_model.generate_content_async(llm_request, stream=False)

    response = None
    async for llm_response in response_generator:
        response = llm_response
        break
    sql = response.content.parts[0].text if response and response.content.parts[0].text else ""
    if sql:
        sql = sql.replace("```sql", "").replace("```", "").strip()

    return sql

async def get_create_subcategory_sql_query(
    category_id: str,
    name: str,
    description: str
) -> str:
    prompt_template = """
You are a BigQuery SQL expert that generates SQL to insert new categories into a BigQuery database.

This is the database schema:
CREATE TABLE `BQ_PROJECT_ID.BQ_DATASET_ID.subcategories` (
 subcategory_id STRING NOT NULL,
 category_id STRING NOT NULL,
 name STRING NOT NULL,
 description STRING NOT NULL,
 is_active BOOLEAN NOT NULL,
 created_at TIMESTAMP NOT NULL
);

Given the following information, generate a SQL INSERT statement to add a new category:
- subcategory_id: GENERATE_UUID()
- category_id: {CATEGORY_ID}
- name: {NAME}
- description: {DESCRIPTION}
- is_active: true
- created_at: CURRENT_TIMESTAMP()

Example SQL:
```sql
INSERT INTO `BQ_PROJECT_ID.BQ_DATASET_ID.subcategories`
(subcategory_id, category_id, name, description, is_active, created_at)
VALUES
('subcat_001', 'cateogory_001', 'Coffee Shops', 'Coffee shops and cafes', true, CURRENT_TIMESTAMP());
```
   """

    llm_model = LiteLlm(
        model=os.getenv("BASELINE_NL2SQL_MODEL"),
    )

    prompt = prompt_template.format(
        CATEGORY_ID=category_id,
        NAME=name,
        DESCRIPTION=description,
    )

    # ✅ Crear LlmRequest con estructura completa
    from google.genai import types

    llm_request = LlmRequest(
        contents=[
            types.Content(
                parts=[types.Part.from_text(text=prompt)],
                role="user"
            )
        ],
        config=types.GenerateContentConfig(
            max_output_tokens=512,
            temperature=0.1,
            tools=[]
        )
    )

    response_generator = llm_model.generate_content_async(llm_request, stream=False)

    response = None
    async for llm_response in response_generator:
        response = llm_response
        break
    sql = response.content.parts[0].text if response and response.content.parts[0].text else ""
    if sql:
        sql = sql.replace("```sql", "").replace("```", "").strip()

    print("\n Generated SQL:", sql)
    return sql

async def create_category(
    user_id: str,
    name: str,
    description: str,
    icon_reference: str,
) -> str:
    
    client = get_bq_client()
    
    if not client:
        raise ValueError("BigQuery client is not available.")
    
    sql_query = await get_create_category_sql_query(
            user_id=user_id,
            name=name,
            description=description,
            icon_reference=icon_reference,
        )
    
    
    
    # Preprocess query
    sql_query = sql_query.replace("GENERATE_UUID()", f"'{str(uuid.uuid4())}'")
    sql_query = sql_query.replace("BQ_PROJECT_ID", get_env_var("BQ_PROJECT_ID"))
    sql_query = sql_query.replace("BQ_DATASET_ID", get_env_var("BQ_DATASET_ID"))
    sql_query = sql_query.replace("CURRENT_TIMESTAMP()", f"'{datetime.datetime.now().isoformat()}'")

    
    print("======================")
    print(f"Executing query: {sql_query}")
    print("======================")
    
    # Execute the query
    try:
        query_job = client.query(sql_query)
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
    
async def create_subcategory(
    category_id: str,
    name: str,
    description: str,
) -> str:
    
    client = get_bq_client()
    
    if not client:
        raise ValueError("BigQuery client is not available.")
    
    sql_query = await get_create_subcategory_sql_query(
            category_id=category_id,
            name=name,
            description=description,
        )
    
    # Preprocess query
    sql_query = sql_query.replace("GENERATE_UUID()", f"'{str(uuid.uuid4())}'")
    sql_query = sql_query.replace("BQ_PROJECT_ID", get_env_var("BQ_PROJECT_ID"))
    sql_query = sql_query.replace("BQ_DATASET_ID", get_env_var("BQ_DATASET_ID"))
    sql_query = sql_query.replace("CURRENT_TIMESTAMP()", f"'{datetime.datetime.now().isoformat()}'")
    
    print("======================")
    print(f"Executing query: {sql_query}")
    print("======================")
    
    # Execute the query
    try:
        query_job = client.query(sql_query)
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



# query = """
#   CREATE TABLE `ninth-botany-460322-r5.finassist_db.categories` (
#   category_id STRING NOT NULL,
#   user_id STRING NOT NULL,
#   name STRING NOT NULL,
#   icon_reference STRING,
#   system_default BOOLEAN NOT NULL,
#   description STRING NOT NULL,
#   is_active BOOLEAN NOT NULL,
#   created_at TIMESTAMP NOT NULL
# );





# INSERT INTO `ninth-botany-460322-r5.finassist_db.categories` 
# (category_id, user_id, name, icon_reference, system_default, description, is_active, created_at)
# VALUES 
# ('cat_001', 'user_001', 'Food & Dining', '🍽️', false, 'Restaurant and food expenses', true, CURRENT_TIMESTAMP()),
# ('cat_002', 'user_001', 'Transportation', '🚗', false, 'Travel and commuting costs', true, CURRENT_TIMESTAMP()),
# ('cat_003', 'user_001', 'Entertainment', '🎬', false, 'Movies, streaming, games', true, CURRENT_TIMESTAMP()),
# ('cat_004', 'user_001', 'Shopping', '🛍️', false, 'General purchases and retail', true, CURRENT_TIMESTAMP()),
# ('cat_005', 'user_001', 'Utilities', '💡', false, 'Home utilities and services', true, CURRENT_TIMESTAMP()),
# ('cat_006', 'user_001', 'Health & Fitness', '💪', false, 'Healthcare and fitness expenses', true, CURRENT_TIMESTAMP()),
# ('cat_007', 'user_001', 'Education', '📚', false, 'Learning and educational expenses', true, CURRENT_TIMESTAMP()),
# ('cat_008', 'user_001', 'Personal Care', '💄', false, 'Beauty and personal care', true, CURRENT_TIMESTAMP()),
# ('cat_009', 'user_001', 'Income', '💰', false, 'All sources of income', true, CURRENT_TIMESTAMP()),
# ('cat_010', 'user_001', 'Other', '📋', false, 'Miscellaneous expenses', true, CURRENT_TIMESTAMP());


# INSERT INTO `ninth-botany-460322-r5.finassist_db.subcategories`
# (subcategory_id, category_id, name, description, is_active, created_at)
# VALUES 
# -- Food & Dining (cat_001)
# ('sub_001', 'cat_001', 'Restaurants', 'Dining out and takeout orders', true, CURRENT_TIMESTAMP()),
# ('sub_002', 'cat_001', 'Groceries', 'Supermarket and grocery shopping', true, CURRENT_TIMESTAMP()),
# ('sub_003', 'cat_001', 'Coffee Shops', 'Coffee shops and cafes', true, CURRENT_TIMESTAMP()),
# ('sub_004', 'cat_001', 'Fast Food', 'Quick service restaurants', true, CURRENT_TIMESTAMP()),
# ('sub_005', 'cat_001', 'Food Delivery', 'Delivery services like UberEats', true, CURRENT_TIMESTAMP()),

# -- Transportation (cat_002)
# ('sub_006', 'cat_002', 'Gas', 'Vehicle fuel and gas stations', true, CURRENT_TIMESTAMP()),
# ('sub_007', 'cat_002', 'Public Transport', 'Bus, metro, and train tickets', true, CURRENT_TIMESTAMP()),
# ('sub_008', 'cat_002', 'Rideshare', 'Uber, Lyft, and taxi services', true, CURRENT_TIMESTAMP()),
# ('sub_009', 'cat_002', 'Parking', 'Parking fees and meters', true, CURRENT_TIMESTAMP()),
# ('sub_010', 'cat_002', 'Car Maintenance', 'Vehicle repairs and maintenance', true, CURRENT_TIMESTAMP()),

# -- Entertainment (cat_003)
# ('sub_011', 'cat_003', 'Streaming', 'Netflix, Spotify, streaming services', true, CURRENT_TIMESTAMP()),
# ('sub_012', 'cat_003', 'Movies', 'Cinema tickets and movie rentals', true, CURRENT_TIMESTAMP()),
# ('sub_013', 'cat_003', 'Games', 'Video games and gaming apps', true, CURRENT_TIMESTAMP()),
# ('sub_014', 'cat_003', 'Books', 'Books and e-books', true, CURRENT_TIMESTAMP()),
# ('sub_015', 'cat_003', 'Concerts', 'Live music and events', true, CURRENT_TIMESTAMP()),

# -- Shopping (cat_004)
# ('sub_016', 'cat_004', 'Clothing', 'Clothes and accessories', true, CURRENT_TIMESTAMP()),
# ('sub_017', 'cat_004', 'Electronics', 'Tech gadgets and electronics', true, CURRENT_TIMESTAMP()),
# ('sub_018', 'cat_004', 'Home & Garden', 'Home improvement and gardening', true, CURRENT_TIMESTAMP()),
# ('sub_019', 'cat_004', 'Gifts', 'Presents and gift purchases', true, CURRENT_TIMESTAMP()),
# ('sub_020', 'cat_004', 'Online Shopping', 'Amazon and other online purchases', true, CURRENT_TIMESTAMP()),

# -- Utilities (cat_005)
# ('sub_021', 'cat_005', 'Electricity', 'Electric utility bills', true, CURRENT_TIMESTAMP()),
# ('sub_022', 'cat_005', 'Internet', 'Internet service provider', true, CURRENT_TIMESTAMP()),
# ('sub_023', 'cat_005', 'Phone', 'Mobile phone bills', true, CURRENT_TIMESTAMP()),
# ('sub_024', 'cat_005', 'Water', 'Water utility bills', true, CURRENT_TIMESTAMP()),
# ('sub_025', 'cat_005', 'Gas Bill', 'Natural gas utility bills', true, CURRENT_TIMESTAMP()),

# -- Health & Fitness (cat_006)
# ('sub_026', 'cat_006', 'Gym', 'Gym memberships and fitness', true, CURRENT_TIMESTAMP()),
# ('sub_027', 'cat_006', 'Medical', 'Doctor visits and medical expenses', true, CURRENT_TIMESTAMP()),
# ('sub_028', 'cat_006', 'Pharmacy', 'Medications and pharmacy', true, CURRENT_TIMESTAMP()),
# ('sub_029', 'cat_006', 'Dental', 'Dental care and treatments', true, CURRENT_TIMESTAMP()),
# ('sub_030', 'cat_006', 'Supplements', 'Vitamins and health supplements', true, CURRENT_TIMESTAMP()),

# -- Education (cat_007)
# ('sub_031', 'cat_007', 'Courses', 'Online courses and certifications', true, CURRENT_TIMESTAMP()),
# ('sub_032', 'cat_007', 'Books & Materials', 'Educational books and materials', true, CURRENT_TIMESTAMP()),
# ('sub_033', 'cat_007', 'Tuition', 'School and university tuition', true, CURRENT_TIMESTAMP()),
# ('sub_034', 'cat_007', 'Workshops', 'Professional workshops and seminars', true, CURRENT_TIMESTAMP()),

# -- Personal Care (cat_008)
# ('sub_035', 'cat_008', 'Haircut', 'Hair salon and barber services', true, CURRENT_TIMESTAMP()),
# ('sub_036', 'cat_008', 'Skincare', 'Skincare products and treatments', true, CURRENT_TIMESTAMP()),
# ('sub_037', 'cat_008', 'Cosmetics', 'Makeup and beauty products', true, CURRENT_TIMESTAMP()),
# ('sub_038', 'cat_008', 'Spa', 'Spa treatments and wellness', true, CURRENT_TIMESTAMP()),

# -- Income (cat_009)
# ('sub_039', 'cat_009', 'Salary', 'Monthly salary payments', true, CURRENT_TIMESTAMP()),
# ('sub_040', 'cat_009', 'Freelance', 'Freelance project payments', true, CURRENT_TIMESTAMP()),
# ('sub_041', 'cat_009', 'Investments', 'Investment returns and dividends', true, CURRENT_TIMESTAMP()),
# ('sub_042', 'cat_009', 'Side Hustle', 'Additional income sources', true, CURRENT_TIMESTAMP()),

# -- Other (cat_010)
# ('sub_043', 'cat_010', 'Donations', 'Charitable donations', true, CURRENT_TIMESTAMP()),
# ('sub_044', 'cat_010', 'Fees', 'Bank fees and service charges', true, CURRENT_TIMESTAMP()),
# ('sub_045', 'cat_010', 'Miscellaneous', 'Uncategorized expenses', true, CURRENT_TIMESTAMP());
# """