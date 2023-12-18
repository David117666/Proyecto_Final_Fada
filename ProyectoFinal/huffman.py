# Milton David Zapata Aguilera - 1866060 - 2711
# Julián Andrés Ibáñez - 1866221 - 2711
# 15/12/2023

# Importar las bibliotecas necesarias
import pickle
import networkx as nx
import matplotlib.pyplot as plt
import os
import leerArchiv
import formatoBin

#oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

#En este ejemplo se realizará con el archivo de texto llamado evangelio_segun_marcos.txt 
# Ejemplo de uso
ruta_del_archivo = "evangelio_segun_marcos.txt"
cadena = leerArchiv.leer_archivo_txt(ruta_del_archivo)
#cadena = 'Mi Pasion es programar'
#oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

# Crear la clase NodoArbol
class NodoArbol(object):
    def __init__(self, izquierda=None, derecha=None):
        self.izquierda = izquierda
        self.derecha = derecha

    def hijos(self):
        return (self.izquierda, self.derecha)

    def nodos(self):
        return (self.izquierda, self.derecha)

    def __str__(self):
        return '%s_%s' % (self.izquierda, self.derecha)

# Función principal que implementa la codificación de huffman
def arbol_codificacion_huffman(nodo, izquierda=True, binario=''):    # toma un nodo del árbol y genera un diccionario que representa la codificación binaria para cada símbolo en el árbol.
    if type(nodo) is str:             #Verifica si el tipo de nodo es una cadena. Si es así, significa que nodo es una hoja que contiene un símbolo.
        return {nodo: binario}     #Devuelve un diccionario con la clave siendo el símbolo representado por nodo y el valor siendo la cadena binaria acumulada hasta ese símbolo.
    (izq, der) = nodo.hijos()               #: Obtiene los hijos del nodo actual, asumiendo que el objeto nodo tiene un método llamado hijos que devuelve una tupla con los dos hijos.
    diccionario = dict()     #Crea un diccionario vacío para almacenar las codificaciones binarias.
    diccionario.update(arbol_codificacion_huffman(izq, True, binario + '0'))  # Recursivamente llama a la función arbol_codificacion_huffman para el hijo izquierdo (izq) del nodo actual. Agrega el resultado al diccionario actual con la cadena binaria acumulada aumentada por '0' para indicar que estamos yendo hacia la izquierda en el árbol.
    diccionario.update(arbol_codificacion_huffman(der, False, binario + '1'))  #Recursivamente llama a la función arbol_codificacion_huffman para el hijo derecho (der) del nodo actual. Agrega el resultado al diccionario actual con la cadena binaria acumulada aumentada por '1' para indicar que estamos yendo hacia la derecha en el árbol.
    return diccionario    #aaqui utilizamos como estructura de datos el diccionario


# Calculando la frecuencia de cada caracter en la cadena
frecuencia = {}  # es un diccionario que se utilizará para almacenar la frecuencia de cada carácter en la cadena.
for caracter in cadena:
    frecuencia[caracter] = frecuencia.get(caracter, 0) + 1  

#Al final de este bucle, frecuencia contiene la frecuencia de cada carácter en la cadena.
# Ordenar la frecuencia en orden descendente
frecuencia = sorted(frecuencia.items(), key=lambda x: x[1], reverse=True)   #sorted vuelve lo elementos del diccionario una list de tuplas de par clave. tenemos un ordenamiento descendente por el 'reverse = true'

# Inicializar nodos con la frecuencia ordenada
nodos = frecuencia  #La lista nodos se inicializa con la lista ordenada de tuplas que contiene los caracteres y sus frecuencias.

# Construir el árbol de Huffman

"""
para la construcción del arbol.
El bucle se ejecuta mientras haya más de un nodo en la lista nodos.
En cada iteración, se extraen los dos nodos con menor frecuencia (nodos[-1] y nodos[-2]), se eliminan de la lista, y se crea un nuevo nodo que tiene estos dos nodos como hijos.
El nuevo nodo se agrega de nuevo a la lista junto con la suma de sus frecuencias.
La lista se ordena nuevamente en orden descendente según las frecuencias.
En resumen, la lista nodos se utiliza como una cola de prioridad para mantener los nodos ordenados por frecuencia durante la construcción del árbol de Huffman. La prioridad está determinada por la frecuencia de los nodos, y la lista se actualiza en cada iteración del bucle principal para fusionar los nodos con menor frecuencia.


"""
while len(nodos) > 1:
    (clave1, c1) = nodos[-1]           #obtienen los dos nodos con menor frecuencia al final de la lista nodos.
    (clave2, c2) = nodos[-2] 
    nodos = nodos[:-2]            #elimina esos dos nodos de la lista nodos.
    nodo = NodoArbol(clave1, clave2)       # crea un nuevo nodo de árbol con los nodos combinados. Se asume que existe una clase NodoArbol que tiene un constructor que toma dos claves (en este caso, los caracteres) como parámetros y crea un nuevo nodo.
    nodos.append((nodo, c1 + c2))            # agrega el nuevo nodo combinado junto con su frecuencia total a la lista nodos
    nodos = sorted(nodos, key=lambda x: x[1], reverse=True)      # ordena la lista nodos en orden descendente según la frecuencia total de los nodos.
#-----------------------------------------------------------------
# Guardar el árbol en un archivo en formato pickle
with open('arbol_huffman.pkl', 'wb') as archivo_arbol:
    pickle.dump(nodos[0][0], archivo_arbol)

# Imprimir mensaje de éxito
print('Árbol de Huffman guardado en "arbol_huffman.pkl".')

# Cargar el árbol desde el archivo pickle
with open('arbol_huffman.pkl', 'rb') as archivo_arbol:
    arbol_cargado = pickle.load(archivo_arbol)
#-----------------------------------------------------------------


# Codificación de Huffman en binario
codigo_huffman = arbol_codificacion_huffman(arbol_cargado)   #Utiliza la función arbol_codificacion_huffman para obtener un diccionario que contiene la codificación Huffman en binario para cada carácter. arbol_cargado se pasa como argumento a esta función, asumiendo que representa el árbol de Huffman.

#-----------------------------------------------------------------
 
# Imprimir tabla de codificación en binario
print(' Codificacion en Binario \n ')
print(' Caracter | Código Huffman ')
print('--------------------------')


for (caracter, frecuencia) in frecuencia:
    print(f' %-8r |%12s' % (caracter, codigo_huffman[caracter]))
print('--------------------------')

#-----------------------------------------------------------------

# Función para codificar la cadena original
# Este código da una función para codificar una cadena utilizando la codificación Huffman proporcionada y luego la aplica a la cadena original, almacenando el resultado en la variable cadena_codificada.
def codificar(cadena, codigo_huffman):
    cadena_codificada = ''
    for caracter in cadena:
        cadena_codificada += codigo_huffman[caracter]
    return cadena_codificada

# Codificar la cadena original
cadena_codificada = codificar(cadena, codigo_huffman)
#-----------------------------------------------------------------

# Imprimir la cadena codificada en binario
print('Código en Binario:', cadena_codificada,'\n')

#-----------------------------------------------------------------
#almacena el archivo la cadena en txt
with open('CodigoHuffmanBinario.txt', 'w') as archivo:
    archivo.write(cadena_codificada)
#-----------------------------------------------------------------
#almacenar ek archivo codificado en formato binario
formatoBin.guardar_en_binario(cadena_codificada, nombre_archivo = 'CodigoHuffmanBinario.bin')
#----------------------------------------------------------------   

# Función para decodificar la cadena codificada en binario
def decodificar(cadena_codificada, arbol_huffman):
    arbol_actual = arbol_huffman
    cadena_decodificada = ''
    for bit in cadena_codificada:
        if bit == '0':
            arbol_actual = arbol_actual.izquierda
        else:
            arbol_actual = arbol_actual.derecha

        if isinstance(arbol_actual, NodoArbol):   #Se verifica si arbol_actual es una instancia de la clase NodoArbol o una cadena (str).
            continue  # No es una hoja, seguir descendiendo
        elif isinstance(arbol_actual, str):   #Si es una cadena (str), se agrega a cadena_decodificada, y arbol_actual se reinicia al árbol de Huffman original.
            cadena_decodificada += arbol_actual
            arbol_actual = arbol_huffman

    return cadena_decodificada

# Decodificar la cadena codificada en binario
cadena_decodificada = decodificar(cadena_codificada, arbol_cargado)
#-----------------------------------------------------------------

#print('Cadena decodificada:', cadena_decodificada,'\n')
#-----------------------------------------------------------------

# Obtener el tamaño en bytes del archivo de entrada
size_input_file = len(cadena.encode('utf-8')) 
# Obtener el tamaño en bytes del archivo .txt en binario)
size_txt_file = os.path.getsize('CodigoHuffmanBinario.txt')
# Obtener el tamaño en bytes paraa el archivo .bin (comprimido)
size_bin_file = os.path.getsize('CodigoHuffmanBinario.bin')

# Obtener el tamaño en bytes del archivo .pkl
size_pkl_file = os.path.getsize('arbol_huffman.pkl')

def calcular_porcentaje_compresion(tamano_original, tamano_comprimido):
    return (1 - (tamano_comprimido / tamano_original)) * 100

Tamaño_porcentaje = calcular_porcentaje_compresion(size_input_file, size_bin_file)

# Imprimir los tamaños de archivo
print(f'Tamaño del archivo de entrada: {size_input_file} bytes')
print(f'Tamaño del archivo comprimido y en formato binario: {size_bin_file} bytes')
print(f'Porcentaje de compresion entre el archivo de entraad y el archivo comprimido (en formato .Bin): {Tamaño_porcentaje} %')
#Hay que guardar el archivo decodificado en un txt nuevamente para ver el resultado. Este tiene que tener el mismo tamaño.
print(f'Tamaño del archivo CodigoHuffmanBinario.txt: {size_txt_file} bytes')

print(f'Tamaño del árbol en formato .pkl: {size_pkl_file} bytes')

#print(f'Porcentaje de la compresión en este ejemplo: {size_bin_file*8}')







