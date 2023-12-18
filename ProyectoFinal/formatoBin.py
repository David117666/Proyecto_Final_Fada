def cadena_bits_a_bytes(cadena_bits):
    # Asegurar que la longitud de la cadena sea múltiplo de 8
    cadena_bits = cadena_bits + '0' * (8 - len(cadena_bits) % 8) 
    # Convertir la cadena de bits a bytes
    bytes_datos = bytes(int(cadena_bits[i:i+8], 2) for i in range(0, len(cadena_bits), 8))
    return bytes_datos

def guardar_en_binario(cadena_bits, nombre_archivo):
    bytes_datos = cadena_bits_a_bytes(cadena_bits)

    # Escribir los datos en el archivo binario
    with open(nombre_archivo, 'wb') as archivo_binario:
        archivo_binario.write(bytes_datos)



#contador de caracteres para el archivo .txt
        
def contar_letras_y_caracteres(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()

            # Contar la cantidad total de caracteres, incluyendo espacios
            total_caracteres = len(contenido)

            # Contar la cantidad de letras (alfabéticas)
            letras = sum(c.isalpha() for c in contenido)

            return total_caracteres, letras

    except FileNotFoundError:
        print(f"El archivo {ruta_archivo} no fue encontrado.")
        return None

# Ejemplo de uso
archivo_txt = "evangelio_segun_marcos.txt"
total_caracteres, letras = contar_letras_y_caracteres(archivo_txt)

if total_caracteres is not None:
    print(f"El archivo {archivo_txt} contiene {total_caracteres} caracteres en total.")
    print(f"La cantidad de letras en el archivo es: {letras}.")
