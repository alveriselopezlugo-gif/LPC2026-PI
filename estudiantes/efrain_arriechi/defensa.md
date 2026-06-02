# defensa.md

## 1. Al correr la simulación, la curva de Satisfacción (ISN) se queda completamente plana. ¿Por qué crees que ocurre esto al analizar los datos reales de tus compañeros?

En el método original con pesos políticos (Wf de 1.0 a 1.5), la curva del ISN
sí permanecía completamente plana porque el bloque ganador nunca cambiaba a lo
largo de toda la simulación. Como el algoritmo seleccionaba siempre el mismo
bloque (`Jue_12-14`), el conjunto de estudiantes que podía asistir era idéntico
en cada iteración, y por lo tanto el cociente felices/asistentes daba siempre
el mismo resultado: 42.9%.

Sin embargo, ese resultado revela un problema de fondo: el bloque con más
asistentes no era necesariamente el más satisfactorio. De los 7 que podían ir
al `Jue_12-14`, solo 3 lo tenían como preferencia real. La curva plana no
indicaba estabilidad genuina, sino que el algoritmo estaba atrapado en un
máximo local — un bloque popular por cantidad pero no por calidad.

Por eso se adoptó el método de media geométrica, que evalúa cada bloque con
la fórmula `score = √(% asistencia × ISN)` y castiga los extremos: ni el
bloque con muchos asistentes insatisfechos, ni el bloque con pocos asistentes
felices. Con este método la curva de score ya no es plana sino descendente,
reflejando un ranking real entre los 20 bloques evaluados.

## 2. ¿Cuál es el bloque horario que el algoritmo seleccionó como consenso definitivo?

El algoritmo seleccionó **`Jue_10-12` — Jueves de 10:00 a 12:00** como el
consenso definitivo de la sección, con un score de **47.14**.

Este bloque reúne 5 estudiantes que pueden asistir, de los cuales 4 lo tienen
como su horario preferido, logrando un ISN de 80%. Ningún otro bloque combina
un número alto de asistentes con un nivel tan elevado de satisfacción al mismo
tiempo. El bloque `Jue_12-14`, que el método original hubiera elegido, tiene
más asistentes (7) pero un ISN de apenas 42.9% — más de la mitad va sin
quererlo. El consenso definitivo no es el horario que más gente tolera, sino
el que más gente genuinamente quiere.
