import itertools
import numpy as np
from numpy import random
from scipy.optimize import linear_sum_assignment
 

class SelectionData:
#Realizamos una clase para poder inicialiar los datos
    def __init__(self, exercise):
        self.exercise = exercise
        self.min_cost, self.best_solution, self.b = self.Hungary(exercise)
 

 # Método húngaro
    def Hungary(self, exercise):
        b = exercise.copy()
 # Buscamos y restamos el numero menos de cada columna y fila
        for i in range(len(b)):
            row_min = np.min(b[i])
            for j in range(len(b[i])):
                b[i][j] -= row_min
        for i in range(len(b[0])):
            col_min = np.min(b[:, i])
            for j in range(len(b)):
                b[j][i] -= col_min
        line_count = 0
 # Nos aseguramos que el numero de lineas a tachast no sea
 #mayor al numero de longitud de nuestro array
        while (line_count < len(b)):
            line_count = 0
            row_zero_count = []
            col_zero_count = []
            for i in range(len(b)):
                #Usamos row_zero_count para saber cuantos 0 hay en cada fila
                row_zero_count.append(np.sum(b[i] == 0))
            for i in range(len(b[0])):
                #Usamos row_zero_count para saber cuantos 0 hay en cada columna
                col_zero_count.append((np.sum(b[:, i] == 0)))
 #line order: contendra los indices de los ceros de nuestro array en axis 0 y 1 (de aca saremos)
 # los indices de los numeros donde se interseccionan las lineas
 #  
 #row_or_col: Una lista que contiene 0 y 1 en las posiciones donde hay 0 en filas y 0 en columans
 #de aca sacaremos los indices de los datos que no seran techados por las lineas
            line_order = []
            row_or_col = []
            for i in range(len(b[0]), 0, -1):
                while (i in row_zero_count):
                    line_order.append(row_zero_count.index(i))
                    row_or_col.append(0)
                    row_zero_count[row_zero_count.index(i)] = 0
                while (i in col_zero_count):
                    line_order.append(col_zero_count.index(i))
                    row_or_col.append(1)
                    col_zero_count[col_zero_count.index(i)] = 0
 # Dibuje una línea que cubra 0 y obtenga la matriz con la fila menos el valor mínimo y la columna más 
 # el valor mínimo
            delete_count_of_row = []
            delete_count_of_col = []
            row_and_col = [i for i in range(len(b))]
            for i in range(len(line_order)):
                if row_or_col[i] == 0:
                    delete_count_of_row.append(line_order[i])
                else:
                    delete_count_of_col.append(line_order[i])
                c = np.delete(b, delete_count_of_row, axis=0)
                c = np.delete(c, delete_count_of_col, axis=1)
                line_count = len(delete_count_of_row) + len(delete_count_of_col)
              ##Cuando el número de líneas es igual a la longitud de la matriz, salta.
              #len(b) represantaria el tamaño de la copia de nuestro array
                if line_count == len(b):
                    break
 # Revisamos si las lineas cubren todos los ceros
 # En esta parte sumamos y restamos el numero menor de nuestros datos que no tachamos con 
 # las lineas
                if 0 not in c:
                    row_sub = list(set(row_and_col) - set(delete_count_of_row))
                    
                    min_value = np.min(c)
                    for i in row_sub:
                        b[i] = b[i] - min_value
                    for i in delete_count_of_col:
                        b[:, i] = b[:, i] + min_value
                    break

#Usamos linear_sum_assigment para asignar los indices en rows and cols de nuestro array (solamente
# de nuestras respuestas es decir de nuestros 0 seleccionados)
        row_ind, col_ind = linear_sum_assignment(b)
        min_cost = exercise[row_ind, col_ind].sum()
        best_solution = list(exercise[row_ind, col_ind])
        return min_cost, best_solution, b
 
def run():
    #Generar matriz de costos
    ##rd = random.RandomState(10000)``
    ##exercise = rd.randint(0, 100, size=(5, 5))
    #exercise = np.array([[1, 4, 6, 3],
    #         [9, 7, 10, 9],
    #         [4, 5, 11, 7],
    #         [8, 7, 8, 5]])
    exercise = np.array([[3, 9, 2, 3, 7],
    [6, 1, 5, 6, 6],
    [9, 4, 7, 10, 3],
    [2, 5, 4, 2, 1],
    [9, 6, 2, 4, 5]])


    #Use el método húngaro para lograr la asignación de tareas
    ass_by_Hun = SelectionData(exercise)
    print ('Asignación de tarea del método húngaro:')
    print('min cost = ', ass_by_Hun.min_cost)
    print('best solution = ', ass_by_Hun.best_solution)
    print('array: \n', ass_by_Hun.b)

if __name__ == "__main__":
    run()