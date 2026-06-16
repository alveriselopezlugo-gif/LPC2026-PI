Codigo
import base64
import json
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# 1. CARGA DE ESTUDIANTES DESDE ARCHIVO .TXT (TOKENS BASE64)
# ============================================================

def cargar_estudiantes_desde_archivo(ruta):
    estudiantes = []

    try:
        with open(ruta, "r", encoding="utf-8") as f:
            lineas = f.readlines()
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")
        return estudiantes

    for i, linea in enumerate(lineas, start=1):
        token = linea.strip()
        if not token:
            continue

        try:
            json_str = base64.b64decode(token).decode("utf-8")
            est_raw = json.loads(json_str)

            # Convertir formato viejo → formato interno
            tipo = "foraneo" if est_raw.get("f", False) else "local"

            bloques = []

            # Procesar bloques donde PUEDE
            for bp in est_raw.get("v_p", []):
                dia, hora = bp.split("_")
                bloques.append({"dia": dia, "hora": hora, "puede": True, "quiere": False})

            # Procesar bloques donde QUIERE
            for bd in est_raw.get("v_d", []):
                dia, hora = bd.split("_")
                encontrado = False
                for b in bloques:
                    if b["dia"] == dia and b["hora"] == hora:
                        b["quiere"] = True
                        encontrado = True
                        break
                if not encontrado:
                    bloques.append({"dia": dia, "hora": hora, "puede": False, "quiere": True})

            estudiante = {
                "tipo": tipo,
                "bloques": bloques
            }

            estudiantes.append(estudiante)

        except Exception as e:
            print(f"⚠ Advertencia: Token inválido en la línea {i}. Se omitirá.")
            print(e)

    return estudiantes


# ============================================================
# 2. DEFINICIÓN DE BLOQUES HORARIOS
# ============================================================

DIAS = ["Lun", "Mar", "Mie", "Jue", "Vie"]
HORAS = ["08-10", "10-12", "12-14", "14-16"]

def generar_lista_bloques():
    bloques = []
    for dia in DIAS:
        for hora in HORAS:
            bloques.append((dia, hora))
    return bloques


# ============================================================
# 3. CÁLCULO DE MÉTRICAS
# ============================================================

def calcular_metricas_bloque(estudiantes, bloque, wf):
    dia_obj, hora_obj = bloque

    utotal = 0.0
    total_pueden = 0
    total_quieren_y_pueden = 0

    for est in estudiantes:
        tipo = est.get("tipo", "local")
        peso = 1.0 if tipo == "local" else wf

        puntos_estudiante = 0.0
        registro_encontrado = False

        for b in est.get("bloques", []):
            if b.get("dia") == dia_obj and b.get("hora") == hora_obj:
                registro_encontrado = True
                puede = b.get("puede", False)
                quiere = b.get("quiere", False)

                if puede:
                    puntos_estudiante += 1.0
                    total_pueden += 1
                    if quiere:
                        puntos_estudiante += 0.5
                        total_quieren_y_pueden += 1
                else:
                    puntos_estudiante -= 1.5
                break

        if not registro_encontrado:
            puntos_estudiante -= 1.5

        utotal += puntos_estudiante * peso

    isn = (total_quieren_y_pueden / total_pueden * 100) if total_pueden > 0 else 0.0

    return utotal, isn


# ============================================================
# 4. SIMULACIÓN
# ============================================================

def simular(estudiantes, wf_min=1.0, wf_max=10.0, wf_step=0.1):
    bloques = generar_lista_bloques()

    pesos_wf = np.arange(wf_min, wf_max + 0.0001, wf_step)
    utotales_mejor_bloque = []
    isn_mejor_bloque = []
    mejores_bloques = []

    for wf in pesos_wf:
        mejor_utotal = None
        mejor_isn = None
        mejor_bloque = None

        for bloque in bloques:
            utotal, isn = calcular_metricas_bloque(estudiantes, bloque, wf)

            if (mejor_utotal is None) or (utotal > mejor_utotal):
                mejor_utotal = utotal
                mejor_isn = isn
                mejor_bloque = bloque

        utotales_mejor_bloque.append(mejor_utotal)
        isn_mejor_bloque.append(mejor_isn)
        mejores_bloques.append(mejor_bloque)

    return pesos_wf, utotales_mejor_bloque, isn_mejor_bloque, mejores_bloques


# ============================================================
# 5. GRÁFICA
# ============================================================

def graficar_resultados(pesos_wf, utotales, isn):
    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.set_xlabel('Peso del Foráneo (Wf)')
    ax1.set_ylabel('Bienestar General (Utotal)', color='blue')
    ax1.plot(pesos_wf, utotales, color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Índice de Satisfacción Neta (ISN %)', color='red')
    ax2.plot(pesos_wf, isn, color='red', linestyle='--', marker='o', markersize=3)
    ax2.tick_params(axis='y', labelcolor='red')

    plt.title('Impacto del Peso del Foráneo en Utotal e ISN')
    ax1.grid(True, linestyle=':', alpha=0.5)

    plt.tight_layout()
    plt.show()


# ============================================================
# 6. MAIN
# ============================================================

def main():
    print("=== CONFIGURACIÓN INICIAL ===")
    ruta = input("Ingresa la ruta del archivo con los tokens Base64: ").strip()

    estudiantes = cargar_estudiantes_desde_archivo(ruta)

    if not estudiantes:
        print("No se cargaron estudiantes. Terminando programa.")
        return

    pesos_wf, utotales, isn, mejores_bloques = simular(estudiantes)

    print("\n=== RESULTADOS PARCIALES ===")
    for wf, bloque, ut, is_nv in zip(pesos_wf[::10], mejores_bloques[::10], utotales[::10], isn[::10]):
        dia, hora = bloque
        print(f"Wf={wf:.1f} -> Mejor bloque: {dia} {hora}, Utotal={ut:.2f}, ISN={is_nv:.2f}%")

    graficar_resultados(pesos_wf, utotales, isn)


if __name__ == '__main__':
    main()
