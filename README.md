# FinAssist - Auditor Financiero Autónomo Multi-Agente

## Visión del Producto

FinAssist es un sistema multi-agente autónomo que actúa como auditor financiero personal o para pequeñas empresas. A diferencia de herramientas tradicionales, FinAssist no solo organiza transacciones: detecta patrones críticos, simula escenarios futuros, y entrega recomendaciones personalizadas y éticas utilizando una arquitectura avanzada de agentes especializados.

## Objetivos Principales

- **Automatizar la gestión financiera** mediante el procesamiento de lenguaje natural e importación de documentos
- **Proporcionar insights financieros valiosos** mediante análisis de patrones de gasto y detección de anomalías
- **Facilitar la toma de decisiones financieras** a través de simulaciones y recomendaciones personalizadas
- **Garantizar prácticas financieras éticas** mediante la evaluación de recomendaciones

## Arquitectura del Sistema

FinAssist se construye sobre el Agent Development Kit (ADK) de Google, implementando una arquitectura distribuida de múltiples agentes, cada uno con un rol especializado.

### Tecnologías Clave

- **Agent Development Kit (ADK)**: Núcleo de la lógica multi-agente
- **Google Cloud Functions & Pub/Sub**: Comunicación y eventos entre agentes
- **BigQuery**: Almacenamiento y análisis de datos transaccionales
- **Vertex AI (PaLM o Gemini)**: Procesamiento de lenguaje natural y generación de explicaciones
- **Google Sheets API / Looker Studio**: Visualización de reportes e insights

### Estructura de Agentes

| Agente | Función |
|--------|---------|
| **RootAgent** | Coordina todos los sub-agentes e interpreta la intención del usuario para dirigir las consultas al agente adecuado |
| **TransactionAgent** | Registra, modifica y gestiona transacciones financieras mediante lenguaje natural o importa datos de documentos |
| **CategorizerAgent** | Clasifica automáticamente los gastos en categorías usando embeddings y reglas adaptativas |
| **InsightAgent** | Analiza patrones de gasto, identifica anomalías, y detecta oportunidades de ahorro o riesgo |
| **SimulationAgent** | Permite correr simulaciones financieras: "¿qué pasa si elimino Uber o si ingreso X más?" |
| **EthicsAgent** | Evalúa la viabilidad y ética de las recomendaciones, evitando sugerencias perjudiciales |
| **ReportAgent** | Genera reportes visuales y resúmenes en lenguaje natural de los hallazgos financieros |

## Modelo de Datos

FinAssist utiliza BigQuery para almacenar y analizar datos financieros de forma eficiente. La estructura principal de la base de datos es:

### Esquema de Base de Datos

```
finassist/
├── users                  # Información y preferencias de usuarios
├── transactions          # Registro de transacciones financieras
├── categories            # Categorías principales para gastos/ingresos
├── subcategories         # Subcategorías para clasificación más específica
├── budgets               # Presupuestos por categoría y período
└── financial_goals       # Objetivos financieros del usuario
```

### Flujo de Datos Principal

1. El usuario interactúa con el sistema mediante lenguaje natural
2. RootAgent interpreta la intención y dirige la consulta al agente especializado
3. Los agentes especializados procesan, almacenan o recuperan datos de BigQuery según sea necesario
4. Los resultados se presentan al usuario en lenguaje natural o visualizaciones

## Casos de Uso Principales

### 1. Gestión de Transacciones
- **Descripción**: El usuario registra, modifica o consulta transacciones financieras mediante lenguaje natural
- **Ejemplo**: "Registra que ayer pagué $12.99 por mi suscripción de Netflix"
- **Agentes involucrados**: RootAgent → TransactionAgent → (posiblemente) CategorizerAgent
- **Resultado esperado**: Confirmación de registro con categorización adecuada

### 2. Análisis Financiero
- **Descripción**: El usuario solicita análisis de sus patrones de gasto o anomalías
- **Ejemplo**: "¿Cuáles son mis gastos recurrentes innecesarios?"
- **Agentes involucrados**: RootAgent → InsightAgent
- **Resultado esperado**: Lista priorizada de gastos recurrentes con recomendaciones

### 3. Simulación Financiera
- **Descripción**: El usuario plantea escenarios hipotéticos para evaluar impacto
- **Ejemplo**: "¿Qué pasaría si reduzco mi gasto en comida un 20%?"
- **Agentes involucrados**: RootAgent → SimulationAgent → (posiblemente) EthicsAgent
- **Resultado esperado**: Proyección financiera del escenario con evaluación ética

### 4. Generación de Reportes
- **Descripción**: El usuario solicita resúmenes o visualizaciones de su situación financiera
- **Ejemplo**: "Muéstrame un resumen de mis finanzas de abril"
- **Agentes involucrados**: RootAgent → ReportAgent
- **Resultado esperado**: Reporte visual con análisis narrativo

## Métricas de Éxito

- **Precisión en extracción de información**: >95% de datos correctamente extraídos de entradas de usuario
- **Precisión en categorización**: >90% de transacciones correctamente categorizadas
- **Valor percibido**: >80% de usuarios reportan obtener insights que no conocían previamente
- **Eficiencia**: Reducción del 50% en tiempo dedicado a gestión financiera manual

## Riesgos y Mitigación

| Riesgo | Impacto | Probabilidad | Estrategia de mitigación |
|--------|---------|--------------|--------------------------|
| Imprecisión en procesamiento de lenguaje natural | Alto | Media | Implementar ciclos de feedback y mejora continua de prompts |
| Sobrecosto en BigQuery | Medio | Baja | Implementar particionamiento adecuado y monitoreo de consultas |
| Recomendaciones financieras inadecuadas | Alto | Media | Implementar EthicsAgent y sistema de revisión humana para casos límite |
| Dificultad de integración entre agentes | Medio | Media | Implementar arquitectura modular con interfaces bien definidas |

## Plan de Desarrollo

El desarrollo de FinAssist seguirá un enfoque incremental por fases, priorizando la funcionalidad core y expandiendo gradualmente sus capacidades:

1. **Infraestructura Básica y RootAgent** - Establecer fundamentos del sistema
2. **Registro y Gestión de Transacciones** - Implementar capacidades transaccionales
3. **Análisis y Visualización Básica** - Desarrollar insights y reportes iniciales
4. **Presupuestos y Objetivos Financieros** - Expandir a gestión presupuestaria
5. **Simulaciones y Ética Financiera** - Implementar capacidades avanzadas
6. **Refinamiento e Inteligencia Avanzada** - Optimizar y mejorar el sistema

## Alcance de la Versión 1.0

Para la primera versión funcional (MVP), el alcance incluirá:
- Implementación completa de RootAgent y TransactionAgent
- Capacidades básicas de CategorizerAgent e InsightAgent
- Integración con BigQuery para almacenamiento y consulta
- Interfaz conversacional funcional mediante ADK
- Soporte para operaciones básicas de transacciones y consultas simples

## Criterios de Aceptación V1.0

- El sistema puede registrar transacciones a partir de lenguaje natural con >90% de precisión
- El sistema puede categorizar automáticamente transacciones con >85% de precisión
- El sistema puede responder a consultas básicas sobre gastos por categoría y período
- El sistema puede importar transacciones desde documentos CSV básicos
- El tiempo de respuesta promedio es <3 segundos para operaciones estándar

---

## Próximos Pasos

1. Finalizar especificaciones detalladas de cada agente
2. Configurar entorno de desarrollo y repositorio
3. Implementar esquema inicial de BigQuery
4. Desarrollar prototipo de RootAgent