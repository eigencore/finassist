# FinAssist Database Documentation

This is the documentation for the FinAssist database schema, which is designed to support an autonomous multi-agent financial auditor. The schema is structured to handle user accounts, financial transactions, budgeting, income tracking, financial goals, and advanced financial analysis.

## Overview

This document provides detailed documentation for the FinAssist database schema, a comprehensive financial management system designed to support an autonomous multi-agent financial auditor. The database is structured to handle user accounts, financial transactions, budgeting, income tracking, financial goals, and advanced financial analysis.

## Table Specifications

## User Management

### `users`

Primary table for storing user account information.

| Column | Type | Description |
|--------|------|-------------|
| `user_id` | PRIMARY KEY | Unique identifier for each user |
| `email` | VARCHAR | User's email address, used for login |
| `name` | VARCHAR | User's full name |
| `password` | VARCHAR | Hashed password |
| `phone_number` | VARCHAR | User's phone number |
| `preferred_currency` | VARCHAR | Default currency for the user |
| `created_at` | TIMESTAMP | Account creation timestamp |
| `updated_at` | TIMESTAMP | Last account update timestamp |
| `timezone` | VARCHAR | User's timezone |
| `language_preference` | VARCHAR | User's preferred language |
| `mfa_enabled` | BOOLEAN | Whether multi-factor authentication is enabled |
| `mfa_type` | VARCHAR | Type of MFA (app, sms, email) |

**Usage**: Core user identification and authentication. Referenced by most other tables to associate data with specific users.

### `user_preferences` (Pending)

Stores user-specific settings and preferences.

| Column | Type | Description |
|--------|------|-------------|
| `preference_id` | PRIMARY KEY | Unique identifier for each preference |
| `user_id` | FOREIGN KEY | Reference to users.user_id |
| `category` | VARCHAR | Preference category (notifications, privacy, display, analytics) |
| `key` | VARCHAR | Specific preference identifier |
| `value` | VARCHAR/JSON | Preference value |
| `updated_at` | TIMESTAMP | Last update timestamp |

**Usage**: Enables customization of the user experience and application behavior.

## Accounts Management

### `accounts`

Tracks different financial accounts owned by users.

| Column | Type | Description |
|--------|------|-------------|
| `account_id` | PRIMARY KEY | Unique identifier for each account |
| `user_id` | FOREIGN KEY | Reference to users.user_id |
| `name` | VARCHAR | Account name (e.g., "Main Checking", "Savings") |
| `type` | VARCHAR | Account type (checking, savings, credit card, investment, etc.) |
| `institution` | VARCHAR | Financial institution name |
| `balance` | DECIMAL | Current account balance |
| `currency` | VARCHAR | Account currency |
| `last_updated` | TIMESTAMP | Last balance update timestamp |
| `account_number_masked` | VARCHAR | Masked account number for reference |
| `active` | BOOLEAN | Whether the account is active |
| `notes` | TEXT | Additional account notes |

**Usage**: Serves as the source and destination for transactions, allowing users to track balances across multiple accounts.

## Transaction Management

### `transactions`

Central table for recording all financial transactions.

| Column | Type | Description |
|--------|------|-------------|
| `transaction_id` | PRIMARY KEY | Unique identifier for each transaction |
| `user_id` | FOREIGN KEY | Reference to users.user_id |
| `account_id` | FOREIGN KEY | Reference to accounts.account_id |
| `amount` | DECIMAL | Transaction amount |
| `currency` | VARCHAR | Transaction currency |
| `category_id` | FOREIGN KEY | Reference to categories.category_id |
| `subcategory_id` | FOREIGN KEY | Reference to subcategories.subcategory_id |
| `establishment` | VARCHAR | Place where transaction occurred |
| `transaction_date` | DATE | Date the transaction took place |
| `recorded_date` | TIMESTAMP | Date when transaction was recorded in system |
| `transaction_type` | VARCHAR | Type of transaction (expense, income, transfer) |
| `payment_method` | VARCHAR | Method used (cash, credit card, etc.) |
| `is_recurring` | BOOLEAN | Whether this is a recurring transaction |
| `recurrence_period` | VARCHAR | Frequency (daily, weekly, monthly, yearly) |
| `parent_transaction_id` | FOREIGN KEY | For recurring transactions, reference to original transaction |
| `notes` | TEXT | Additional transaction details |
| `source` | VARCHAR | How transaction was entered (manual, imported) |
| `attachment_url` | VARCHAR | URL to receipt or documentation |
| `geo_location` | VARCHAR/JSON | Transaction location coordinates |
| `tags` | JSON | Array of tags or categories |
| `verification_status` | VARCHAR | Transaction verification status (verified, pending, disputed) |

**Usage**: Core table for expense and income tracking, financial analysis, and budget monitoring.

### `categories`

Categorizes transactions for organization and analysis.

| Column | Type | Description |
|--------|------|-------------|
| `category_id` | PRIMARY KEY | Unique identifier for each category |
| `user_id` | FOREIGN KEY | Reference to users.user_id (NULL for system defaults) |
| `name` | VARCHAR | Category name (e.g., "Food", "Transportation") |
| `system_default` | BOOLEAN | Whether this is a system-defined category |
| `icon_reference` | VARCHAR | Reference to category icon for UI |
| `description` | TEXT | Category description |

**Usage**: Enables transaction organization and categorization for analysis and budgeting.

CREATE TABLE categories (
  category_id STRING PRIMARY KEY,
  user_id STRING NOT NULL,
  name STRING,
  icon_reference STRING,
  system_default BOOLEAN,
  description TEXT,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP
);

### `subcategories`

Further categorizes transactions within main categories.

| Column | Type | Description |
|--------|------|-------------|
| `subcategory_id` | PRIMARY KEY | Unique identifier for each subcategory |
| `category_id` | FOREIGN KEY | Reference to categories.category_id |
| `name` | VARCHAR | Subcategory name (e.g., "Restaurants", "Groceries") |
| `system_default` | BOOLEAN | Whether this is a system-defined subcategory |
| `description` | TEXT | Subcategory description |

**Usage**: Provides more granular transaction categorization.

## Budget Management

### `budgets`

Defines spending limits for categories over specific time periods.

| Column | Type | Description |
|--------|------|-------------|
| `budget_id` | PRIMARY KEY | Unique identifier for each budget |
| `user_id` | FOREIGN KEY | Reference to users.user_id |
| `category_id` | FOREIGN KEY | Reference to categories.category_id |
| `subcategory_id` | FOREIGN KEY | Reference to subcategories.subcategory_id (can be NULL) |
| `amount` | DECIMAL | Budget amount |
| `currency` | VARCHAR | Budget currency |
| `period_type` | VARCHAR | Budget period (monthly, weekly, annual) |
| `start_date` | DATE | Budget start date |
| `end_date` | DATE | Budget end date (optional) |
| `is_recurring` | BOOLEAN | Whether budget recurs automatically |
| `active` | BOOLEAN | Whether budget is currently active |

**Usage**: Allows users to set and track spending limits for different categories.

## Income Management

### `income`

Tracks income transactions separately for clearer financial management.

| Column | Type | Description |
|--------|------|-------------|
| `income_id` | PRIMARY KEY | Unique identifier for each income record |
| `user_id` | FOREIGN KEY | Reference to users.user_id |
| `account_id` | FOREIGN KEY | Reference to accounts.account_id |
| `amount` | DECIMAL | Income amount |
| `currency` | VARCHAR | Income currency |
| `income_type` | VARCHAR | Type of income (salary, investment, freelance, gift, etc.) |
| `income_date` | DATE | Date income was received |
| `recorded_date` | TIMESTAMP | Date income was recorded in system |
| `is_recurring` | BOOLEAN | Whether this is recurring income |
| `recurrence_period` | VARCHAR | Frequency (daily, weekly, monthly, yearly) |
| `parent_income_id` | FOREIGN KEY | For recurring income, reference to original record |
| `notes` | TEXT | Additional income details |
| `source` | VARCHAR | How income was entered (manual, imported) |
| `attachment_url` | VARCHAR | URL to documentation |
| `verification_status` | VARCHAR | Income verification status |

**Usage**: Provides a dedicated table for income tracking, separate from expenses.

## Financial Goals

### `financial_goals`

Tracks user's financial objectives and progress.

| Column | Type | Description |
|--------|------|-------------|
| `goal_id` | PRIMARY KEY | Unique identifier for each goal |
| `user_id` | FOREIGN KEY | Reference to users.user_id |
| `name` | VARCHAR | Goal name |
| `description` | TEXT | Detailed goal description |
| `target_amount` | DECIMAL | Target amount to reach |
| `current_amount` | DECIMAL | Current progress amount |
| `start_date` | DATE | Goal start date |
| `target_date` | DATE | Goal target completion date |
| `status` | VARCHAR | Goal status (in progress, completed, on hold) |
| `priority` | VARCHAR | Goal priority (high, medium, low) |
| `linked_account_id` | FOREIGN KEY | Optional reference to accounts.account_id for tracking |
| `savings_plan_id` | FOREIGN KEY | Reference to savings_plans.plan_id |
| `progress_percentage` | DECIMAL | Percentage of goal completed for easier tracking |
| `monthly_contribution_target` | DECIMAL | Required monthly savings to reach goal |

**Usage**: Enables users to set and track progress towards financial goals.

### `savings_plans`

Detailed plans for achieving financial goals through systematic saving.

| Column | Type | Description |
|--------|------|-------------|
| `plan_id` | PRIMARY KEY | Unique identifier for each savings plan |
| `goal_id` | FOREIGN KEY | Reference to financial_goals.goal_id |
| `user_id` | FOREIGN KEY | Reference to users.user_id |
| `monthly_amount` | DECIMAL | Amount to save each month |
| `auto_transfer_enabled` | BOOLEAN | Whether automatic transfers are enabled |
| `linked_savings_account_id` | FOREIGN KEY | Reference to accounts.account_id where savings are deposited |
| `alert_threshold_percentage` | DECIMAL | Threshold for triggering alerts when falling behind |
| `start_date` | DATE | When the savings plan begins |
| `current_streak` | INTEGER | Days/months of consistent contributions |
| `adjustment_history` | JSON | History of adjustments made to the plan |

**Usage**: Provides structure and automation for goal-based savings strategies, allowing the system to track, monitor, and adjust savings plans to keep users on target for their financial goals.

## Analysis & Insights

### `financial_insights`

Stores generated financial insights and recommendations.

| Column | Type | Description |
|--------|------|-------------|
| `insight_id` | PRIMARY KEY | Unique identifier for each insight |
| `user_id` | FOREIGN KEY | Reference to users.user_id |
| `type` | VARCHAR | Insight type (spending pattern, budget alert, saving opportunity) |
| `description` | TEXT | Detailed insight description |
| `severity` | VARCHAR | Importance level (information, warning, critical) |
| `created_at` | TIMESTAMP | Insight generation timestamp |
| `expired_at` | TIMESTAMP | Insight expiration date |
| `read_status` | BOOLEAN | Whether the insight has been viewed |
| `related_categories` | JSON | Categories related to this insight |
| `action_taken` | BOOLEAN | Whether user has acted on this insight |

**Usage**: Stores AI-generated insights and recommendations, enabling proactive financial advice.

## Simulations

### `simulation_scenarios`

Stores financial simulation scenarios for "what-if" analysis.

| Column | Type | Description |
|--------|------|-------------|
| `scenario_id` | PRIMARY KEY | Unique identifier for each scenario |
| `user_id` | FOREIGN KEY | Reference to users.user_id |
| `name` | VARCHAR | Scenario name |
| `description` | TEXT | Scenario description |
| `creation_date` | TIMESTAMP | Scenario creation date |
| `parameters` | JSON | Simulation parameters |
| `results` | JSON | Simulation results |
| `is_favorite` | BOOLEAN | Whether user has marked as favorite |
| `last_modified` | TIMESTAMP | Last modification date |

**Usage**: Enables users to simulate different financial scenarios and their outcomes.

## Reporting

### `saved_reports`

Stores user-saved custom financial reports.

| Column | Type | Description |
|--------|------|-------------|
| `report_id` | PRIMARY KEY | Unique identifier for each report |
| `user_id` | FOREIGN KEY | Reference to users.user_id |
| `name` | VARCHAR | Report name |
| `type` | VARCHAR | Report type (spending_summary, budget_performance, tax_report) |
| `parameters` | JSON | Report generation parameters |
| `created_at` | TIMESTAMP | Report creation date |
| `last_generated` | TIMESTAMP | Last report generation date |
| `is_scheduled` | BOOLEAN | Whether report generation is scheduled |
| `schedule_frequency` | VARCHAR | How often report is generated |
| `delivery_method` | VARCHAR | How report is delivered (in-app, email) |

**Usage**: Allows users to save and schedule custom financial reports.

## Utility Tables

### `currency_conversions`

Tracks currency exchange rates for multi-currency support.

| Column | Type | Description |
|--------|------|-------------|
| `conversion_id` | PRIMARY KEY | Unique identifier for each conversion rate |
| `from_currency` | VARCHAR | Source currency code |
| `to_currency` | VARCHAR | Target currency code |
| `conversion_rate` | DECIMAL | Exchange rate |
| `effective_date` | DATE | Date rate is effective |
| `source` | VARCHAR | Rate source (API provider) |

**Usage**: Enables multi-currency support and historical exchange rate tracking.

### `tags`

Stores custom tags for flexible transaction categorization.

| Column | Type | Description |
|--------|------|-------------|
| `tag_id` | PRIMARY KEY | Unique identifier for each tag |
| `user_id` | FOREIGN KEY | Reference to users.user_id |
| `name` | VARCHAR | Tag name |
| `color` | VARCHAR | Tag color for UI |

**Usage**: Provides flexible categorization beyond the fixed category/subcategory hierarchy.

### `transaction_tags`

Junction table linking transactions to tags.

| Column | Type | Description |
|--------|------|-------------|
| `transaction_id` | FOREIGN KEY | Reference to transactions.transaction_id |
| `tag_id` | FOREIGN KEY | Reference to tags.tag_id |

**Usage**: Establishes many-to-many relationship between transactions and tags.

## Recommendations for Recurring Transactions

For handling recurring transactions, consider implementing the following:

1. A scheduled job that runs daily to check for and generate recurring transactions
2. A dedicated table for recurring templates to better handle complex recurrence patterns
3. Status flags to indicate which transactions were auto-generated and which need verification

## Database Relationships

- One user can have multiple accounts, transactions, budgets, goals, etc.
- Transactions are associated with categories and optionally subcategories
- Transactions can be linked to multiple tags through the transaction_tags junction table
- Recurring transactions reference their parent transaction
- Budgets are associated with categories and optionally subcategories

## Schema Evolution Considerations

As the FinAssist application evolves, consider:

- Adding support for shared accounts between multiple users
- Implementing more sophisticated recurrence rules for transactions
- Expanding the insight generation capabilities with more detailed metadata
- Adding support for tax categories and tax reporting
- Creating transaction rules for automatic categorization
- Implementing notification preferences and event tracking
- Developing integration points with external financial institutions
- Building reward mechanisms for achieving financial goals and maintaining healthy habits