# Milton David Zapata Aguilera - 1866060 - 2711
# 15/12/2023

# Importar las bibliotecas necesarias
import pickle
import networkx as nx
import matplotlib.pyplot as plt
import os

# Definir la cadena de entrada
cadena = 'Mi pasion es programar'

# Imprimir la cadena original
print(' Codigo :  Mi Pasion es programar \n')

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

# Función principal que implementa la codificación de Huffman
def arbol_codificacion_huffman(nodo, izquierda=True, binario=''):
    if type(nodo) is str:
        return {nodo: binario}
    (izq, der) = nodo.hijos()
    diccionario = dict()
    diccionario.update(arbol_codificacion_huffman(izq, True, binario + '0'))
    diccionario.update(arbol_codificacion_huffman(der, False, binario + '1'))
    return diccionario

# Calculando la frecuencia de cada caracter en la cadena
frecuencia = {}
for caracter in cadena:
    frecuencia[caracter] = frecuencia.get(caracter, 0) + 1

# Ordenar la frecuencia en orden descendente
frecuencia = sorted(frecuencia.items(), key=lambda x: x[1], reverse=True)

# Inicializar nodos con la frecuencia ordenada
nodos = frecuencia

# Construir el árbol de Huffman
while len(nodos) > 1:
    (clave1, c1) = nodos[-1]
    (clave2, c2) = nodos[-2]
    nodos = nodos[:-2]
    nodo = NodoArbol(clave1, clave2)
    nodos.append((nodo, c1 + c2))
    nodos = sorted(nodos, key=lambda x: x[1], reverse=True)

# Guardar el árbol en un archivo en formato pickle
with open('arbol_huffman.pkl', 'wb') as archivo_arbol:
    pickle.dump(nodos[0][0], archivo_arbol)

# Imprimir mensaje de éxito
print('Árbol de Huffman guardado en "arbol_huffman.pkl".')

# Cargar el árbol desde el archivo pickle
with open('arbol_huffman.pkl', 'rb') as archivo_arbol:
    arbol_cargado = pickle.load(archivo_arbol)

# Codificación de Huffman en binario
codigo_huffman = arbol_codificacion_huffman(arbol_cargado)

# Imprimir tabla de codificación en binario
print(' Codificacion en Binario \n ')
print(' Caracter | Código Huffman ')
print('--------------------------')
for (caracter, frecuencia) in frecuencia:
    print(f' %-8r |%15s' % (caracter, codigo_huffman[caracter]))
print('--------------------------')

# Función para codificar la cadena original
def codificar(cadena, codigo_huffman):
    cadena_codificada = ''
    for caracter in cadena:
        cadena_codificada += codigo_huffman[caracter]
    return cadena_codificada

# Codificar la cadena original
cadena_codificada = codificar(cadena, codigo_huffman)

# Imprimir la cadena codificada en binario
print('Código en Binario:', cadena_codificada,'\n')

# Guardar la cadena codificada en un archivo de texto
with open('CodigoHuffmanBinario.txt', 'w') as archivo:
    archivo.write(cadena_codificada)

# Imprimir mensaje de éxito
print(f'Cadena codificada almacenada en el archivo "CodigoHuffmanBinario.txt". \n')

# Función para decodificar la cadena codificada en binario
def decodificar(cadena_codificada, arbol_huffman):
    arbol_actual = arbol_huffman
    cadena_decodificada = ''
    for bit in cadena_codificada:
        if bit == '0':
            arbol_actual = arbol_actual.izquierda
        else:
            arbol_actual = arbol_actual.derecha

        if isinstance(arbol_actual, NodoArbol):
            continue  # No es una hoja, seguir descendiendo
        elif isinstance(arbol_actual, str):
            cadena_decodificada += arbol_actual
            arbol_actual = arbol_huffman

    return cadena_decodificada

# Decodificar la cadena codificada en binario
cadena_decodificada = decodificar(cadena_codificada, arbol_cargado)

# Imprimir la cadena decodificada
print('Cadena decodificada:', cadena_decodificada,'\n')

# Obtener el tamaño en bytes del archivo de entrada
size_input_file = len(cadena.encode('utf-8'))

# Obtener el tamaño en bytes del archivo .txt
size_txt_file = os.path.getsize('CodigoHuffmanBinario.txt')

# Obtener el tamaño en bytes del archivo .pkl
size_pkl_file = os.path.getsize('arbol_huffman.pkl')

# Imprimir los tamaños de archivo
print(f'Tamaño del archivo de entrada: {size_input_file} bytes')
print(f'Tamaño del archivo txt: {size_txt_file} bytes')
print(f'Tamaño del archivo pkl: {size_pkl_file} bytes')
print(f'Tamaño total: {size_txt_file + size_pkl_file} bytes')

# Graficar  el arbol de huffman

"""
def arbol_a_grafo(arbol, G=None, parent_name=None, graph_style='spring', pos=None, level=0, width=2., vert_gap=0.4, xcenter=0.5):
    if G is None:
        G = nx.Graph()

    if pos is None:
        pos = {parent_name: (xcenter, 1 - level * vert_gap)}
    else:
        pos[parent_name] = (xcenter, 1 - level * vert_gap)

    neighbors = list(arbol.hijos())
    if len(neighbors) != 0:
        dx = width / 2
        nextx = xcenter - width/2 - dx/2
        for neighbor in neighbors:
            nextx += dx
            pos = arbol_a_grafo(neighbor, G=G, parent_name=parent_name, pos=pos, level=level+1, width=dx, xcenter=nextx)

    return pos

def graficar_arbol(arbol, graph_style='spring', graph_orientation='horizontal', node_size=1600, node_color='blue', node_alpha=0.3, node_text_size=12, edge_color='blue', edge_alpha=0.3, edge_tickness=1, edge_text_pos=0.3, text_font='sans-serif'):
    G = nx.Graph()
    G.add_node(arbol)
    pos = arbol_a_grafo(arbol, G=G)
    nx.draw(G, pos, node_size=node_size, node_color=node_color, alpha=node_alpha, node_shape='o', with_labels=True, font_size=node_text_size, font_color='white', font_weight='bold', font_family=text_font)

    plt.show()

    # Obtener el tamaño en bytes del archivo de entrada
    size_input_file = len(cadena.encode('utf-8'))

    # Obtener el tamaño en bytes del archivo .txt
    size_txt_file = os.path.getsize('CodigoHuffmanBinario.txt')

    # Obtener el tamaño en bytes del archivo .pkl
    size_pkl_file = os.path.getsize('arbol_huffman.pkl')
"""


