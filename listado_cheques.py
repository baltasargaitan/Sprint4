import csv
from datetime import datetime


# Función para leer el archivo CSV y convertirlo a una lista de diccionarios
def leer_cheques_desde_csv(archivo_csv):
    cheques = []
    try:
        with open(archivo_csv, mode='r', newline='', encoding='utf-8') as archivo:
            lector_csv = csv.DictReader(archivo)
            for fila in lector_csv:
                cheque = {
                    'numero_cheque': fila['numero_cheque'],
                    'codigo_banco': int(fila['codigo_banco']),
                    'codigo_sucursal': int(fila['codigo_sucursal']),
                    'numero_cuenta_origen': fila['numero_cuenta_origen'],
                    'numero_cuenta_destino': fila['numero_cuenta_destino'],
                    'valor': float(fila['valor_cheque']),
                    'fecha_emision': datetime.strptime(fila['fecha_emision'], '%d%m%Y'),  # Convertir a datetime
                    'fecha_pago_cobro': float(fila['fecha_pago_cobro']),
                    'dni_cliente': fila['dni_cliente'],
                    'estado': fila['estado'],
                    'tipo_cheque': fila['tipo_cheque']
                }
                cheques.append(cheque)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo_csv}'.")
    return cheques


def corroborar_no_repeticion(cheques,dni):
    cheques_vistos = set()
    for cheque in cheques:
        if cheque['dni_cliente'] == dni:
            clave = (cheque['numero_cheque'],cheque['numero_cuenta_origen'])
            if clave in cheques_vistos:
                print(f"Error: El cheque número {cheque['numero_cheque']} ya existe para la cuenta "
                      f"{cheque['numero_cuenta_origen']} con el DNI {cheque['dni_cliente']}.")
            else:
                cheques_vistos.add(clave)


# Función para filtrar cheques según criterios dados
def filtrar_cheques(cheques, dni_cliente, tipo_cheque, estado=None, fecha_desde=None, fecha_hasta=None):
    cheques_filtrados = []
    for cheque in cheques:
        if cheque['dni_cliente'] != dni_cliente:
            continue
        if cheque['tipo_cheque'].lower() != tipo_cheque.lower():
            continue
        if estado and cheque['estado'].lower() != estado.lower():
            continue
        if fecha_desde and cheque['fecha_emision'] < fecha_desde:
            continue
        if fecha_hasta and cheque['fecha_emision'] > fecha_hasta:
            continue
        cheques_filtrados.append(cheque)

    corroborar_no_repeticion(cheques_filtrados,dni_cliente)
    return cheques_filtrados


# Función para imprimir los cheques filtrados
def imprimir_cheques(cheques, salida):
    if salida == "PANTALLA":
        for cheque in cheques:
            print(cheque)
    elif salida == "CSV":
        if not cheques:
            return print('No se ha creado la lista, ningun elemento coincide con los criterios. ')
        nombre_archivo = f"{cheques[0]['dni_cliente']}_{int(datetime.now().timestamp())}.csv"
        with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
            escritor_csv = csv.DictWriter(archivo, fieldnames=cheques[0].keys())
            escritor_csv.writeheader()
            escritor_csv.writerows(cheques)
        print(f"Cheques exportados a '{nombre_archivo}'.")


# Función principal
def filtrado(cheques):
    # Obtener argumentos desde la línea de comandos
    dni_cliente = input('Ingrese el DNI: ')      # DNI del cliente
    salida = input('Salida (PANTALLA o CSV): ').upper()          # Salida (PANTALLA o CSV)
    tipo_cheque = input('Tipo de cheque (EMITIDO o  DEPOSITADO): ').upper()       # Tipo de cheque
    estado = input('Estado (opcional): ')          # Estado del cheque (opcional)

    # Obtener fechas desde la entrada del usuario
    while True:
        fecha_desde_input = input('Ingrese la fecha desde (YYYY-MM-DD) (opcional, presione Enter para omitir): ')
        if not fecha_desde_input:
            fecha_desde = None
            break
        try:
            fecha_desde = datetime.strptime(fecha_desde_input, '%Y-%m-%d')
            break
        except ValueError:
            print("Formato de fecha inválido. Por favor, use YYYY-MM-DD.")

    while True:
        fecha_hasta_input = input('Ingrese la fecha hasta (YYYY-MM-DD) (opcional, presione Enter para omitir): ')
        if not fecha_hasta_input:
            fecha_hasta = None
            break
        try:
            fecha_hasta = datetime.strptime(fecha_hasta_input, '%Y-%m-%d')
            break
        except ValueError:
            print("Formato de fecha inválido. Por favor, use YYYY-MM-DD.")

    # Filtrar los cheques según los criterios dados
    cheques_filtrados = filtrar_cheques(cheques, dni_cliente, tipo_cheque, estado, fecha_desde, fecha_hasta)

    # Imprimir los cheques filtrados

    imprimir_cheques(cheques_filtrados, salida)


def mostrar_menu():
    print('---Menu---')
    print('Opción 1: Filtrar cheque')
    print('Opción 2: Corrobar que no se repitan numeros de cheque por DNI')
    print('Opción 3: Salir')
    print('----------')


def main():
    cheques = leer_cheques_desde_csv(input('Ingrese el archivo a leer (ejemplo: archivo.csv): '))
    if cheques:
        while True:
            mostrar_menu()
            opcion = input('Ingrese una opcion : ')
            if opcion == '1':
                filtrado(cheques)
            elif opcion == '2':
                dni_a_corroborar = input("Ingrese un DNI a corroborar: ")
                corroborar_no_repeticion(cheques, dni_a_corroborar)
            elif opcion == '3':
                return


if __name__ == '__main__':
    main()
