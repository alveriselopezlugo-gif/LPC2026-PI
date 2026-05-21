# Asignación 1: Optimización de Recursos Colectivos y Consenso Social

## 🎯 Objetivo del Proyecto
El estudiante diseñará e implementará un script en Python que procese de forma automatizada los tokens de disponibilidad generados por la sección en WhatsApp. El núcleo del reto consiste en evaluar el comportamiento del sistema mediante un enfoque bicriterio, utilizando dos métricas juezas concurrentes para determinar matemáticamente el **Peso Ideal ($W_f$)** de influencia que se le debe otorgar a un estudiante foráneo. El fin es equilibrar de forma "justa" el sistema, protegiendo a la minoría vulnerable sin destruir la satisfacción de la mayoría local.

---

## ⚖️ Las Dos Métricas Juezas de Evaluación

Para auditar el comportamiento del sistema a medida que aumentamos el peso del estudiante foráneo ($W_f$ de 1.0 a 10.0), el script deberá calcular y graficar simultáneamente dos dimensiones independientes:

### 1. El Bienestar General del Sistema ($U_{total}$)
Es la función de utilidad global que balancea las restricciones logísticas de la sección mediante un modelo de optimización lineal condicional. Su ecuación matemática formal para un bloque horario específico $b$ está definida por:

$$U_{total}(b) = \sum_{i=1}^{N} \omega_i \cdot \Big[ \mathbb{I}(b \in v_{p,i}) \cdot \big(1.0 + 0.5 \cdot \mathbb{I}(b \in v_{d,i})\big) - 1.5 \cdot \mathbb{I}(b \notin v_{p,i}) \Big]$$

**Donde el vector de pesos políticos ($\omega_i$) se define dinámicamente como:**
$$\omega_i = \begin{cases} 1.0 & \text{si el estudiante } i \text{ es Local } (f_i = \text{False}) \\ W_f & \text{si el estudiante } i \text{ es Foráneo } (f_i = \text{True}) \end{cases}$$

**Y las funciones indicadoras $\mathbb{I}(\text{condición})$ operan de la siguiente manera:**
* $\mathbb{I}(b \in v_{p,i}) = 1$ si el bloque está en su disponibilidad (**"Puedo"**), otorgando $+1.0$ punto.
* $\mathbb{I}(b \in v_{d,i}) = 1$ si el bloque coincide además con su preferencia (**"Quiero"**), otorgando un bono adicional de $+0.5$ puntos.
* $\mathbb{I}(b \notin v_{p,i}) = 1$ si el bloque **no** está en su disponibilidad, aplicando una penalización drástica de $-1.5$ puntos por exclusión del sistema.

---

### 2. El Índice de Satisfacción Neta Preferencial ($ISN$)
Representa el "Nivel de Confort" real de la subpoblación de estudiantes que el algoritmo logra incorporar de forma efectiva en el horario seleccionado. Su fórmula matemática formal es:

$$ISN(b) = \frac{\sum_{i=1}^{N} \mathbb{I}(b \in v_{p,i} \land b \in v_{d,i})}{\sum_{i=1}^{N} \mathbb{I}(b \in v_{p,i})} \times 100\%$$

*Esta métrica aísla el vector **"Quiero" (`v_d`)** para responder con rigor analítico a la siguiente premisa de la teoría de decisiones: "Lograr que un estudiante asista a clase (disponibilidad) no significa que las condiciones de su entorno sean satisfactorias (preferencia)".*
---

## 🛠️ Especificaciones Técnicas del Script
Se recomienda ampliamente el uso de herramientas de Inteligencia Artificial (como Gemini o ChatGPT) para asistir en la generación de la estructura sintáctica del código. El programa final debe operar bajo las siguientes fases lógicas:

1. **Fase de Ingesta (Parsing):** Leer un archivo plano `.txt` con los tokens codificados en Base64. Debe decodificarlos de forma segura, convirtiendo la cadena de vuelta a un objeto JSON legible (diccionario de Python) e incluyendo control de excepciones (`try-except`) para manejar errores de copiado o falta de alineación (*padding*) sin detener el programa.
2. **Fase de Simulación Lineal:** Iterar progresivamente variando el factor de peso para los estudiantes foráneos (`f = True`) en un rango continuo desde **1.0 hasta 10.0** (con incrementos discretos de 0.1). El peso de los locales se mantendrá estático en 1.0.
3. **Fase de Optimización Colectiva:** Por cada incremento de peso, evaluar todo el espacio de estados de bloques horarios disponibles (Lunes a Viernes, de 08-10 hasta 14-16) para hallar el bloque que maximice el Bienestar General ($U_{total}$) y calcular el $ISN$ resultante para ese bloque óptimo.
4. **Fase de Visualización Avanzada:** Generar una gráfica analítica utilizando un **doble eje Y** (`ax.twinx()` en Matplotlib). El eje $X$ representará el peso del foráneo; el eje $Y$ izquierdo mostrará la curva del Bienestar General ($U_{total}$); y el eje $Y$ derecho mostrará de forma discontinua el porcentaje de Satisfacción Neta ($ISN$).

---

## 📋 Requisitos de Entrega
Cada estudiante debe cargar en su respectiva subcarpeta asignada dentro del directorio `estudiantes/` los siguientes archivos:

1. **`solucion.py` o `solucion.ipynb`:** El código fuente en Python, debidamente documentado, limpio y libre de errores de ejecución.
2. **`grafica_consenso.png`:** La imagen exportada directamente por el script donde se visualice claramente el comportamiento de ambas curvas, las etiquetas de los bloques horarios dominantes y la línea del peso óptimo detectado.
3. **`defensa.md`:** Un breve reporte explicativo que responda con rigurosidad científica las siguientes preguntas:
   * Al ejecutar la simulación con los datos reales de la sección, la curva de Satisfacción Neta ($ISN$) exhibe un comportamiento totalmente estático y plano a lo largo del eje. ¿Qué interpretación sistémica, física o social atribuye a este fenómeno particular?
   * ¿Por qué el punto crítico de equilibrio o "Número de la Justicia" ($W_i$) se ubica al inicio del espectro en este set de datos y qué bloque horario representa el atractor global del sistema?

---

## 🤖 Guía de Orientación para Ingeniería de Prompts (Uso de IA)
No intente escribir toda la lógica algorítmica desde cero si presenta dificultades con la sintaxis. Puede estructurar sus instrucciones a la IA dividiendo el problema en bloques específicos.

**Ejemplo de Prompt Base sugerido para la visualización:**
> *"Actúa como un experto en visualización de datos con Matplotlib en Python. Necesito que generes un fragmento de código para graficar un sistema bivariado compartiendo el mismo eje X (pesos de 1.0 a 10.0). El eje Y izquierdo debe graficar una curva continua de utilidad (valores negativos entre -3 y -13) en color índigo. El eje Y derecho debe graficar una curva discontinua de porcentaje (escala de 0 a 100%) en color naranja. Asegúrate de unificar las leyendas de ambos ejes en una sola caja ubicada en la esquina inferior derecha para que no obstruya las líneas de datos."*
