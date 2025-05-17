# Esquema Detallado de Base de Datos (Continuación)

## Definición Detallada de Tablas (Continuación)

### 5. Tabla: `budgets` (continuación)

| Campo | Tipo | Descripción | Notas |
|-------|------|-------------|-------|
| `budget_id` | STRING | Identificador único del presupuesto | PRIMARY KEY |
| `user_id` | STRING | ID del usuario propietario | FOREIGN KEY |
| `category_id` | STRING | ID de la categoría (opcional) | FOREIGN KEY |
| `subcategory_id` | STRING | ID de la subcategoría (opcional) | FOREIGN KEY |
| `amount` | NUMERIC | Monto presupuestado | NOT NULL |
| `currency` | STRING | Moneda del presupuesto | NOT NULL |
| `period_type` | STRING | Tipo de período: mensual, semanal, anual | DEFAULT 'monthly' |
| `start_date` | DATE | Fecha de inicio del presupuesto | |
| `is_recurring` | BOOL | Indica si el presupuesto se repite | DEFAULT TRUE |
| `active` | BOOL | Indica si el presupuesto está activo | DEFAULT TRUE |

**Índices adicionales:**
- Índice compuesto en `(user_id, category_id, period_type)` para consultas de análisis

**Notas de implementación:**
- Un presupuesto puede referirse a una categoría principal (ej. "Alimentación") o a una subcategoría específica (ej. "Restaurantes")
- Si se especifica solo `category_id`, el presupuesto aplica a toda la categoría
- Si se especifican ambos, el presupuesto aplica solo a esa subcategoría específica

### 6. Tabla: `financial_goals`

Almacena objetivos financieros definidos por los usuarios.

| Campo | Tipo | Descripción | Notas |
|-------|------|-------------|-------|
| `goal_id` | STRING | Identificador único del objetivo | PRIMARY KEY |
| `user_id` | STRING | ID del usuario propietario | FOREIGN KEY |
| `name` | STRING | Nombre del objetivo financiero | NOT NULL |
| `description` | STRING | Descripción detallada | |
| `target_amount` | NUMERIC | Monto objetivo a alcanzar | NOT NULL |
| `currency` | STRING | Moneda del objetivo | NOT NULL |
| `current_amount` | NUMERIC | Monto actual acumulado | DEFAULT 0 |
| `start_date` | DATE | Fecha de inicio | DEFAULT CURRENT_DATE() |
| `target_date` | DATE | Fecha objetivo para completar | |
| `status` | STRING | Estado: en_progreso, completado, abandonado | DEFAULT 'in_progress' |
| `priority` | STRING | Prioridad: alta, media, baja | DEFAULT 'medium' |

**Índices adicionales:**
- Índice en `(user_id, status)` para filtrado rápido

**Notas de implementación:**
- Considerar agregar un campo para categorizar objetivos (ahorro, inversión, deuda, etc.)
- Implementar lógica para actualización automática del progreso basada en transacciones etiquetadas

### 7. Tabla: `transaction_tags` (Opcional)

Permite etiquetar transacciones para análisis personalizados.

| Campo | Tipo | Descripción | Notas |
|-------|------|-------------|-------|
| `tag_id` | STRING | Identificador único de la etiqueta | PRIMARY KEY |
| `transaction_id` | STRING | ID de la transacción | FOREIGN KEY |
| `tag_name` | STRING | Nombre de la etiqueta | NOT NULL |
| `created_at` | TIMESTAMP | Fecha de creación | DEFAULT CURRENT_TIMESTAMP() |

**Índices adicionales:**
- Índice en `transaction_id` para búsquedas rápidas
- Índice en `tag_name` para agrupación

**Notas de implementación:**
- Permite análisis multidimensional más allá de categorías predefinidas
- Útil para situaciones como "vacaciones", "proyecto especial", que atraviesan categorías

### 8. Vista: `monthly_spending_summary`

Vista materializada para análisis rápido de gastos mensuales.

```sql
CREATE OR REPLACE VIEW `finassist.monthly_spending_summary` AS
SELECT
  user_id,
  FORMAT_DATE('%Y-%m', transaction_date) AS month,
  category_id,
  c.name AS category_name,
  SUM(amount) AS total_amount,
  COUNT(*) AS transaction_count
FROM
  `finassist.transactions` t
JOIN
  `finassist.categories` c ON t.category_id = c.category_id
WHERE
  transaction_type = 'expense'
GROUP BY
  user_id, month, category_id, category_name
```

**Notas de implementación:**
- Considerar convertir en tabla materializada con actualización programada para mejor rendimiento
- Útil para paneles de control y análisis frecuentes

## Relaciones entre Tablas

```
users 1──────────N transactions
                    │
                    │
categories 1────────┘
      │
      │
      1
      │
      │
subcategories 1─────┘


users 1──────────N budgets
                   │
                   │
categories 1───────┤
      │            │
      │            │
      1            │
      │            │
      │            │
subcategories 1────┘


users 1──────────N financial_goals
```

## Optimizaciones para BigQuery

### Particionamiento

- **transactions**: Particionar por `transaction_date` para optimizar consultas basadas en rangos de fecha
  ```sql
  CREATE TABLE `finassist.transactions`
  (
    -- campos definidos anteriormente
  )
  PARTITION BY transaction_date
  CLUSTER BY user_id, category_id;
  ```

- **budgets**: Considerar particionamiento por `start_date` si se espera un gran volumen

### Clustering

- **transactions**: Clusterizar por `user_id` y `category_id` para mejorar consultas filtradas
- **budgets**: Clusterizar por `user_id` y `category_id`

### Vistas Materializadas

Considerar las siguientes vistas materializadas para análisis frecuentes:

1. **monthly_category_spending**:
   ```sql
   CREATE MATERIALIZED VIEW `finassist.monthly_category_spending` AS
   SELECT
     user_id,
     FORMAT_DATE('%Y-%m', transaction_date) AS month,
     category_id,
     SUM(amount) AS total_amount
   FROM
     `finassist.transactions`
   WHERE
     transaction_type = 'expense'
   GROUP BY
     user_id, month, category_id
   ```

2. **budget_vs_actual**:
   ```sql
   CREATE MATERIALIZED VIEW `finassist.budget_vs_actual` AS
   SELECT
     b.user_id,
     b.category_id,
     b.amount AS budget_amount,
     COALESCE(SUM(t.amount), 0) AS actual_amount,
     (COALESCE(SUM(t.amount), 0) / b.amount) * 100 AS percentage_used
   FROM
     `finassist.budgets` b
   LEFT JOIN
     `finassist.transactions` t
     ON b.user_id = t.user_id
     AND b.category_id = t.category_id
     AND t.transaction_date BETWEEN b.start_date 
       AND DATE_ADD(b.start_date, INTERVAL 1 MONTH)
     AND t.transaction_type = 'expense'
   WHERE
     b.active = TRUE
     AND b.period_type = 'monthly'
   GROUP BY
     b.user_id, b.category_id, b.amount
   ```

## Consideraciones de Escalabilidad

1. **Particionamiento efectivo**:
   - Particionar tablas grandes por fecha
   - Considerar particionamiento adicional para usuarios muy activos

2. **Monitoreo de rendimiento**:
   - Implementar seguimiento de consultas más costosas
   - Optimizar paulatinamente basado en patrones de uso

3. **Estrategia de datos históricos**:
   - Considerar tabla separada para transacciones históricas (> 1 año)
   - Implementar políticas de retención y agregación para datos antiguos

4. **Optimización de costo**:
   - Monitorear uso de BigQuery para identificar optimizaciones
   - Considerar caché en memoria para datos frecuentemente accedidos

## DDL Inicial

Script SQL para crear el esquema inicial:

```sql
-- Crear dataset
CREATE SCHEMA IF NOT EXISTS `finassist`;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS `finassist.users` (
  user_id STRING NOT NULL,
  email STRING,
  name STRING,
  preferred_currency STRING DEFAULT 'USD',
  budget_period STRING DEFAULT 'monthly',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  timezone STRING DEFAULT 'UTC',
  language_preference STRING DEFAULT 'en',
  notification_settings JSON,
  PRIMARY KEY(user_id)
);

-- Tabla de categorías
CREATE TABLE IF NOT EXISTS `finassist.categories` (
  category_id STRING NOT NULL,
  name STRING NOT NULL,
  system_default BOOL DEFAULT TRUE,
  icon_reference STRING,
  description STRING,
  PRIMARY KEY(category_id)
);

-- Tabla de subcategorías
CREATE TABLE IF NOT EXISTS `finassist.subcategories` (
  subcategory_id STRING NOT NULL,
  category_id STRING NOT NULL,
  name STRING NOT NULL,
  system_default BOOL DEFAULT TRUE,
  description STRING,
  PRIMARY KEY(subcategory_id),
  FOREIGN KEY(category_id) REFERENCES `finassist.categories`(category_id)
);

-- Tabla de transacciones
CREATE TABLE IF NOT EXISTS `finassist.transactions` (
  transaction_id STRING NOT NULL,
  user_id STRING NOT NULL,
  amount NUMERIC NOT NULL,
  currency STRING NOT NULL,
  category_id STRING,
  subcategory_id STRING,
  establishment STRING,
  transaction_date DATE NOT NULL,
  recorded_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  transaction_type STRING DEFAULT 'expense',
  payment_method STRING,
  is_recurring BOOL DEFAULT FALSE,
  recurrence_period STRING,
  notes STRING,
  source STRING DEFAULT 'manual',
  PRIMARY KEY(transaction_id),
  FOREIGN KEY(user_id) REFERENCES `finassist.users`(user_id),
  FOREIGN KEY(category_id) REFERENCES `finassist.categories`(category_id),
  FOREIGN KEY(subcategory_id) REFERENCES `finassist.subcategories`(subcategory_id)
)
PARTITION BY transaction_date
CLUSTER BY user_id, category_id;

-- Tabla de presupuestos
CREATE TABLE IF NOT EXISTS `finassist.budgets` (
  budget_id STRING NOT NULL,
  user_id STRING NOT NULL,
  category_id STRING,
  subcategory_id STRING,
  amount NUMERIC NOT NULL,
  currency STRING NOT NULL,
  period_type STRING DEFAULT 'monthly',
  start_date DATE,
  is_recurring BOOL DEFAULT TRUE,
  active BOOL DEFAULT TRUE,
  PRIMARY KEY(budget_id),
  FOREIGN KEY(user_id) REFERENCES `finassist.users`(user_id),
  FOREIGN KEY(category_id) REFERENCES `finassist.categories`(category_id),
  FOREIGN KEY(subcategory_id) REFERENCES `finassist.subcategories`(subcategory_id)
);

-- Tabla de objetivos financieros
CREATE TABLE IF NOT EXISTS `finassist.financial_goals` (
  goal_id STRING NOT NULL,
  user_id STRING NOT NULL,
  name STRING NOT NULL,
  description STRING,
  target_amount NUMERIC NOT NULL,
  currency STRING NOT NULL,
  current_amount NUMERIC DEFAULT 0,
  start_date DATE DEFAULT CURRENT_DATE(),
  target_date DATE,
  status STRING DEFAULT 'in_progress',
  priority STRING DEFAULT 'medium',
  PRIMARY KEY(goal_id),
  FOREIGN KEY(user_id) REFERENCES `finassist.users`(user_id)
);

-- Inserción de categorías predeterminadas
INSERT INTO `finassist.categories` (category_id, name, system_default, icon_reference, description)
VALUES
  ('cat_food', 'Food & Dining', TRUE, 'restaurant', 'Expenses related to food and dining'),
  ('cat_transport', 'Transportation', TRUE, 'commute', 'Expenses related to transportation'),
  ('cat_housing', 'Housing', TRUE, 'home', 'Expenses related to housing'),
  ('cat_utilities', 'Utilities', TRUE, 'utility', 'Expenses related to utilities'),
  ('cat_entertainment', 'Entertainment', TRUE, 'movie', 'Expenses related to entertainment'),
  ('cat_healthcare', 'Healthcare', TRUE, 'medical', 'Expenses related to healthcare'),
  ('cat_education', 'Education', TRUE, 'school', 'Expenses related to education'),
  ('cat_personal', 'Personal', TRUE, 'person', 'Personal expenses'),
  ('cat_shopping', 'Shopping', TRUE, 'shopping', 'Shopping expenses'),
  ('cat_income', 'Income', TRUE, 'payments', 'Sources of income');

-- Inserción de subcategorías predeterminadas (muestra parcial)
INSERT INTO `finassist.subcategories` (subcategory_id, category_id, name, system_default, description)
VALUES
  ('subcat_groceries', 'cat_food', 'Groceries', TRUE, 'Food purchases for home consumption'),
  ('subcat_restaurants', 'cat_food', 'Restaurants', TRUE, 'Dining out expenses'),
  ('subcat_fastfood', 'cat_food', 'Fast Food', TRUE, 'Fast food expenses'),
  
  ('subcat_gas', 'cat_transport', 'Gas/Fuel', TRUE, 'Fuel expenses'),
  ('subcat_publictransport', 'cat_transport', 'Public Transport', TRUE, 'Public transportation expenses'),
  ('subcat_rideshare', 'cat_transport', 'Ride Sharing', TRUE, 'Uber, Lyft, etc.'),
  
  ('subcat_rent', 'cat_housing', 'Rent', TRUE, 'Rental payments'),
  ('subcat_mortgage', 'cat_housing', 'Mortgage', TRUE, 'Mortgage payments'),
  
  ('subcat_electricity', 'cat_utilities', 'Electricity', TRUE, 'Electricity bills'),
  ('subcat_water', 'cat_utilities', 'Water', TRUE, 'Water bills'),
  ('subcat_internet', 'cat_utilities', 'Internet', TRUE, 'Internet bills'),
  
  ('subcat_streaming', 'cat_entertainment', 'Streaming Services', TRUE, 'Netflix, Disney+, etc.'),
  ('subcat_movies', 'cat_entertainment', 'Movies & Events', TRUE, 'Cinema tickets, live events'),
  
  ('subcat_salary', 'cat_income', 'Salary', TRUE, 'Employment income'),
  ('subcat_freelance', 'cat_income', 'Freelance', TRUE, 'Freelance income'),
  ('subcat_investments', 'cat_income', 'Investments', TRUE, 'Investment returns');
```

## Próximos Pasos

1. **Validar esquema** con requisitos específicos de FinAssist
2. **Implementar scripts de migración** para versiones futuras
3. **Desarrollar capa de acceso a datos** con patrones eficientes
4. **Implementar pruebas de rendimiento** con datos sintéticos
5. **Documentar patrones de consulta** recomendados para cada agente