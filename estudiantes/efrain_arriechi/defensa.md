# defensa.md

1. ¿Por qué la curva de Satisfacción (ISN) **no** se queda completamente plana?

Al ejecutar la simulación con los datos reales de la sección, la curva del ISN 
experimenta un salto visible en lugar de mantenerse constante.
Esto ocurre porque en nuestra sección hay dos bloques de horarios los cuales compiten por ser el
ganador: `Jueves 12-14` y `Jueves 10-12` (este ultimo que toma ventaja por el peso del voto foraneo).

Cuando el algoritmo cambia de bloque ganador, también cambia el conjunto de
estudiantes que asisten y los que consiguen su preferencia, por lo que el numerador
y el denominador del ISN varían de golpe, produciendo el escalón que se observa
en la gráfica.

En resumen: el ISN es plano dentro de cada bloque ganador, pero da un salto
cada vez que el cambio de peso hace que el algoritmo prefiera un bloque diferente.
Si hubiera un único bloque dominante en toda la simulación (como es el caso teórico
ideal), la curva sí sería completamente horizontal.



2. Bloque horario seleccionado como consenso definitivo

El algoritmo eligió de manera consistente (en la mayor parte de la simulación) el
bloque:

Jueves de 10:00 a 12:00**

aumenta a partir de cierto punto en la simulación.
