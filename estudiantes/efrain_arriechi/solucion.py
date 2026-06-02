"""
Asignación 1: Optimización de Horarios y Consenso Colectivo
============================================================
Método de consenso: Media Geométrica (asistencia × satisfacción)
Selecciona el bloque que mejor equilibra cuántos pueden asistir
y cuántos quedan felices con ese horario, sin pesos políticos.
"""

import base64
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

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
    "eyJuIjogIkplc1x1MDBmYXMgU3VcdTAwZTFyZXoiLCAiZiI6IGZhbHNlLCAidl9wIjogWyJMdW5fMTAtMTIiLCAiTHVuXzEyLTE0IiwgIk1hcl8wOC0xMCIsICJNYXJfMTAtMTIiLCAiTWFyXzEyLTE0IiwgIk1pZV8xMiIsICJKdWVfMTAtMTIiLCAiSnVlXzEyLTE0Il0sICJ2X2QiOiBbIkx1bl8xMC0xMiIsICJMdW5fMTItMTQiLCAiTWFyXzA4LTEwIiwgIk1hcl8xMC0xMiIsICJNYXJfMTItMTQiLCAiSnVlXzEwLTEyIiwgIkp1ZV8xMi0xNCJdfQ==",
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
        if "v_d" not in data and "v" in data:
            data["v_d"] = data["v"]
        if "v_p" not in data:
            data["v_p"] = []
        if "v_d" not in data:
            data["v_d"] = []
        estudiantes.append(data)
    except Exception as e:
        print(f"[AVISO] Token {i} ignorado: {e}")

N = len(estudiantes)
print(f"Estudiantes cargados: {N}")

# ─── 3. BLOQUES HORARIOS ──────────────────────────────────────────────────────
dias  = ["Lun", "Mar", "Mie", "Jue", "Vie"]
horas = ["08-10", "10-12", "12-14", "14-16"]
bloques = [f"{d}_{h}" for d in dias for h in horas]

# ─── 4. CÁLCULO DEL SCORE POR BLOQUE ─────────────────────────────────────────
# Método: Media Geométrica entre % de asistencia e ISN
# score = sqrt(pct_asistencia * ISN)
# Penaliza los extremos: no sirve tener 100% ISN con 1 asistente,
# ni 18 asistentes con 0% de satisfacción.

resultados = []
for bloque in bloques:
    asistentes, felices = 0, 0
    for est in estudiantes:
        if bloque in est.get("v_d", []):
            asistentes += 1
            if bloque in est.get("v_p", []):
                felices += 1

    isn            = (felices / asistentes * 100) if asistentes > 0 else 0.0
    pct_asistencia = asistentes / N * 100
    score          = (pct_asistencia * isn) ** 0.5   # media geométrica

    resultados.append({
        "bloque":     bloque,
        "asistentes": asistentes,
        "felices":    felices,
        "isn":        round(isn, 1),
        "excluidos":  N - asistentes,
        "score":      round(score, 2),
    })

resultados.sort(key=lambda x: x["score"], reverse=True)
consenso = resultados[0]["bloque"]

print(f"\n{'Bloque':<14} {'Asisten':>7} {'Felices':>8} {'ISN':>7} {'Excluidos':>10} {'Score':>7}")
print("-" * 58)
for r in resultados[:8]:
    print(f"{r['bloque']:<14} {r['asistentes']:>7} {r['felices']:>8} "
          f"{r['isn']:>6}% {r['excluidos']:>10} {r['score']:>7}")

print(f"\nConsenso definitivo: {consenso}  (score={resultados[0]['score']})")

# ─── 5. GRÁFICA ───────────────────────────────────────────────────────────────
top     = resultados[:8]
labels  = [r["bloque"]     for r in top]
asisten = [r["asistentes"] for r in top]
felices = [r["felices"]    for r in top]
scores  = [r["score"]      for r in top]

x = np.arange(len(labels))
w = 0.3

fig, ax1 = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor('#f8f9fa')
ax1.set_facecolor('#f8f9fa')

bars1 = ax1.bar(x - w/2, asisten, w, label='Pueden asistir',
                color='steelblue', alpha=0.85)
bars2 = ax1.bar(x + w/2, felices, w, label='Felices (Pueden + Quieren)',
                color='mediumseagreen', alpha=0.85)

ax1.set_ylabel('N° de estudiantes', fontsize=11)
ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=20, ha='right')
ax1.set_ylim(0, N + 1)
ax1.axhline(N, color='gray', linestyle=':', alpha=0.4,
            label=f'Total sección ({N})')
ax1.grid(axis='y', linestyle='--', alpha=0.4)

ax2 = ax1.twinx()
ax2.plot(x, scores, color='darkorange', marker='o', linewidth=2.5,
         linestyle='--', label='Score (media geométrica)')
ax2.set_ylabel('Score combinado', color='darkorange', fontsize=11)
ax2.tick_params(axis='y', labelcolor='darkorange')
ax2.set_ylim(0, 70)

# Resaltar bloque ganador
ax1.get_xticklabels()[0].set_fontweight('bold')
ax1.get_xticklabels()[0].set_color('indigo')
for b in [bars1[0], bars2[0]]:
    b.set_edgecolor('indigo')
    b.set_linewidth(2.5)

lines1, lbl1 = ax1.get_legend_handles_labels()
lines2, lbl2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, lbl1 + lbl2, loc='upper right',
           fontsize=9, framealpha=0.9)

plt.title(
    f'Consenso óptimo — Media Geométrica (asistencia × satisfacción)\n'
    f'Ganador → {consenso}  |  Score: {resultados[0]["score"]}',
    fontsize=13, fontweight='bold'
)
plt.tight_layout()
plt.savefig('grafica_consenso.png', dpi=150)
print("Imagen guardada: grafica_consenso.png")