# Flujos de Interacción y Diagramas de Secuencia

Este documento describe los principales flujos de interacción entre el usuario y los agentes de FinAssist, así como los diagramas de secuencia para los casos de uso más importantes.

## 1. Flujo de Procesamiento Principal

```mermaid
sequenceDiagram
    participant Usuario
    participant RootAgent
    participant AgenteEspecializado
    participant BigQuery

    Usuario->>RootAgent: Consulta en lenguaje natural
    RootAgent->>RootAgent: Analiza intención
    
    alt Consulta simple
        RootAgent->>BigQuery: Consulta datos básicos
        BigQuery->>RootAgent: Resultados
        RootAgent->>Usuario: Respuesta directa
    else Consulta especializada
        RootAgent->>AgenteEspecializado: Deriva consulta con contexto
        AgenteEspecializado->>BigQuery: Consulta datos específicos
        BigQuery->>AgenteEspecializado: Resultados
        AgenteEspecializado->>AgenteEspecializado: Procesa información
        AgenteEspecializado->>RootAgent: Devuelve respuesta procesada
        RootAgent->>Usuario: Respuesta formateada
    end
```

## 2. Registro de Transacción

```mermaid
sequenceDiagram
    participant Usuario
    participant RootAgent
    participant TransactionAgent
    participant CategorizerAgent
    participant BigQuery

    Usuario->>RootAgent: "Registra que pagué $50 en el restaurante ayer"
    RootAgent->>RootAgent: Identifica intención de registro
    RootAgent->>TransactionAgent: Deriva consulta con contexto
    
    TransactionAgent->>TransactionAgent: Extrae entidades (monto, fecha, establecimiento)
    
    alt Información completa
        TransactionAgent->>CategorizerAgent: Solicita categorización
        CategorizerAgent->>BigQuery: Consulta patrones previos
        BigQuery->>CategorizerAgent: Datos históricos
        CategorizerAgent->>TransactionAgent: Sugiere categoría (ej. "Alimentación/Restaurantes")
        
        TransactionAgent->>BigQuery: Almacena transacción
        BigQuery->>TransactionAgent: Confirmación
        
        TransactionAgent->>RootAgent: Confirmación de registro
        RootAgent->>Usuario: "He registrado tu gasto de $50 en restaurante como Alimentación/Restaurantes"
    else Información incompleta
        TransactionAgent->>RootAgent: Solicita información adicional
        RootAgent->>Usuario: "¿En qué restaurante realizaste este gasto?"
        Usuario->>RootAgent: "En La Parrilla"
        RootAgent->>TransactionAgent: Proporciona información adicional
        
        TransactionAgent->>CategorizerAgent: Solicita categorización
        CategorizerAgent->>BigQuery: Consulta patrones previos
        BigQuery->>CategorizerAgent: Datos históricos
        CategorizerAgent->>TransactionAgent: Sugiere categoría
        
        TransactionAgent->>BigQuery: Almacena transacción
        BigQuery->>TransactionAgent: Confirmación
        
        TransactionAgent->>RootAgent: Confirmación de registro
        RootAgent->>Usuario: Confirmación con detalles completos
    end
```

## 3. Análisis de Gastos y Generación de Insights

```mermaid
sequenceDiagram
    participant Usuario
    participant RootAgent
    participant InsightAgent
    participant BigQuery

    Usuario->>RootAgent: "¿Cuáles son mis gastos innecesarios este mes?"
    RootAgent->>RootAgent: Identifica intención de análisis
    RootAgent->>InsightAgent: Deriva consulta
    
    InsightAgent->>BigQuery: Consulta transacciones del mes actual
    BigQuery->>InsightAgent: Datos de transacciones
    
    InsightAgent->>BigQuery: Consulta patrones históricos
    BigQuery->>InsightAgent: Datos históricos
    
    InsightAgent->>InsightAgent: Analiza patrones y detecta anomalías
    InsightAgent->>InsightAgent: Identifica gastos recurrentes optimizables
    InsightAgent->>InsightAgent: Prioriza insights por impacto
    
    InsightAgent->>RootAgent: Devuelve insights procesados
    RootAgent->>Usuario: "He identificado los siguientes gastos potencialmente innecesarios: 1) Suscripciones duplicadas ($X/mes), 2) Comisiones bancarias evitables ($Y/mes)..."
```

## 4. Creación y Seguimiento de Presupuesto

```mermaid
sequenceDiagram
    participant Usuario
    participant RootAgent
    participant InsightAgent
    participant BigQuery

    Usuario->>RootAgent: "Crea un presupuesto de $500 para alimentación este mes"
    RootAgent->>RootAgent: Identifica intención de presupuesto
    
    RootAgent->>BigQuery: Almacena nuevo presupuesto
    BigQuery->>RootAgent: Confirmación
    
    RootAgent->>InsightAgent: Solicita análisis de viabilidad
    InsightAgent->>BigQuery: Consulta gastos históricos en alimentación
    BigQuery->>InsightAgent: Datos históricos
    
    InsightAgent->>InsightAgent: Analiza viabilidad del presupuesto
    InsightAgent->>RootAgent: Evaluación de viabilidad
    
    alt Presupuesto viable
        RootAgent->>Usuario: "He creado tu presupuesto de $500 para alimentación. Basado en tus gastos anteriores ($X/mes en promedio), este presupuesto es [realista/ajustado/desafiante]."
    else Presupuesto poco realista
        RootAgent->>Usuario: "He creado tu presupuesto de $500 para alimentación, pero debo señalar que históricamente has gastado un promedio de $X/mes en esta categoría. ¿Deseas mantener este objetivo o ajustarlo?"
    end
```

## 5. Simulación Financiera

```mermaid
sequenceDiagram
    participant Usuario
    participant RootAgent
    participant SimulationAgent
    participant EthicsAgent
    participant BigQuery
    participant ReportAgent

    Usuario->>RootAgent: "¿Qué pasaría si reduzco mi gasto en restaurantes un 50%?"
    RootAgent->>RootAgent: Identifica intención de simulación
    RootAgent->>SimulationAgent: Deriva consulta
    
    SimulationAgent->>BigQuery: Consulta gastos en restaurantes
    BigQuery->>SimulationAgent: Datos históricos
    
    SimulationAgent->>SimulationAgent: Calcula impacto de reducción
    SimulationAgent->>SimulationAgent: Proyecta escenario a 3/6/12 meses
    
    SimulationAgent->>EthicsAgent: Solicita evaluación de viabilidad
    EthicsAgent->>EthicsAgent: Evalúa realismo y sostenibilidad
    EthicsAgent->>SimulationAgent: Resultado de evaluación
    
    SimulationAgent->>ReportAgent: Solicita visualización
    ReportAgent->>ReportAgent: Genera gráficos comparativos
    ReportAgent->>SimulationAgent: Devuelve visualizaciones
    
    SimulationAgent->>RootAgent: Resultados completos de simulación
    RootAgent->>Usuario: "Reduciendo tu gasto en restaurantes un 50% (de $X a $Y mensual), podrías ahorrar aproximadamente $Z en 6 meses. Esto representaría un N% de aumento en tu capacidad de ahorro mensual. Según tus patrones actuales, esta meta es [evaluación de viabilidad]."
```

## 6. Importación de Transacciones desde CSV

```mermaid
sequenceDiagram
    participant Usuario
    participant RootAgent
    participant TransactionAgent
    participant CategorizerAgent
    participant BigQuery

    Usuario->>RootAgent: "Importa este archivo CSV de mi banco"
    RootAgent->>RootAgent: Identifica intención de importación
    RootAgent->>TransactionAgent: Deriva solicitud con archivo
    
    TransactionAgent->>TransactionAgent: Procesa archivo CSV
    TransactionAgent->>TransactionAgent: Extrae transacciones
    
    loop Para cada transacción
        TransactionAgent->>BigQuery: Verifica duplicados
        BigQuery->>TransactionAgent: Resultado verificación
        
        alt No es duplicado
            TransactionAgent->>CategorizerAgent: Solicita categorización
            CategorizerAgent->>CategorizerAgent: Asigna categoría
            CategorizerAgent->>TransactionAgent: Categoría asignada
            
            TransactionAgent->>BigQuery: Almacena transacción
            BigQuery->>TransactionAgent: Confirmación
        else Es duplicado
            TransactionAgent->>TransactionAgent: Marca como duplicado
        end
    end
    
    TransactionAgent->>RootAgent: Resumen de importación
    RootAgent->>Usuario: "He importado 15 transacciones de tu archivo CSV. 12 fueron registradas correctamente, 3 fueron identificadas como duplicados. ¿Deseas revisar las categorías asignadas?"
```

## 7. Generación de Reporte Mensual

```mermaid
sequenceDiagram
    participant Usuario
    participant RootAgent
    participant ReportAgent
    participant InsightAgent
    participant BigQuery

    Usuario->>RootAgent: "Muéstrame un resumen de mis finanzas de abril"
    RootAgent->>RootAgent: Identifica intención de reporte
    RootAgent->>ReportAgent: Deriva solicitud
    
    ReportAgent->>BigQuery: Consulta transacciones de abril
    BigQuery->>ReportAgent: Datos de transacciones
    
    ReportAgent->>BigQuery: Consulta presupuestos de abril
    BigQuery->>ReportAgent: Datos de presupuestos
    
    ReportAgent->>InsightAgent: Solicita análisis de tendencias
    InsightAgent->>InsightAgent: Analiza datos
    InsightAgent->>ReportAgent: Insights relevantes
    
    ReportAgent->>ReportAgent: Genera visualizaciones
    ReportAgent->>ReportAgent: Compila resumen narrativo
    
    ReportAgent->>RootAgent: Reporte completo
    RootAgent->>Usuario: Presentación del reporte mensual con gráficos, tendencias principales e insights
```

## 8. Flujo de Evaluación Ética de Recomendación

```mermaid
sequenceDiagram
    participant InsightAgent
    participant EthicsAgent
    participant BigQuery

    InsightAgent->>InsightAgent: Genera recomendación financiera
    InsightAgent->>EthicsAgent: Solicita evaluación ética
    
    EthicsAgent->>BigQuery: Consulta perfil financiero completo
    BigQuery->>EthicsAgent: Datos de perfil
    
    EthicsAgent->>EthicsAgent: Analiza riesgo financiero
    EthicsAgent->>EthicsAgent: Evalúa adecuación a objetivos
    EthicsAgent->>EthicsAgent: Verifica sostenibilidad
    
    alt Recomendación adecuada
        EthicsAgent->>InsightAgent: Aprueba recomendación
        InsightAgent->>InsightAgent: Presenta recomendación al usuario
    else Recomendación problemática
        EthicsAgent->>InsightAgent: Rechaza con explicación
        InsightAgent->>InsightAgent: Genera alternativa más segura
        InsightAgent->>EthicsAgent: Solicita evaluación de alternativa
        EthicsAgent->>InsightAgent: Evaluación de alternativa
    end
```

## 9. Flujo de Detección y Categorización de Transacción Recurrente

```mermaid
sequenceDiagram
    participant Usuario
    participant RootAgent
    participant TransactionAgent
    participant BigQuery

    Usuario->>RootAgent: "Registra mi pago de Netflix de $13.99"
    RootAgent->>TransactionAgent: Deriva solicitud de registro
    
    TransactionAgent->>BigQuery: Busca transacciones similares
    BigQuery->>TransactionAgent: Historial de transacciones
    
    TransactionAgent->>TransactionAgent: Identifica patrón recurrente
    
    alt Primera ocurrencia
        TransactionAgent->>BigQuery: Registra como transacción normal
        BigQuery->>TransactionAgent: Confirmación
        TransactionAgent->>RootAgent: Confirmación de registro
        RootAgent->>Usuario: "He registrado tu pago de Netflix. ¿Es este un pago recurrente que debo recordar?"
    else Recurrencia detectada
        TransactionAgent->>TransactionAgent: Marca como recurrente
        TransactionAgent->>BigQuery: Actualiza como transacción recurrente
        BigQuery->>TransactionAgent: Confirmación
        TransactionAgent->>RootAgent: Confirmación con contexto de recurrencia
        RootAgent->>Usuario: "He registrado tu pago recurrente de Netflix. Basado en tu historial, esto ocurre mensualmente alrededor del día 15."
    end
```

## 10. Flujo Completo Multi-Agente para Consulta Compleja

```mermaid
sequenceDiagram
    participant Usuario
    participant RootAgent
    participant TransactionAgent
    participant InsightAgent
    participant SimulationAgent
    participant ReportAgent
    participant BigQuery

    Usuario->>RootAgent: "Registra mi gasto de $80 en restaurante y dime cómo afecta a mi presupuesto mensual y si debo ajustar mis hábitos de consumo"
    
    RootAgent->>RootAgent: Analiza intención múltiple
    
    RootAgent->>TransactionAgent: Solicita registro de transacción
    TransactionAgent->>BigQuery: Registra transacción
    BigQuery->>TransactionAgent: Confirmación
    TransactionAgent->>RootAgent: Confirmación de registro
    
    RootAgent->>InsightAgent: Solicita análisis de impacto en presupuesto
    InsightAgent->>BigQuery: Consulta presupuesto y gastos actuales
    BigQuery->>InsightAgent: Datos financieros
    InsightAgent->>InsightAgent: Analiza impacto
    InsightAgent->>RootAgent: Resultados de análisis
    
    RootAgent->>SimulationAgent: Solicita proyección si continúa patrón
    SimulationAgent->>BigQuery: Consulta datos históricos
    BigQuery->>SimulationAgent: Datos históricos
    SimulationAgent->>SimulationAgent: Proyecta tendencias
    SimulationAgent->>RootAgent: Resultados de simulación
    
    RootAgent->>ReportAgent: Solicita visualización comparativa
    ReportAgent->>ReportAgent: Genera visualización
    ReportAgent->>RootAgent: Devuelve visualización
    
    RootAgent->>RootAgent: Compila respuesta integral
    RootAgent->>Usuario: "He registrado tu gasto de $80 en restaurante. Este gasto representa el X% de tu presupuesto mensual en alimentación, del cual ya has usado un Y%. Si continúas con este patrón de gastos, superarás tu presupuesto en aproximadamente Z días. Basado en tu historial, podrías considerar reducir la frecuencia de comidas en restaurantes de N a M veces por semana para mantenerte dentro del presupuesto."
```

## Notas sobre los Flujos de Interacción

1. **Coordinación centralizada**: El RootAgent actúa siempre como punto central de coordinación, manteniendo el contexto de la conversación y asegurando coherencia en las respuestas.

2. **Flujos paralelos vs. secuenciales**: Para consultas que involucran múltiples agentes, generalmente se sigue un flujo secuencial donde el resultado de un agente alimenta al siguiente, aunque en algunos escenarios podrían ejecutarse procesos paralelos.

3. **Manejo de contexto**: El contexto del usuario (preferencias, historial reciente) se mantiene en memoria durante la sesión y se pasa entre agentes según sea necesario.

4. **Gestión de errores**: No representada explícitamente en los diagramas, pero cada interacción incluye manejo de errores (datos no disponibles, ambigüedad en la consulta, etc.).

5. **Optimización de consultas**: En implementación real, se optimizarían las consultas a BigQuery para minimizar carga y costos, agrupando consultas relacionadas cuando sea posible.

6. **Umbral de confianza**: Los agentes utilizan umbrales de confianza para determinar cuándo solicitar clarificación vs. proceder con la información disponible.

7. **Aprendizaje adaptativo**: A lo largo del tiempo, los agentes mejoran sus respuestas basadas en el historial de interacciones, aunque esto no se muestra explícitamente en los diagramas.