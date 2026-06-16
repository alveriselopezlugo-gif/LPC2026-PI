import base64
import json
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# 1. Lista interna de tokens de la sección en Base64
# ============================================================
tokens_base64 = [
    "eyJuIjogIlJlYmVjYSBCYXJyaW9zICIsICJmIjogZmFsc2UsICJ2X3AiOiBbIk1hcl8xMi0xNCJdLCAidl9kIjogWyJNYXJfMTItMTQiXX0=",
    "eyJuIjogIkx1Y2lhbm8gUGFsZW5jaWEgIiwgImYiOiBmYWxzZSwgInZfcCI6IFsiTHVuXzEyLTE0IiwgIkx1bl8xNC0xNiIsICJNYXJfMTItMTQiLCAiTWFyXzE0LTE2IiwgIkp1ZV8xMi0xNCJdLCAidl9kIjogWyJMdW5fMTItMTQiLCAiTHVuXzE0LTE2IiwgIk1hcl8wOC0xMCJdfQ==",
    "eyJuIjogIlNhbWFudGhhIFBhcnJhIiwgImYiOiB0cnVlLCAidl9wIjogWyJMdW5fMTAtMTIiLCAiSnVlXzA4LTEwIl0sICJ2X2QiOiBbIkx1bl8xMC0xMiJdfQ==",
    "eyJuIjogIkFuZHJcdTAwZTlzIE1lbmRvemEgIiwgImYiOiB0cnVlLCAidl9wIjogWyJNYXJfMTItMTQiXSwgInZfZCI6IFsiTWFyXzEwLTEyIl19",
    "eyJuIjogIkVsaWV6ZXIgVmVsYXNxdWV6IiwgImYiOiBmYWxzZSwgInZfcCI6IFsiTHVuXzA4LTEwIiwgIkx1bl8xMC0xMiIsICJMdW5fMTItMTQiLCAiTHVuXzE0LTE2IiwgIk1pZV8wOC0xMCIsICJNaWVfMTAtMTIiLCAiTWllXzEyLTE0IiwgIk1pZV8xNC0xNiIsICJWaWVfMDgtMTAiLCAiVmllXzEwLTEyIiwgIlZpZV8xMi0xNCIsICJWaWVfMTQtMTYiXSwgInZfZCI6IFsiTWFyXzA4LTEwIiwgIk1hcl8xMC0xMiIsICJNYXJfMTItMTQiLCAiTWFyXzE0LTE2IiwgIkp1ZV8wOC0xMCIsICJKdWVfMTAtMTIiLCAiSnVlXzEyLTE0IiwgIkp1ZV8xNC0xNiJdfQ==",
    "eyJuIjogIllhcmlhbmEgT3JvemNvIiwgImYiOiBmYWxzZSwgInZfcCI6IFsiTHVuXzEyLTE0IiwgIkp1ZV8xMC0xMiJdLCAidl9kIjogWyJMdW5fMTAtMTIiLCAiSnVlXzEyLTE0Il19",
    "eyJuIjogIkRlbmljZSBWaWxjaGV6ICIsICJmIjogdHJ1ZSwgInZfcCI6IFsiSnVlXzEwLTEyIl0sICJ2X2QiOiBbIkp1ZV8xMC0xMiJdfQ==",
    "eyJuIjogIkZyYW5jbyBKYWltZXMiLCAiZiI6IGZhbHNlLCAidl9wIjogWyJNYXJfMDgtMTAiLCAiTWFyXzEwLTEyIiwgIk1hcl8xMi0xNCIsICJNYXJfMTQtMTYiLCAiSnVlXzEyLTE0IiwgIlZpZV8wOC0xMCJdLCAidl9kIjogWyJNYXJfMTAtMTIiLCAiTWFyXzEyLTE0IiwgIk1hcl8xNC0xNiIsICJKdWVfMTAtMTQiXX0=",
    "eyJuIjogIlphcmFoIEFsdmFyYWRvIiwgImYiOiBmYWxzZSwgInZfcCI6IFsiTWllXzE0LTE2IiwgIkp1ZV8xMC0xMiJdLCAidl9kIjogWyJNaWVfMTQtMTYiLCAiSnVlXzEwLTEyIl19",
    "eyJuIjogIkNlYnJpXHUwMGUxbiBJcmlhcnRlIiwgImYiOiBmYWxzZSwgInZfcCI6IFsiTWFyXzEyLTE0IiwgIk1hcl8xNC0xNiIsICJKdWVfMDgtMTAiLCAiSnVlXzEwLTEyIiwgIlZpZV8wOC0xMCIsICJWaWVfMTAtMTIiLCAiVmllXzEyLTE0IiwgIlZpZV8xNC0xNiJdLCAidl9kIjogWyJNYXJfMTQtMTYiLCAiSnVlXzA4LTEwIiwgIlZpZV8wOC0xMCJdfQ==",
    "eyJuIjogIlJvaW5lciBSb3NhcmlvICIsICJmIjogdHJ1ZSwgInZfcCI6IFsiTHVuXzEyLTE0IiwgIk1hcl8xMi0xNCJdLCAidl9kIjogW119",
    "eyJuIjogIk1hdXJvIE1lbGVhbiAiLCAiZiI6IGZhbHNlLCAidl9wIjogWyJNYXJfMDgtMTAiLCAiTWFyXzEwLTEyIiwgIk1pZV8xMC0xMiIsICJNaWVfMTAtMTQiXSwgInZfZCI6IFsiTWllXzEwLTEyIiwgIk1pZV8xMi0xNCJdfQ==",
    "eyJuIjogIkJlc1x1MDBmYXMgU3VcdTAwZTFyZXoiLCAiZiI6IGZhbHNlLCAidl9wIjogWyJMdW5fMTAtMTIiLCAiTHVuXzEyLTE0IiwgIk1hcl8wOC0xMCIsICJNYXJfMTAtMTIiLCAiTWFyXzEyLTE0IiwgIk1pZV8xMi0xNCIsICJKdWVfMTAtMTIiLCAiSnVlXzEyLTE0Il0sICJ2X2QiOiBbIkx1bl8xMC0xMiIsICJMdW5fMTItMTQiLCAiTWFyXzA4LTEwIiwgIk1hcl8xMC0xMiIsICJNYXJfMTItMTQiLCAiSnVlXzEwLTEyIiwgIkp1ZV8xMi0xNCJdfQ==",
    "eyJuIjogIkVmcmFpbiBBcnJpZWNoZSIsICJmIjogZmFsc2UsICJ2X3AiOiBbIkx1bl8xMC0xMiIsICJMdW5fMTItMTQiLCAiTHVuXzE0LTE2IiwgIk1hcl8wOC0xMCIsICJNYXJfMTAtMTIiLCAiTWFyXzEyLTE0IiwgIk1hcl8xNC0xNiIsICJKdWVfMTAtMTIiLCAiSnVlXzEyLTE0IiwgIkp1ZV8xNC0xNiJdLCAidl9kIjogWyJMdW5fMTAtMTIiLCAiSnVlXzEwLTEyIl19",
    "eyJuIjogIlJlYmVjYSBIZXJuYW5kZXogIiwgImYiOiBmYWxzZSwgInZfcCI6IFsiTWFyXzEyLTE0IiwgIkp1ZV8xMi0xNCJdLCAidl9kIjogWyJNYXJfMDgtMTAiLCAiSnVlXzEyLTE0Il19",
    "eyJuIjogIkFsdmVyaXMgRWRtdW5kbyBMXHUwMGYzcGV6IGx1Z28gIiwgImYiOiBmYWxzZSwgInYiOiBbIkx1bl8xMi0xNCIsICJNYXJfMTItMTQiLCAiTWllXzEyLTE0IiwgIkp1ZV8xMi0xNCIsICJWaWVfMTAtMTIiXX0=",
    "eyJuIjogIkp1YW4gUmFtaXJleiAiLCAiZiI6IGZhbHNlLCAidl9wIjogWyJMdW5fMTAtMTIiLCAiTWFyXzA4LTEwIl0sICJ2X2QiOiBbIk1pZV8xMi0xNCIsICJKdWVfMTAtMTQiLCAiVmllXzEyLTE0Il19",
    "eyJuIjogIk1pcmFuZGEgTW9udGVybyAiLCAiZiI6IGZhbHNlLCAidl9wIjogWyJNYXJfMTAtMTIiLCAiTWllXzEwLTEyIiwgIkp1ZV8xMC0xMiIsICJWaWVfMTAtMTIiLCAiVmllXzEyLTE0Il0sICJ2X2QiOiBbIk1pcl8xMC0xMiIsICJNYXJfMTItMTQiLCAiTWllXzEwLTEyIiwgIlZpZV8xMC0xMiIsICJNYXJfMTItMTQiXX0="
]

# ============================================================
# 2. Decodificación y Normalización de datos reales
# ============================================================
estudiantes = []

for i, token in enumerate(tokens_base64, 1):
    try:
        json_bytes = base64.b64decode(token.strip(), validate=True)
        json_str = json_bytes.decode("utf-8")
        datos = json.loads(json_str)

        datos["tipo"] = "Foráneo" if datos.get("f", False) else "Local"
        
        if "v" in datos and "v_p" not in datos:
            datos["v_p"] = datos["v"]
            
        if "v_p" not in datos: datos["v_p"] = []
        if "v_d" not in datos: datos["v_d"] = []

        estudiantes.append(datos)

    except Exception as e:
        print(f"Error procesando el token {i}: {e}. Se omite.")

if not estudiantes:
    print("Error crítico: No se cargó ningún estudiante válido.")
    exit()

# ============================================================
# 3. Mapeo del Universo de Bloques Horarios
# ============================================================
dias_token = ["Lun", "Mar", "Mie", "Jue", "Vie"]
dias_pantalla = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
horas = ["08-10", "10-12", "12-14", "14-16"]

bloques = []
for dt, dp in zip(dias_token, dias_pantalla):
    for h in horas:
        bloques.append({"codigo": f"{dt}_{h}", "pantalla": f"{dp} {h}"})

# ============================================================
# 4. Evaluación focalizada en Wf = 2.00 (Mantenimiento de Línea)
# ============================================================
# Generamos un entorno cerrado alrededor de 2.00 para permitir el trazado continuo solicitado
wf_valores = np.array([1.9, 2.0, 2.1])  
utilidad_optima = []
satisfaccion_optima = []

print("Evaluando el bloque con los pesos asignados...")
for wf in wf_valores:
    mejor_utilidad = -float("inf")
    stats_ganador = (0, 0)

    for blq in bloques:
        codigo = blq["codigo"]
        utilidad_total = 0.0
        num_pueden = 0
        num_quieren = 0

        for est in estudiantes:
            puedo = codigo in est["v_p"]
            quiero = codigo in est["v_d"]

            # Asignación estricta de pesos
            peso = wf if est["tipo"] == "Foráneo" else 1.00

            if puedo:
                puntos = 1.5 if quiero else 1.0
                num_pueden += 1
                if quiero:
                    num_quieren += 1
            else:
                puntos = -1.5
                
            utilidad_total += puntos * peso

        if utilidad_total > mejor_utilidad:
            mejor_utilidad = utilidad_total
            stats_ganador = (num_pueden, num_quieren)

    num_pueden, num_quieren = stats_ganador
    isn_final = (num_quieren / num_pueden * 100.0) if num_pueden > 0 else 0.0

    utilidad_optima.append(mejor_utilidad)
    satisfaccion_optima.append(isn_final)

# Extraer métricas exactas del punto central solicitado (Wf = 2.00)
u_fina = utilidad_optima[1]
isn_fina = satisfaccion_optima[1]

print("\n" + "="*50)
print(f"RESULTADOS DE LA EVALUACIÓN (Local = 1.00 | Wf = 2.00)")
print("="*50)
print(f"📊 Bienestar General (U_total): {u_fina:.2f}")
print(f"🎯 Índice de Satisfacción Neta (ISN): {isn_fina:.1f}%")
print("="*50)

# ============================================================
# 5. Generación de Gráfica Bifocal (Mismo Tipo de Gráfica Pedido)
# ============================================================
fig, ax1 = plt.subplots(figsize=(10, 6))

# Eje X: Focalizado estrictamente en Wf = 2.00 con un margen estético limpio
ax1.set_xlabel("Peso del Estudiante Foráneo (Wf)", fontsize=12)
ax1.set_xlim(1.8, 2.2)
ax1.set_xticks([2.00])
ax1.set_xticklabels(["Local: 1.00\nForáneo (Wf): 2.00"], fontsize=11)

# Eje Y Izquierdo: Bienestar General (U_total) -> Curva continua e indicador circular
color_util = "indigo"
ax1.set_ylabel("Bienestar General (U_total)", color=color_util, fontsize=12)
line1 = ax1.plot(wf_valores, utilidad_optima, color=color_util, linestyle="-", linewidth=2.5,
                 label=f"U_total (Continua: {u_fina:.2f})")
ax1.plot(2.00, u_fina, color=color_util, marker='o', markersize=10) # Punto de destaque
ax1.tick_params(axis="y", labelcolor=color_util)
ax1.grid(True, linestyle="--", alpha=0.5)

# Eje Y Derecho: Satisfacción (ISN) -> Línea discontinua punteada e indicador cuadrado
ax2 = ax1.twinx()
color_sat = "darkorange"
ax2.set_ylabel("Porcentaje de Satisfacción (ISN) [%]", color=color_sat, fontsize=12)
line2 = ax2.plot(wf_valores, satisfaccion_optima, color=color_sat, linestyle=":", linewidth=2.5,
                 label=f"ISN (Punteada: {isn_fina:.1f}%)")
ax2.plot(2.00, isn_fina, color=color_sat, marker='s', markersize=10) # Punto de destaque
ax2.tick_params(axis="y", labelcolor=color_sat)
ax2.set_ylim(0, 105)

# Construcción de la leyenda unificada sin alterar el layout anterior
lineas = line1 + line2
etiquetas = [l.get_label() for l in lineas]
ax1.legend(lineas, etiquetas, loc="lower right", framealpha=0.95)

plt.title("Consenso Horario Decidido (Doble Eje Y)", fontsize=13, fontweight='bold', pad=12)
fig.tight_layout()

# Guardar y desplegar
plt.savefig("grafica_consenso.png", dpi=150)
plt.show()

print("\n✅ Script y gráfica actualizados. Tipo de gráfica doble eje Y preservado.")