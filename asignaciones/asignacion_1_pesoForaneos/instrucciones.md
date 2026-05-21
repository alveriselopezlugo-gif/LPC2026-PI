# Asignación 1: Optimización de Horarios y Consenso Colectivo 🏛️📊

## 🎯 Objetivo del Proyecto
El estudiante diseñará un script en Python que procese de forma automatizada los tokens de disponibilidad de la sección. El reto consiste en evaluar el comportamiento del grupo usando dos métricas sencillas para descubrir qué pasa cuando aumentamos progresivamente el peso o la importancia de un estudiante foráneo ($W_f$ desde 1.0 hasta 10.0), buscando un equilibrio justo donde la mayoría local no destruya las opciones de la minoría foránea.

---

## ⚖️ Las Dos Métricas de Evaluación (Reglas del Juego)

Para evaluar cada bloque horario disponible, el script calculará simultáneamente dos valores por cada incremento de peso:

### 1. El Bienestar General ($U_{total}$)
Es el puntaje que recibe un bloque horario tras evaluar a todos los estudiantes de la sección. Se calcula sumando los puntos de cada alumno según esta regla:

* **Si el estudiante PUEDE asistir:** Suma **+1.0 punto**. 
* **Si el estudiante además QUIERE ese bloque (Preferencia):** Se gana un bono extra de **+0.5 puntos** (en total sumaría +1.5).
* **Si el estudiante NO PUEDE asistir:** Se aplica una penalización drástica de **-1.5 puntos** (castigo por exclusión).

**El factor del peso:** Antes de sumar los puntos de un estudiante al total del bloque, debes multiplicarlos por su peso político:
* Si el estudiante es **Local**, su peso es siempre **1.0**.
* Si el estudiante es **Foráneo**, su puntos se multiplican por el **$W_f$** de la iteración actual (que varía de 1.0 a 10.0).

---

### 2. El Índice de Satisfacción Neta ($ISN$)
Mide qué porcentaje de los estudiantes que **sí logran asistir** a la clase quedaron realmente felices con el horario seleccionado (es decir, cuántos consiguieron su bloque deseado).

$$ISN = \frac{\text{Alumnos incluidos que consiguieron su "Quiero"}}{\text{Total de Alumnos que "Pueden" asistir}} \times 100\%$$

*Nota: Esta métrica sirve para demostrar que lograr que un estudiante asista a clase por obligación no significa que el horario sea cómodo para su realidad.*

---

## 🛠️ Especificaciones Técnicas del Script
Se recomienda usar herramientas de Inteligencia Artificial (como Gemini o ChatGPT) para que te ayuden con la sintaxis de Python. Tu programa debe hacer lo siguiente:

1. **Decodificación Segura:** Leer el archivo de texto con los tokens en Base64, decodificarlos y convertirlos a diccionarios JSON. Usa bloques `try-except` para evitar que el programa se detenga si un token está mal copiado.
2. **Simulación:** Hacer un ciclo (`for`) que varíe el peso del foráneo de **1.0 a 10.0** con pasos de 0.1.
3. **Optimización:** En cada paso, revisar todos los bloques de la semana (Lunes a Viernes, de 08-10 hasta 14-16), calcular el Bienestar General ($U_{total}$) y quedarse con el bloque que dé la puntuación más alta. Para ese bloque ganador, calcula también el $ISN$.
4. **Gráfica Bifocal:** Generar una gráfica en Matplotlib con **doble eje Y**. El eje X será el Peso del Foráneo; el eje Y izquierdo mostrará la curva continua del Bienestar General ($U_{total}$); y el eje Y derecho mostrará de forma discontinua (línea punteada) el porcentaje de Satisfacción ($ISN$).

---

## 📋 Requisitos de Entrega
Carga en tu carpeta asignada dentro del repositorio (`estudiantes/tu_nombre_apellido/`) los siguientes archivos:

1. **`solucion.py` o `solucion.ipynb`:** El código fuente documentado y listo para correr.
2. **`grafica_consenso.png`:** La imagen exportada por tu script.
3. **`defensa.md`:** Un pequeño informe donde respondas con tus palabras:
   * Al correr la simulación, la curva de Satisfacción ($ISN$) se queda completamente plana en el tiempo. ¿Por qué crees que ocurre esto al analizar los datos reales de tus compañeros?
   * ¿Cuál es el bloque horario que el algoritmo seleccionó como el consenso definitivo para la sección?

---

## 🤖 Guía de Prompts Sugerida (Para usar con la IA)
Si te cuesta armar la gráfica de doble eje, puedes pedirle ayuda a la IA usando un prompt estructurado como este:

> *"Actúa como un tutor de Python para primer semestre. Necesito graficar una simulación en Matplotlib. El eje X va de 1.0 a 10.0. Necesito dos ejes Y en la misma gráfica: el izquierdo debe mostrar una curva continua color índigo para valores de utilidad (entre -3 y -13), y el derecho debe mostrar una línea punteada naranja para valores en porcentaje (0 a 100%). Agrega cuadrícula y coloca la leyenda unificada abajo a la derecha para que no tape las líneas."*
