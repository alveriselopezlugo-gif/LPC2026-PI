# Asignación 1: Optimización de Recursos Colectivos y Consenso Social 🏛️📊

## 🎯 Objetivo del Proyecto
El estudiante diseñará e implementará un script en Python que procese de forma automatizada los tokens de disponibilidad generados por la sección en WhatsApp. El núcleo del reto consiste en utilizar una **Métrica Juez** basada en el **Ratio de Sacrificio ($S$)** para determinar matemáticamente el **Peso Ideal ($W_f$)** de influencia que se le debe otorgar a un estudiante foráneo para equilibrar de forma "justa" el sistema, protegiendo a la minoría vulnerable sin destruir el bienestar de la mayoría local.

---

## ⚖️ La Métrica Juez: Ratio de Sacrificio ($S$)
Para evaluar qué tan "justo" o equilibrado es un horario a medida que aumentamos el peso del estudiante foráneo, utilizaremos formalmente la siguiente ecuación:

$$S = \frac{\text{Locales Excluidos}}{\text{Foráneos Incluidos}}$$

### 🔍 Interpretación del Ratio:
* **Si $S < 1$:** El sistema es eficiente. Al aumentar el peso, logramos incluir a estudiantes foráneos sacrificando a menos estudiantes locales en el proceso.
* **Si $S = 1$:** Es el **Punto de Inflexión Crítico**. El costo de inclusión es exactamente equivalente al costo de exclusión.
* **Si $S > 1$:** El sistema entra en desequilibrio perjudicial. El algoritmo está excluyendo a demasiados estudiantes locales solo para forzar la entrada de un foráneo (Tiranía del Outlier).

El **Peso Ideal ($W_i$)** a reportar será el valor máximo en el que el sistema logre el mayor equilibrio antes de que el Ratio de Sacrificio colapse o supere la unidad de forma irreversible.

---

## 🛠️ Especificaciones Técnicas del Script
Para resolver este problema, se recomienda ampliamente el uso de herramientas de Inteligencia Artificial (como Gemini o ChatGPT) para asistir en la generación de la estructura del código. El script final debe operar bajo las siguientes fases lógicas:

1. **Fase de Ingesta (Parsing):** El programa debe de leer un archivo plano `.txt` que contenga los tokens codificados en Base64 enviados por el grupo. Debe decodificar cada token de forma segura, convirtiendo la cadena Base64 de vuelta a un objeto JSON legible en Python.
2. **Fase de Simulación Lineal:** El algoritmo debe iterar progresivamente variando un factor de peso para los estudiantes foráneos (`f = True`) en un rango continuo desde **1.0 hasta 10.0** (con incrementos discretos de 0.1). El peso de los locales se mantendrá estático en 1.0.
3. **Fase de Optimización Colectiva:** Por cada incremento de peso, el script evaluará todo el espacio de estados de bloques horarios disponibles (Lunes a Viernes, de 08-10 hasta 14-16) calculando el Ratio de Sacrificio ($S$) para hallar cuál es el bloque óptimo.
4. **Fase de Visualización:** El script debe generar, utilizando librerías de graficación (como `matplotlib` o `seaborn`), una gráfica analítica impecable que relacione el peso del foráneo en el eje $X$ con la puntuación de la métrica juez en el eje $Y$, señalando visualmente el punto crítico de equilibrio o "Peso Ideal".

---

## 🧠 Restricciones Obligatorias del Análisis
La evaluación de la asistencia no puede ser un simple conteo plano. Es **estrictamente obligatorio** que su diseño incorpore el vector de preferencias ideales, denotado en el JSON como **"Quiero" (`v_d`)**, adicionalmente al vector de disponibilidad **"Puedo" (`v_p`)**. El uso de `v_d` les servirá para cuantificar los niveles de "satisfacción vs. insatisfacción" de los estudiantes que van quedando seleccionados en cada iteración.

---

## 📋 Requisitos de Entrega
Cada estudiante debe cargar en su respectiva subcarpeta asignada dentro del directorio `estudiantes/` los siguientes archivos:

1. **`solucion.py` o `solucion.ipynb`:** El código fuente en Python, debidamente documentado, limpio y libre de errores de ejecución.
2. **`grafica_consenso.png`:** La imagen exportada directamente por el script donde se visualice claramente el comportamiento de la curva y el peso óptimo detectado.
3. **`defensa.md`:** Un breve reporte explicativo que responda con rigurosidad científica las siguientes preguntas:
   * ¿Cuál fue la lógica lógica/algorítmica que usaste para contar los "Excluidos" e "Incluidos" basándote en los vectores `v_p` y `v_d`?
   * ¿Qué significado físico o social atribuye a la pendiente observada en su gráfica?
   * Basado en sus datos analizados, ¿cuál es el número exacto de la justicia para esta sección y qué bloque horario representa el consenso óptimo del sistema?

---

## 🤖 Guía de Orientación para Ingeniería de Prompts (Uso de IA)
Para desarrollar el código de forma eficiente, no intente escribir toda la sintaxis desde cero si presenta dificultades. Puede estructurar sus instrucciones a la IA dividiendo el problema. 

**Ejemplo de Prompt Base sugerido para iniciar:**
> *"Actúa como un científico de datos experto en Python. Necesito que generes un script estructurado que tome una lista de cadenas en Base64, las decodifique usando la librería `base64` y convierta el resultado de bytes a un diccionario JSON usando `json.loads`. Asegúrate de incluir un bloque `try-except` robusto con manejo de excepciones por si alguna cadena de texto llega corrupta o le falta relleno (padding), de modo que el programa avise en consola el error pero continúe procesando los elementos válidos."*
