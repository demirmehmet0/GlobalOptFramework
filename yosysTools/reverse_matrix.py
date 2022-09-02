
from fileinput import filename
import os

def clean_matrix(matrix, fileName = 'matrix.txt'):
    #clean first 3 rows and remove spaces and [ and ] and \n
    for i in range(3):
        matrix.pop(0)
    for i in range(len(matrix)):
        matrix[i] = matrix[i].replace('[', '')
        matrix[i] = matrix[i].replace(']', '')
        matrix[i] = matrix[i].replace(' ', '')
        matrix[i] = matrix[i].replace('\n', '')
        
    return matrix
def start(filename):
    matrix = []
    with open(os.path.dirname(os.path.abspath(__file__)) + '/'+filename, 'r') as f:
        for line in f:
            matrix.append(line)

    clean_matrix(matrix, filename)
    '''
    ['10000010000001010000', '01000101000000101000', '00100000101001000100', '00010000010100100010', '00001100000010000001', '10000100000000100010', '01000010001000000001', '00100001000100110010', '00010000100010001001', '00001000010001000100', '00010100001000001000', '00001010000100010100', '10010001000010000010', '01001000100001000001', '00100000010000110000', '00001000101000010000', '10000000010100001000', '01001100100010000100', '00100010010001000010', '00010001000000100001']
    '''
    equals = []
    #equals.append([0,6,13,15])
    for i in range(len(matrix)):
        equal = []
        for j in range(len(matrix[i])):
            if matrix[i][j] == '1':
                equal.append(j)
        equals.append(equal)

    return equals, matrix