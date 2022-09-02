import os
import back_prop
import reverse_matrix

matrixFile = "kgf3.txt"
circuitFile = "kgf_3sbpndepth.txt"


# Depth Calculate 
def depth(file):
    #run depth.cpp in terminal
    os.system("g++ depth.cpp -o depth")

    #output depth.cpp to file and input file is matrix.txt
    os.system("./depth "+file +" > depth.txt")
# Depth Calculate 


def calculateEqual():
    matrixEquals, matrix = reverse_matrix.start(matrixFile)

    rows, cols = len(matrix), len(matrix)

    circuit = back_prop.start(circuitFile)
    equal_count = 0
    y_index = []
    for i in matrixEquals:
        for j in circuit:
            if i == j:
                equal_count += 1
                #index of y in matrix
                y_index.append([matrixEquals.index(i),circuit.index(i)])
                break
    
    if equal_count == len(matrixEquals):
        print("matrix equals circuit")
        print(y_index)
        return y_index, True
    else:
        print("matrix not equals circuit")
        return y_index, False
    

y_index, equal = calculateEqual()


def formatCircuit(y_index):
    #read circuit.txt
    f = open(circuitFile, 'r')
    circuit = f.read()
    f.close()
    #replace circuit.txt " " with "," and "+" with "," and "=" with ","
    circuit = circuit.replace(" ", "")
    circuit = circuit.replace("+", ",")
    circuit = circuit.replace("=", ",")
    #split circuit.txt into list
    circuit = circuit.split("\n")
    for i in range(len(circuit)):
        circuit[i] = circuit[i].split(",")
    print(circuit)
    #split circuit.txt by ","
    #remove empty string in circuit.txt
    for i in y_index:
        old = circuit[i[1]]
        #find old and replace with new
        for j in range(len(circuit)):
            for k in range(len(circuit[j])):
                if circuit[j][k] == old:
                    circuit[j][k] = "y+"+i[0]
                    break
    print(circuit)

formatCircuit(y_index)