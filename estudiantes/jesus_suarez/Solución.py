import base64
import json
import numpy as np
import matplotlib.pyplot as plt

# 1. CARGA DE DATOS
def cargar_estudiantes(ruta_archivo):
    estudiantes = []
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            for linea in f:
                token = linea.strip()
                if token:
                    data = json.loads(base64.b64decode(token).decode('utf-8'))
                    estudiantes.append(data)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
    return estudiantes

# 2. LÓGICA DE EVALUACIÓN
def evaluar_bloque(bloque, estudiantes, wf):
    u_total = 0.0
    pueden, quieren = 0, 0
    for est in estudiantes:
        peso = wf if est.get("f", False) else 1.0
        # Incluimos 'v' para el caso de Alveris
        lista_p = est.get("v_p", []) + est.get("v", [])
        lista_d = est.get("v_d", [])
        
        if bloque in lista_d:
            u_total += (1.5 * peso)
            pueden += 1; quieren += 1
        elif bloque in lista_p:
            u_total += (1.0 * peso)
            pueden += 1
        else:
            u_total -= (1.5 * peso)
            
    isn = (quieren / pueden * 100) if pueden > 0 else 0.0
    return u_total, isn

# 3. SIMULACIÓN
def ejecutar_simulacion(estudiantes):
    dias, horas = ["Lun", "Mar", "Mie", "Jue", "Vie"], ["08-10", "10-12", "12-14", "14-16"]
    bloques = [f"{d}_{h}" for d in dias for h in horas]
    wf_vals = np.linspace(1.0, 10.0, 50)
    
    u_hist, isn_hist = [], []
    
    for wf in wf_vals:
        mejor_u = -float('inf')
        mejor_isn = 0
        for b in bloques:
            u, isn = evaluar_bloque(b, estudiantes, wf)
            if u > mejor_u:
                mejor_u, mejor_isn = u, isn
        u_hist.append(mejor_u)
        isn_hist.append(mejor_isn)
    return wf_vals, u_hist, isn_hist

# 4. GRÁFICA PERSONALIZADA
def graficar(wf, u, isn):
    # Encontrar punto óptimo
    idx_optimo = np.argmax(u)
    wf_optimo = wf[idx_optimo]
    u_optimo = u[idx_optimo]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Eje Izquierdo: U total (Teal)
    color_teal = '#008080'
    ax1.set_xlabel('Peso del Estudiante Foráneo ($W_f$)', fontsize=12)
    ax1.set_ylabel('$U_{total}$', color=color_teal, fontsize=12, fontweight='bold')
    ax1.plot(wf, u, color=color_teal, linewidth=2.5, label='$U_{total}$')
    ax1.tick_params(axis='y', labelcolor=color_teal)
    ax1.grid(True, linestyle='--', alpha=0.5)

    # Marcador de punto óptimo
    ax1.axvline(x=wf_optimo, color='gray', linestyle='--', alpha=0.7)
    ax1.annotate(f'Óptimo: {wf_optimo:.1f}', 
                 xy=(wf_optimo, u_optimo), 
                 xytext=(wf_optimo + 0.5, u_optimo),
                 arrowprops=dict(facecolor='black', shrink=0.05))

    # Eje Derecho: ISN (DeepPink)
    ax2 = ax1.twinx()
    color_pink = '#C71585'
    ax2.set_ylabel('ISN (%)', color=color_pink, fontsize=12, fontweight='bold')
    ax2.plot(wf, isn, color=color_pink, linestyle=':', linewidth=2.5, label='ISN (%)')
    ax2.tick_params(axis='y', labelcolor=color_pink)
    ax2.set_ylim(0, 105)

    # Leyenda unificada
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='lower right')

    plt.title('Análisis de Consenso: $U_{total}$ vs ISN (%)', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('grafica_consenso.png', dpi=300)
    print(f"✅ Gráfica generada. Punto óptimo en Wf = {wf_optimo:.1f}")

# EJECUCIÓN
if __name__ == "__main__":
    estudiantes = cargar_estudiantes("tokens.txt")
    if estudiantes:
        wf, u, isn = ejecutar_simulacion(estudiantes)
        graficar(wf, u, isn)
