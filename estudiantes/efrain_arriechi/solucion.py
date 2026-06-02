"""
Asignación 1: Optimización de Horarios y Consenso Colectivo
============================================================
Script que simula el impacto del peso del estudiante foráneo (Wf)
sobre la selección del mejor bloque horario de la sección.

Métricas calculadas por iteración:
  - Utotal : Bienestar General ponderado del bloque ganador
  - ISN    : Índice de Satisfacción Neta (% de asistentes felices)
"""

import base64
import json
import matplotlib
matplotlib.use('Agg')           # backend sin ventana (compatible con servidores)
import matplotlib.pyplot as plt
from collections import Counter

# ─── 1. DATOS: tokens Base64 de cada compañero ───────────────────────────────
tokens = [
    "eyJuIjogIlJlYmVjYSBCYXJyaW9zICIsICJmIjogZmFsc2UsICJ2X3AiOiBbIk1hcl8xMi0xNCJdLCAidl9kIjogWyJNYXJfMTItMTQiXX0=",
    "eyJuIjogIkx1Y2lhbm8gUGFsZW5jaWEgIiwgImYiOiBmYWxzZSwgInZfcCI6IFsiTHVuXzEyLTE0IiwgIkx1bl8xNC0xNiIsICJNYXJfMTItMTQiLCAiTWFyXzE0LTE2IiwgIkp1ZV8xMi0xNCJdLCAidl9kIjogWyJMdW5fMTItMTQiLCAiTHVuXzE0LTE2IiwgIk1hcl8wOC0xMCJdfQ==",
    "eyJuIjogIlNhbWFudGhhIFBhcnJhIiwgImYiOiB0cnVlLCAidl9wIjogWyJMdW5fMTAtMTIiLCAiSnVlXzA4LTEwIl0sICJ2X2QiOiBbIkx1bl8xMC0xMiJdfQ==",
    "eyJuIjogIkFuZHJcdTAwZTlzIE1lbmRvemEgIiwgImYiOiB0cnVlLCAidl9wIjogWyJNYXJfMTItMTQiXSwgInZfZCI6IFsiTWFyXzEwLTEyIl19",
    "eyJuIjogIkVsaWV6ZXIgVmVsYXNxdWV6IiwgImYiOiBmYWxzZSwgInZfcCI6IFsiTHVuXzA4LTEwIiwgIkx1bl8xMC0xMiIsICJMdW5fMTItMTQiLCAiTHVuXzE0LTE2IiwgIk1pZV8wOC0xMCIsICJNaWVfMTAtMTIiLCAiTWllXzEyLTE0IiwgIk1pZV8xNC0xNiIsICJWaWVfMDgtMTAiLCAiVmllXzEwLTEyIiwgIlZpZV8xMi0xNCIsICJWaWVfMTQtMTYiXSwgInZfZCI6IFsiTWFyXzA4LTEwIiwgIk1hcl8xMC0xMiIsICJNYXJfMTItMTQiLCAiTWFyXzE0LTE2IiwgIkp1ZV8wOC0xMCIsICJKdWVfMTAtMTIiLCAiSnVlXzEyLTE0IiwgIkp1ZV8xNC0xNiJdfQ==",
    "eyJuIjogIllhcmlhbmEgT3JvemNvIiwgImYiOiBmYWxzZSwgInZfcCI6IFsiTHVuXzEyLTE0IiwgIkp1ZV8xMC0xMiJdLCAidl9kIjogWyJMdW5fMTItMTQiLCAiSnVlXzEyLTE0Il19",
    "eyJuIjogIkRlbmljZSBWaWxjaGV6ICIsICJmIjogdHJ1ZSwgInZfcCI6IFsiSnVlXzEwLTEyIl0sICJ2X2QiOiBbIkp1ZV8xMC0xMiJdfQ==",
    "eyJuIjogIkZyYW5jbyBKYWltZXMiLCAiZiI6IGZhbHNlLCAidl9wIjogWyJNYXJfMDgtMTAiLCAiTWFyXzEwLTEyIiwgIk1hcl8xMi0xNCIsICJNYXJfMTQtMTYiLCAiSnVlXzEyLTE0IiwgIlZpZV8wOC0xMCJdLCAidl9kIjogWyJNYXJfMTAtMTIiLCAiTWFyXzEyLTE0IiwgIk1hcl8xNC0xNiIsICJKdWVfMTItMTQiXX0=",
    "eyJuIjogIlphcmFoIEFsdmFyYWRvIiwgImYiOiBmYWxzZSwgInZfcCI6IFsiTWllXzE0LTE2IiwgIkp1ZV8xMC0xMiJdLCAidl9kIjogWyJNaWVfMTQtMTYiLCAiSnVlXzEwLTEyIl19",
    "eyJuIjogIkNlYnJpXHUwMGUxbiBJcmlhcnRlIiwgImYiOiBmYWxzZSwgInZfcCI6IFsiTWFyXzEyLTE0IiwgIk1hcl8xNC0xNiIsICJKdWVfMDgtMTAiLCAiSnVlXzEwLTEyIiwgIlZpZV8wOC0xMCIsICJWaWVfMTAtMTIiLCAiVmllXzEyLTE0IiwgIlZpZV8xNC0xNiJdLCAidl9kIjogWyJNYXJfMTQtMTYiLCAiSnVlXzA4LTEwIiwgIlZpZV8wOC0xMCJdfQ==",
    "eyJuIjogIlJvaW5lciBSb3NhcmlvICIsICJmIjogdHJ1ZSwgInZfcCI6IFsiTHVuXzEyLTE0IiwgIk1hcl8xMi0xNCJdLCAidl9kIjogW119",
    "eyJuIjogIk1hdXJvIE1lbGVhbiAiLCAiZiI6IGZhbHNlLCAidl9wIjogWyJNYXJfMDgtMTAiLCAiTWFyXzEwLTEyIiwgIk1pZV8xMC0xMiIsICJNaWVfMTItMTQiXSwgInZfZCI6IFsiTWllXzEwLTEyIiwgIk1pZV8xMi0xNCJdfQ==",
    "eyJuIjogIkplc1x1MDBmYXMgU3VcdTAwZTFyZXoiLCAiZiI6IGZhbHNlLCAidl9wIjogWyJMdW5fMTAtMTIiLCAiTHVuXzEyLTE0IiwgIk1hcl8wOC0xMCIsICJNYXJfMTAtMTIiLCAiTWFyXzEyLTE0IiwgIk1pZV8xMi0xNCIsICJKdWVfMTAtMTIiLCAiSnVlXzEyLTE0Il0sICJ2X2QiOiBbIkx1bl8xMC0xMiIsICJMdW5fMTItMTQiLCAiTWFyXzA4LTEwIiwgIk1hcl8xMC0xMiIsICJNYXJfMTItMTQiLCAiSnVlXzEwLTEyIiwgIkp1ZV8xMi0xNCJdfQ==",
    "eyJuIjogIkVmcmFpbiBBcnJpZWNoZSIsICJmIjogZmFsc2UsICJ2X3AiOiBbIkx1bl8xMC0xMiIsICJMdW5fMTItMTQiLCAiTHVuXzE0LTE2IiwgIk1hcl8wOC0xMCIsICJNYXJfMTAtMTIiLCAiTWFyXzEyLTE0IiwgIk1hcl8xNC0xNiIsICJKdWVfMTAtMTIiLCAiSnVlXzEyLTE0IiwgIkp1ZV8xNC0xNiJdLCAidl9kIjogWyJMdW5fMTAtMTIiLCAiSnVlXzEwLTEyIl19",
    "eyJuIjogIlJlYmVjYSBIZXJuYW5kZXogIiwgImYiOiBmYWxzZSwgInZfcCI6IFsiTWFyXzEyLTE0IiwgIkp1ZV8xMi0xNCJdLCAidl9kIjogWyJNYXJfMDgtMTAiLCAiSnVlXzEyLTE0Il19",
    "eyJuIjogIkFsdmVyaXMgRWRtdW5kbyBMXHUwMGYzcGV6IGx1Z28gIiwgImYiOiBmYWxzZSwgInYiOiBbIkx1bl8xMi0xNCIsICJNYXJfMTItMTQiLCAiTWllXzEyLTE0IiwgIkp1ZV8xMi0xNCIsICJWaWVfMTItMTQiXX0=",
    "eyJuIjogIkp1YW4gUmFtaXJleiAiLCAiZiI6IGZhbHNlLCAidl9wIjogWyJMdW5fMTItMTQiLCAiTWFyXzA4LTEwIl0sICJ2X2QiOiBbIk1pZV8xMi0xNCIsICJKdWVfMTItMTQiLCAiVmllXzEyLTE0Il19",
    "eyJuIjogIk1pcmFuZGEgTW9udGVybyAiLCAiZiI6IGZhbHNlLCAidl9wIjogWyJNYXJfMTAtMTIiLCAiTWllXzEwLTEyIiwgIkp1ZV8xMC0xMiIsICJWaWVfMTAtMTIiLCAiVmllXzEyLTE0Il0sICJ2X2QiOiBbIk1hcl8xMC0xMiIsICJNYXJfMTItMTQiLCAiTWllXzEwLTEyIiwgIlZpZV8xMC0xMiIsICJWaWVfMTItMTQiXX0="
]

# ─── 2. DECODIFICACIÓN SEGURA ─────────────────────────────────────────────────
estudiantes = []
for i, t in enumerate(tokens):
    try:
        data = json.loads(base64.b64decode(t).decode('utf-8'))
        # Normalizar: algunos tokens usan "v" en lugar de "v_d"
        if "v_d" not in data and "v" in data:
            data["v_d"] = data["v"]
        if "v_p" not in data:
            data["v_p"] = []
        if "v_d" not in data:
            data["v_d"] = []
        estudiantes.append(data)
    except Exception as e:
        print(f"[AVISO] Token {i} ignorado por error: {e}")

print(f"Estudiantes cargados correctamente: {len(estudiantes)}")

# ─── 3. BLOQUES HORARIOS ──────────────────────────────────────────────────────
dias  = ["Lun", "Mar", "Mie", "Jue", "Vie"]
horas = ["08-10", "10-12", "12-14", "14-16"]
bloques = [f"{d}_{h}" for d in dias for h in horas]

# ─── 4. SIMULACIÓN: Wf de 1.0 a 10.0 en pasos de 0.1 ────────────────────────
pesos   = [round(w / 10, 1) for w in range(10, 101)]
utilidad_max          = []
isn_max               = []
bloque_ganador_hist   = []

for wf in pesos:
    mejor_utotal  = -float('inf')
    mejor_bloque  = None
    mejor_isn     = 0.0

    for bloque in bloques:
        utotal    = 0.0
        asistentes = 0
        felices    = 0

        for est in estudiantes:
            v_d        = est.get("v_d", [])
            v_p        = est.get("v_p", [])
            es_foraneo = est.get("f", False)
            peso       = wf if es_foraneo else 1.0

            if bloque in v_d:               # puede asistir
                if bloque in v_p:           # además lo prefiere
                    puntos   = 1.5
                    felices += 1
                else:
                    puntos = 1.0
                asistentes += 1
            else:                           # no puede → penalización
                puntos = -1.5

            utotal += puntos * peso

        # ¿Es el mejor bloque de esta iteración?
        if utotal > mejor_utotal:
            mejor_utotal = utotal
            mejor_bloque = bloque
            mejor_isn    = (felices / asistentes * 100) if asistentes > 0 else 0.0

    utilidad_max.append(mejor_utotal)
    isn_max.append(mejor_isn)
    bloque_ganador_hist.append(mejor_bloque)

# Consenso definitivo = bloque que más veces resultó ganador
consenso = Counter(bloque_ganador_hist).most_common(1)[0][0]
print(f"Bloque consenso definitivo: {consenso}")
print(f"Rango Utotal : {min(utilidad_max):.2f}  →  {max(utilidad_max):.2f}")
print(f"Rango ISN    : {min(isn_max):.1f}%  →  {max(isn_max):.1f}%")

# ─── 5. GRÁFICA BIFOCAL ───────────────────────────────────────────────────────
fig, ax1 = plt.subplots(figsize=(11, 6))
fig.patch.set_facecolor('#f8f9fa')
ax1.set_facecolor('#f8f9fa')

# Eje izquierdo – Utotal (línea continua índigo)
color_util = 'indigo'
ax1.set_xlabel('Peso del Foráneo (Wf)', fontsize=12)
ax1.set_ylabel('Bienestar General (Utotal)', color=color_util, fontsize=12)
line1, = ax1.plot(pesos, utilidad_max, color=color_util, linewidth=2.5,
                  label='Utotal (máximo)')
ax1.tick_params(axis='y', labelcolor=color_util)
ax1.grid(True, linestyle='--', alpha=0.4)

# Eje derecho – ISN (línea punteada naranja)
ax2 = ax1.twinx()
color_isn = 'darkorange'
ax2.set_ylabel('Índice de Satisfacción Neta – ISN (%)', color=color_isn, fontsize=12)
line2, = ax2.plot(pesos, isn_max, color=color_isn, linestyle='--', linewidth=2.5,
                  label='ISN (%)')
ax2.tick_params(axis='y', labelcolor=color_isn)
ax2.set_ylim(0, 100)

# Leyenda unificada abajo a la derecha
ax1.legend([line1, line2], ['Utotal (máximo)', 'ISN (%)'],
           loc='lower right', fontsize=10, framealpha=0.9)

plt.title(
    f'Optimización de Horarios: Utotal e ISN vs Peso Foráneo\n'
    f'Consenso definitivo → {consenso}',
    fontsize=13, fontweight='bold'
)
plt.tight_layout()
plt.savefig('grafica_consenso.png', dpi=150)
print("Imagen guardada: grafica_consenso.png")
