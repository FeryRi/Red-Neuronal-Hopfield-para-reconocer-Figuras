#para leer el txt y devolverlo como matriz
def leer_patron_txt(ruta):
    matriz = []
    with open(ruta, 'r') as f: # abre archivo en modo de lectura
        for linea in f:
            linea = linea.strip() # elimina espacios y saltos de línea
            # omite líneas vacías
            if linea:  
                fila = [int(c) for c in linea] #convierte cada caracter en int (0 o 1)
                matriz.append(fila)
    return matriz


# para convertir una matriz NxM en un vector 
def reshape(matriz):
    result = []
    row_result = []
    for row in range(len(matriz)):
        for element in range(len(matriz[row])):
            row_result.append(matriz[row][element])
    result.append(row_result)
    return result


# para convertir los 0 en -1
def replace_zeros(matriz):
    result = []
    for row in matriz:
        new_row = []
        for element in row:
            if element == 0:
                new_row.append(-1)
            else:
                new_row.append(element)
        result.append(new_row)
    return result


# calcular la traspuesta de una matriz
def transpose(matriz):
     #verifica que la matriz no esté vacía
    if not matriz:
        return []
    num_rows = len(matriz)
    num_cols = len(matriz[0])
    result = []
    for j in range(num_cols):
        new_row = []
        for i in range(num_rows):
            new_row.append(matriz[i][j])
        result.append(new_row)
    return result


# multiplicación de matrices
def multiply(m1, m2):
    ren_m1 = len(m1)
    cols_m1 = len(m1[0])
    ren_m2 = len(m2)
    cols_m2 = len(m2[0])

    if cols_m1 != ren_m2:
        print("No se puede multiplicar")
        return None

    matriz_result = []
    for i in range(ren_m1):
        lista = []
        for j in range(cols_m2):
            dato = 0
            lista.append(dato)
        matriz_result.append(lista)

    for i in range(ren_m1):
        for j in range(cols_m2):
            for k in range(cols_m1):
                matriz_result[i][j] += m1[i][k] * m2[k][j]
    return matriz_result


# hacer la suma de matrices
def sum_matrices(m1, m2):
    if len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
        print("No se pueden sumar")
        return None

    result = []
    for i in range(len(m1)):
        row = []
        for j in range(len(m1[0])):
            row.append(m1[i][j] + m2[i][j])
        result.append(row)
    return result


# para poner 0s en la diagonal 
def diagonal_matrix(matriz):
    result = []
    for row in range(len(matriz)):
        new_row = []
        for element in range(len(matriz[row])):
            if row == element:
                new_row.append(0)
            else:
                new_row.append(matriz[row][element])
        result.append(new_row)
    return result


def funcion_activacion(valor):
    return 1 if valor >= 0 else -1


# algoritmo iterativo para el reconocimiento de patrones aplicando el algoritmo Hopfield
def reconocer_patron_iterativo(patron_entrada, matriz_pesos):
    #se asegura que la entrada sea una lista plana
    if isinstance(patron_entrada[0], list):
        patron_actual = patron_entrada[0].copy()
    else:
        patron_actual = patron_entrada.copy()

    while True:
        entrada_matriz = [patron_actual]
        resultado = multiply(entrada_matriz, matriz_pesos)

        patron_siguiente = []
        for x in resultado[0]:
            patron_siguiente.append(funcion_activacion(x))

        if patron_siguiente == patron_actual:
            return patron_siguiente

        patron_actual = patron_siguiente.copy()


# para mostrar el patrón como cuadrícula
def mostrar_patron(patron, filas, columnas, titulo="Patrón"):
    print(f"{titulo}:")
    for i in range(filas):
        fila = ""
        for j in range(columnas):
            valor = patron[i*columnas + j]
            fila += "█" if valor == 1 else " "
        print(fila)
    print()  


def main():
    # rutas a los patrones
    ruta_uno = "dataset/a.txt"
    ruta_dos = "dataset/o.txt"
    ruta_tres = "dataset/u.txt"
    ruta_x = "dataset/x.txt"
    ruta_x2 = "dataset/x2.txt"

    # 1. lectura de patrones
    x1 = leer_patron_txt(ruta_uno)
    x2 = leer_patron_txt(ruta_dos)
    x3 = leer_patron_txt(ruta_tres)

    filas = len(x1)
    columnas = len(x1[0])

    # 2. reshape
    x1_r = reshape(x1)
    x2_r = reshape(x2)
    x3_r = reshape(x3)

    # 3. reemplazar ceros con -1
    x1_r = replace_zeros(x1_r)
    x2_r = replace_zeros(x2_r)
    x3_r = replace_zeros(x3_r)

    # 4. obtener transpuesta y multiplicar por si mismo (primer patrón)
    W = multiply(transpose(x1_r), x1_r)

    # 5. agregar segundo y tercer patrón a la matriz de pesos
    W = sum_matrices(W, multiply(transpose(x2_r), x2_r))
    W = sum_matrices(W, multiply(transpose(x3_r), x3_r))

    # 6. poner la diagonal en 0
    W = diagonal_matrix(W)

    # 7. leer patrón de entrada 
    #coincide
    x2_in = leer_patron_txt(ruta_x2)
    x2_in_r = reshape(x2_in)
    x2_in_r = replace_zeros(x2_in_r)
    #no coincide
    x_in = leer_patron_txt(ruta_x)
    x_in_r = reshape(x_in)
    x_in_r = replace_zeros(x_in_r)

    mostrar_patron(x_in_r[0], filas, columnas, "Patrón de entrada (no coincidente)")

    # 8. ejecutar la función para reconocimiento 
    resultado = reconocer_patron_iterativo(x_in_r, W)

    mostrar_patron(resultado, filas, columnas, "Patrón reconocido")

    # 8.2 ejecutar la función para reconocimiento 
    resultado2 = reconocer_patron_iterativo(x2_in_r, W)

    mostrar_patron(resultado2, filas, columnas, "Patrón reconocido")
    mostrar_patron(x2_in_r[0], filas, columnas, "Patrón de entrada (coincidente)")

if __name__ == "__main__":
    main()