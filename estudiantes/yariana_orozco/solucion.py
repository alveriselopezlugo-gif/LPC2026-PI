import base64
import json

def mostrar_menu_opciones(titulo, opciones):
    print(f"\n{titulo}")
    for idx, (texto, _) in enumerate(opciones, start=1):
        print(f"  {idx}. {texto}")
    
    while True:
        try:
            seleccion = int(input("👉 Selecciona una opción (número): "))
            if 1 <= seleccion <= len(opciones):
                return opciones[seleccion - 1][1]
            print(f"❌ Por favor, elige un número entre 1 y {len(opciones)}.")
        except ValueError:
            print("❌ Entrada inválida. Ingresa un número entero.")

def capturar_horarios():
    dias = ["Lun", "Mar", "Mie", "Jue", "Vie"]
    bloques = ["08-10", "10-12", "12-14", "14-16"]
    
    puedo = []
    deseo = []
    
    print("\n📅 CONFIGURACIÓN DE DISPONIBILIDAD HORARIA")
    print("Para cada bloque responde con:")
    print("  'P' si solo PUEDES asistir.")
    print("  'D' si además lo DESEAS (Tu horario ideal).")
    print("  Presiona ENTER o cualquier otra tecla si NO PUEDES.")
    print("-" * 50)
    
    for d in dias:
        print(f"\n--- {d.upper()} ---")
        for b in bloques:
            respuesta = input(f"  ¿{b}? [P / D / No]: ").strip().upper()
            
            identificador_bloque = f"{d}_{b}"
            if respuesta == 'P':
                puedo.append(identificador_bloque)
            elif respuesta == 'D':
                puedo.append(identificador_bloque)
                deseo.append(identificador_bloque)
                
    return puedo, deseo

def main():
    print("🏛️  CONFIGURACION DE HORARIO v3.0 (Optimización Equitativa)")
    print("Por favor, llena tus datos socio-geográficos primero.")
    print("=" * 60)
    
    # 1. Captura de Nombre
    nombre = ""
    while not nombre.strip():
        nombre = input("👤 Ingresa tu Nombre y Apellido: ").strip()
        if not nombre:
            print("❌ El nombre no puede estar vacío.")

    # 2. Opciones de Procedencia
    opciones_procedencia = [
        ('Local (Vive en Maracaibo)', 1.0),
        ('Foráneo Cerca (San Francisco / La Cañada)', 1.2),
        ('Foráneo Medio (Cabimas / Costa Oriental)', 1.5),
        ('Foráneo Lejos (Fuera de la COL / Horas de viaje)', 2.0)
    ]
    proc_w = mostrar_menu_opciones("📍 ¿Cuál es tu procedencia geográfica?", opciones_procedencia)

    # 3. Residencia Temporal
    res_m_input = input("\n🏠 ¿Resides en Maracaibo de Lunes a Viernes? (S/N): ").strip().lower()
    res_m = res_m_input in ['s', 'si', 'sí', 'y', 'yes']

    # 4. Opciones de Logística Local
    opciones_logistica = [
        ('Transporte propio / Sin complicaciones de traslado', 1.0),
        ('Dependo de transporte público largo o difícil', 1.3),
        ('Tengo horario laboral u obligaciones restrictivas', 1.5)
    ]
    socio_w = mostrar_menu_opciones("🚌 ¿Cómo evalúas tu logística o transporte diario?", opciones_logistica)

    # 5. Captura de la matriz de horarios
    puedo, deseo = capturar_horarios()

    # Validación de seguridad
    if not puedo:
        print("\n❌ Error crítico: Debes marcar al menos una disponibilidad ('P' o 'D') para procesar el voto.")
        return

    # Estructura de datos avanzada compatible con la matriz v3.0
    data = {
        "n": nombre,
        "proc_w": proc_w,
        "res_m": res_m,
        "socio_w": socio_w,
        "v_p": puedo,
        "v_d": deseo
    }

    # Codificación segura a Base64
    token = base64.b64encode(json.dumps(data).encode()).decode()

    # Salida final por pantalla
    print("\n" + "="*65)
    print("✅ ¡VOTO PERSONALIZADO GENERADO CON ÉXITO!")
    print("Copia y pega TODO el bloque de texto de abajo en el grupo de WhatsApp:")
    print("-" * 65)
    print(token)
    print("=" * 65)

if __name__ == "__main__":
    main()
