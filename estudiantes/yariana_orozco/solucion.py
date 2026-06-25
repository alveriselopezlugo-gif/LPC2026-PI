# --- CODIGO DE CONSENSO DE HORARIO v3.0 (Tu Estilo - Matriz de Vulnerabilidad) ---
import ipywidgets as widgets
from IPython.display import display, HTML
import base64
import json

# Configuración inicial de datos personales y socioeconómicos
nombre = widgets.Text(placeholder='Tu Nombre y Apellido', description='Nombre:')

procedencia = widgets.Dropdown(
    options=[
        ('Local (Vive en Maracaibo)', 1.0),
        ('Foráneo Cerca (San Francisco / La Cañada)', 1.2),
        ('Foráneo Medio (Cabimas / Costa Oriental)', 1.5),
        ('Foráneo Lejos (Fuera de la COL / Horas de viaje)', 2.0)
    ],
    description='Procedencia:',
    layout=widgets.Layout(width='450px')
)

residencia_maracaibo = widgets.Checkbox(
    description='¿Resides en Maracaibo de Lunes a Viernes?',
    value=False,
    layout=widgets.Layout(width='450px')
)

logistica_local = widgets.Dropdown(
    options=[
        ('Transporte propio / Sin complicaciones de traslado', 1.0),
        ('Dependo de transporte público largo o difícil', 1.3),
        ('Tengo horario laboral u obligaciones restrictivas', 1.5)
    ],
    description='Logística:',
    layout=widgets.Layout(width='450px')
)

output = widgets.Output()

print("🏛️ CONFIGURACION DE HORARIO v3.0 (Optimización Equitativa)")
print("Por favor, llena tus datos socio-geográficos primero.")
print("-" * 60)
display(nombre, procedencia, residencia_maracaibo, logistica_local)
print("-" * 60)
print("Indica los bloques donde PUEDES asistir y marca con DESEO tu horario ideal:")

# Definición de la matriz de horarios
dias = ["Lun", "Mar", "Mie", "Jue", "Vie"]
bloques = ["08-10", "10-12", "12-14", "14-16"]
checks = {}

# Generamos la interfaz de horarios integrada
for d in dias:
    print(f"\n--- {d} ---")
    for b in bloques:
        # Creamos los dos checkboxes por cada bloque horario
        c_puedo = widgets.Checkbox(description="Puedo", indent=False)
        c_deseo = widgets.Checkbox(description="Deseo", indent=False)

        # Los guardamos en el diccionario para recuperarlos luego en la función
        checks[f"{d}_{b}_puedo"] = c_puedo
        checks[f"{d}_{b}_deseo"] = c_deseo

        # Mostramos la etiqueta del bloque y los dos checks alineados horizontalmente
        etiqueta = widgets.Label(value=f"{b}:", layout=widgets.Layout(width='60px'))
        display(widgets.HBox([etiqueta, c_puedo, c_deseo]))

# Función para compilar los datos y generar el token Base64
def generar_voto(b):
    # Recuperamos las listas de lo marcado por el estudiante
    puedo = [k.replace("_puedo", "") for k, v in checks.items() if "_puedo" in k and v.value]
    deseo = [k.replace("_deseo", "") for k, v in checks.items() if "_deseo" in k and v.value]

    if not nombre.value or not puedo:
        with output:
            output.clear_output()
            print("❌ Error: Debes poner tu nombre y marcar al menos una disponibilidad (Puedo).")
        return

    # Estructura de datos avanzada que se enviará al script de optimización
    data = {
        "n": nombre.value,
        "proc_w": procedencia.value,         # Multiplicador por distancia geográfica
        "res_m": residencia_maracaibo.value, # Ponderador si ya alquila en Maracaibo
        "socio_w": logistica_local.value,    # Multiplicador por dificultad económica/laboral
        "v_p": puedo,                        # Lista de bloques donde PUEDE
        "v_d": deseo                         # Lista de bloques donde DESEA
    }

    # Codificación segura a Base64
    token = base64.b64encode(json.dumps(data).encode()).decode()

    with output:
        output.clear_output()
        print("\n✅ ¡VOTO PERSONALIZADO GENERADO CON ÉXITO!")
        print("Copia y pega TODO este código en el grupo de WhatsApp:")
        print("-" * 65)
        print(token)
        print("-" * 65)

# Botón de acción para procesar el formulario
print("\n")
btn = widgets.Button(description="GENERAR CÓDIGO V3.0", button_style='success', layout=widgets.Layout(width='200px'))
btn.on_click(generar_voto)
display(btn, output)
