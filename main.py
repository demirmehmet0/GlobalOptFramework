# -*- coding: utf-8 -*-
import os
import string
import sys
import time
""" string.decode('utf-8')  # or:
unicode(string, 'utf-8') """

from LWFWSW import main as lwfwsw
def read_file(file_name):
    f = open(file_name, 'r', encoding='utf-8')
    data = f.read()
    f.close()
    return data
def replace(path, find, replace):
    matrixCpp = read_file(path)
    matrixCpp = matrixCpp.replace(find, replace)
    f = open(path, 'w', encoding='utf-8')
    f.write(matrixCpp)
    f.close()

params = dict()
filePath = "./parameter.txt"
with open(filePath, "r") as f:
    for line in f:
        line = line.strip()
        if line.startswith("#"):
            continue
        if line.startswith("ALGORITHM"):
            params["ALGORITHM"] = line.split("=")[1]
        elif line.startswith("MATRIX_PATH"):
            params["MATRIX_PATH"] = line.split("=")[1]
        elif line.startswith("ITERATION"):
            params["ITERATION"] = line.split("=")[1]
        elif line.startswith("CHOSEN_PARAM"):
            params["CHOSEN_PARAM"] = line.split("=")[1]
        elif line.startswith("THRESHOLD"):
            params["THRESHOLD"] = line.split("=")[1]
        elif line.startswith("DEPTH"):
            params["DEPTH"] = line.split("=")[1]
        elif line.startswith("NUM_MATRICES"):
            params["NUM_MATRICES"] = line.split("=")[1]
        elif line.startswith("BFI"):
            params["BFI"] = line.split("=")[1]
        else:
            print("Error: unknown parameter: " + line)
            sys.exit(1)

print("ALGORITHM: " + params["ALGORITHM"])
print("MATRIX_PATH: " + params["MATRIX_PATH"])
print("ITERATION: " + params["ITERATION"])


#convert binary matrix to hex matrix
def convertBinaryToHex(matrix,size):
    temp = ""
    temp16 = []
    for i in range(len(matrix)):
        temp += matrix[i]

        if i % 4 == 3 and i != 0:
            try:
                #print(temp)
                temp = hex(int(temp, 2))
                #print(temp)
                temp16.append(temp)
                temp = ""
            except:
                pass
    hex16 = []

    for i in range(0,len(temp16), int(size/4)):
        if i % int(size/4) == 0:
            #hex16.append(temp16[i]+temp16[i+1].replace("0x", "")+temp16[i+2].replace("0x", "")+temp16[i+3].replace("0x", ""))
            str = ''
            for j in range(int(size/4)):
                if j == 0:
                    str += temp16[i]
                else:
                    str += temp16[i+j].replace("0x", "")
            hex16.append(str)
    
    return hex16

if params["ALGORITHM"] == "1":
    print("XZLBZ")
    matrix = ""
    with open(params["MATRIX_PATH"], "r") as f:
        size = f.readline()
        size = size.strip()
        size = int(size.split(" ")[0])
        for line in f:
            matrix += line
    matrix = matrix.replace(" ", "").replace("\n", "")
    matrix = convertBinaryToHex(matrix,size)
    matrix = ",".join(matrix)
    matrixName = params["MATRIX_PATH"].split("/")[-1].split(".")[0] + "_result.txt"
    replace('./XZLBZ/matrix.cpp', "vector<ROW> m{};", "vector<ROW> m{" + matrix + "};")
    replace('./XZLBZ/main.cpp', "while(say<0)", "while(say<" + params["ITERATION"] + ")")
    replace('./XZLBZ/matrix.h', '#define FILENAME ""', '#define FILENAME "' + matrixName + '"')
    replace('./XZLBZ/matrix.h', '#define SIZE 16', '#define SIZE ' + str(size))
    commandCmake = 'cmake ./XZLBZ'
    commandMake = 'make'
    commandRun = './untitled'
    os.system(commandCmake)
    os.system(commandMake)
    replace('./XZLBZ/matrix.cpp', "vector<ROW> m{" + matrix + "};", "vector<ROW> m{};")
    replace('./XZLBZ/main.cpp', "while(say<" + params["ITERATION"] + ")", "while(say<0)")
    replace('./XZLBZ/matrix.h', '#define FILENAME "' + matrixName + '"', '#define FILENAME ""')
    replace('./XZLBZ/matrix.h', '#define SIZE ' + str(size), '#define SIZE 16')
    os.system(commandRun)


elif params["ALGORITHM"] == "2":
    print("BP")
    replace('./bp/boyarSLP.cpp', "TheMatrix.open(\"\");", "TheMatrix.open(\"" + params["MATRIX_PATH"] + "\");")
    replace('./bp/boyarSLP.cpp', "std::fstream f(\"\",", "std::fstream f(\"./matrices/result/BP_" + params["MATRIX_PATH"].split("/")[-1] + "\", ")
    #NumMatrices = 1; replace to params["NUM_MATRICES"]
    replace('./bp/boyarSLP.cpp', "NumMatrices = 1;", "NumMatrices = " + params["NUM_MATRICES"] + ";")
    #Threshold = 0;
    replace('./bp/boyarSLP.cpp', "Threshold = 0;", "Threshold = " + params["THRESHOLD"] + ";")
    #DepthLimit = 0;
    replace('./bp/boyarSLP.cpp', "DepthLimit = 0;", "DepthLimit = " + params["DEPTH"] + ";")
    os.system("g++ ./bp/boyarSLP.cpp")
    replace('./bp/boyarSLP.cpp', "TheMatrix.open(\"" + params["MATRIX_PATH"] + "\");", "TheMatrix.open(\"\");")
    replace('./bp/boyarSLP.cpp', "std::fstream f(\"./matrices/result/BP_" + params["MATRIX_PATH"].split("/")[-1] + "\", ", "std::fstream f(\"\",")
    replace('./bp/boyarSLP.cpp', "NumMatrices = " + params["NUM_MATRICES"] + ";", "NumMatrices = 1;")
    replace('./bp/boyarSLP.cpp', "Threshold = " + params["THRESHOLD"] + ";", "Threshold = 0;")
    replace('./bp/boyarSLP.cpp', "DepthLimit = " + params["DEPTH"] + ";", "DepthLimit = 0;")
    os.system("./a.out")
    time.sleep(3)

elif params["ALGORITHM"] == "3":
    print("RNBP")
    #int limit = 50;
    replace('./a1_a2_rnbp/main_globalopt.cpp', "int limit = 50;", "int limit = " + params["ITERATION"] + ";")
    replace('./a1_a2_rnbp/main_globalopt.cpp', "std::fstream f(\"\",", "std::fstream f(\"./matrices/result/RNBP_" + params["MATRIX_PATH"].split("/")[-1] + "\", ")
    os.system("g++ -std=c++11 -o a1_a2_rnbp/rnbp.out -D OPTION=1 -D TIME_LIMIT=1000 a1_a2_rnbp/main_globalopt.cpp")
    replace('./a1_a2_rnbp/main_globalopt.cpp', "int limit = " + params["ITERATION"] + ";", "int limit = 50;")
    replace('./a1_a2_rnbp/main_globalopt.cpp', "std::fstream f(\"./matrices/result/RNBP_" + params["MATRIX_PATH"].split("/")[-1] + "\", ", "std::fstream f(\"\",")
    os.system("./a1_a2_rnbp/rnbp.out < " + params["MATRIX_PATH"])
    
elif params["ALGORITHM"] == "4":
    print("A1")
    replace('./a1_a2_rnbp/main_globalopt.cpp', "int limit = 50;", "int limit = " + params["ITERATION"] + ";")
    replace('./a1_a2_rnbp/main_globalopt.cpp', "std::fstream f(\"\",", "std::fstream f(\"./matrices/result/A1_" + params["MATRIX_PATH"].split("/")[-1] + "\", ")
    os.system("g++ -std=c++11 -o a1_a2_rnbp/a1.out -D OPTION=2 -D TIME_LIMIT=1000 a1_a2_rnbp/main_globalopt.cpp")
    replace('./a1_a2_rnbp/main_globalopt.cpp', "int limit = " + params["ITERATION"] + ";", "int limit = 50;")
    replace('./a1_a2_rnbp/main_globalopt.cpp', "std::fstream f(\"./matrices/result/A1_" + params["MATRIX_PATH"].split("/")[-1] + "\", ", "std::fstream f(\"\",")
    os.system("./a1_a2_rnbp/a1.out < " + params["MATRIX_PATH"])
elif params["ALGORITHM"] == "5":
    print("A2")
    replace('./a1_a2_rnbp/main_globalopt.cpp', "int limit = 50;", "int limit = " + params["ITERATION"] + ";")
    replace('./a1_a2_rnbp/main_globalopt.cpp', "std::fstream f(\"\",", "std::fstream f(\"./matrices/result/A2_" + params["MATRIX_PATH"].split("/")[-1] + "\", ")
    os.system("g++ -std=c++11 -o a1_a2_rnbp/a2.out -D OPTION=3 -D TIME_LIMIT=1000 a1_a2_rnbp/main_globalopt.cpp")
    replace('./a1_a2_rnbp/main_globalopt.cpp', "int limit = " + params["ITERATION"] + ";", "int limit = 50;")
    replace('./a1_a2_rnbp/main_globalopt.cpp', "std::fstream f(\"./matrices/result/A2_" + params["MATRIX_PATH"].split("/")[-1] + "\", ", "std::fstream f(\"\",")
    os.system("./a1_a2_rnbp/a2.out < " + params["MATRIX_PATH"])
elif params["ALGORITHM"] == "6":
    print("Paar1")
    #NumMatrices = 1; replace to params["NUM_MATRICES"]
    replace('./paar/paar.cpp', "NumMatrices = 1;", "NumMatrices = " + params["NUM_MATRICES"] + ";")
    os.system("g++ -o paar/paar1.out paar/paar.cpp")
    replace('./paar/paar.cpp', "NumMatrices = " + params["NUM_MATRICES"] + ";", "NumMatrices = 1;")
    os.system("./paar/paar1.out paar1 "+ params["MATRIX_PATH"] + " " + params["THRESHOLD"] + " " + params["DEPTH"])

elif params["ALGORITHM"] == "7":
    print("Paar2")
    #NumMatrices = 1; replace to params["NUM_MATRICES"]
    replace('./paar/paar.cpp', "NumMatrices = 1;", "NumMatrices = " + params["NUM_MATRICES"] + ";")
    os.system("g++ -o paar/paar2.out paar/paar.cpp")
    replace('./paar/paar.cpp', "NumMatrices = " + params["NUM_MATRICES"] + ";", "NumMatrices = 1;")
    os.system("./paar/paar2.out paar2 "+ params["MATRIX_PATH"] + " " + params["THRESHOLD"] + " " + params["DEPTH"])


elif params["ALGORITHM"] == "8":
    lwfwsw.start(params["MATRIX_PATH"], int(params["ITERATION"]))

elif params["ALGORITHM"] == "9":#bfi
    print("bfi orginal")
    with open(params["MATRIX_PATH"], "r") as f:
        size = f.readline()
        size = size.strip()
        size = int(size.split(" ")[0])
    #find int OPTION_B = rand_distribution(rand_generator); in main.cpp and replace with OPTION_B = 1;
    replace('./framework-main-2/reduce.cpp', "int limit = 100;", "int limit = " + params["ITERATION"] + ";")
    replace('./framework-main-2/BFI.cpp', "tmp_dis[16]", "tmp_dis[" + str(size) + "]")
    os.system("g++ framework-main-2/*.cpp -D FUNCTION=1 -o framework-main-2/bfi.out -lpthread")
    replace('./framework-main-2/reduce.cpp', "int limit = " + params["ITERATION"] + ";", "int limit = 100;")
    replace('./framework-main-2/BFI.cpp', "tmp_dis[" + str(size) + "]", "tmp_dis[16]")
    os.system("./framework-main-2/bfi.out < " + params["MATRIX_PATH"])
elif params["ALGORITHM"] == "10":#bfi paar
    print("bfi paar")
    with open(params["MATRIX_PATH"], "r") as f:
        size = f.readline()
        size = size.strip()
        size = int(size.split(" ")[0])
    replace('./framework-main-2/reduce.cpp', "int limit = 100;", "int limit = " + params["ITERATION"] + ";")
    replace('./framework-main-2/RNBP_A1_A2.cpp', "int OPTION_B = rand_distribution(rand_generator);", "int OPTION_B = 0;")
    replace('./framework-main-2/paar.cpp', "tmp_dis[16]", "tmp_dis[" + str(size) + "]")
    replace('./framework-main-2/BFI.cpp', "tmp_dis[16]", "tmp_dis[" + str(size) + "]")
    os.system("g++ framework-main-2/*.cpp -D FUNCTION=1 -o framework-main-2/paar.out -lpthread")
    os.system("./framework-main-2/paar.out < " + params["MATRIX_PATH"])
    replace('./framework-main-2/RNBP_A1_A2.cpp', "int OPTION_B = 0;", "int OPTION_B = rand_distribution(rand_generator);")
    replace('./framework-main-2/reduce.cpp', "int limit = " + params["ITERATION"] + ";", "int limit = 100;")
    replace('./framework-main-2/paar.cpp', "tmp_dis[" + str(size) + "]", "tmp_dis[16]")
    replace('./framework-main-2/BFI.cpp', "tmp_dis[" + str(size) + "]", "tmp_dis[16]")
elif params["ALGORITHM"] == "11":#bfi rpaar
    with open(params["MATRIX_PATH"], "r") as f:
        size = f.readline()
        size = size.strip()
        size = int(size.split(" ")[0])
    print("bfi rpaar")
    replace('./framework-main-2/reduce.cpp', "int limit = 100;", "int limit = " + params["ITERATION"] + ";")
    replace('./framework-main-2/RNBP_A1_A2.cpp', "int OPTION_B = rand_distribution(rand_generator);", "int OPTION_B = 1;")
    replace('./framework-main-2/BFI.cpp', "tmp_dis[16]", "tmp_dis[" + str(size) + "]")
    os.system("g++ framework-main-2/*.cpp -D FUNCTION=1 -o framework-main-2/rpaar.out -lpthread")
    os.system("./framework-main-2/rpaar.out < " + params["MATRIX_PATH"])
    replace('./framework-main-2/RNBP_A1_A2.cpp', "int OPTION_B = 1;", "int OPTION_B = rand_distribution(rand_generator);")
    replace('./framework-main-2/reduce.cpp', "int limit = " + params["ITERATION"] + ";", "int limit = 100;")
    replace('./framework-main-2/BFI.cpp', "tmp_dis[" + str(size) + "]", "tmp_dis[16]")
elif params["ALGORITHM"] == "12":#bfi BP
    with open(params["MATRIX_PATH"], "r") as f:
        size = f.readline()
        size = size.strip()
        size = int(size.split(" ")[0])
    print("bfi BP")
    replace('./framework-main-2/reduce.cpp', "int limit = 100;", "int limit = " + params["ITERATION"] + ";")
    replace('./framework-main-2/RNBP_A1_A2.cpp', "int OPTION_B = rand_distribution(rand_generator);", "int OPTION_B = 2;")
    replace('./framework-main-2/BFI.cpp', "tmp_dis[16]", "tmp_dis[" + str(size) + "]")
    os.system("g++ framework-main-2/*.cpp -D FUNCTION=1 -o framework-main-2/bp.out -lpthread")
    os.system("./framework-main-2/bp.out < " + params["MATRIX_PATH"])
    replace('./framework-main-2/RNBP_A1_A2.cpp', "int OPTION_B = 2;", "int OPTION_B = rand_distribution(rand_generator);")
    replace('./framework-main-2/reduce.cpp', "int limit = " + params["ITERATION"] + ";", "int limit = 100;")
    replace('./framework-main-2/BFI.cpp', "tmp_dis[" + str(size) + "]", "tmp_dis[16]")
elif params["ALGORITHM"] == "13":#bfi a1
    with open(params["MATRIX_PATH"], "r") as f:
        size = f.readline()
        size = size.strip()
        size = int(size.split(" ")[0])
    print("bfi a1")
    replace('./framework-main-2/reduce.cpp', "int limit = 100;", "int limit = " + params["ITERATION"] + ";")
    replace('./framework-main-2/RNBP_A1_A2.cpp', "int OPTION_B = rand_distribution(rand_generator);", "int OPTION_B = 3;")
    replace('./framework-main-2/BFI.cpp', "tmp_dis[16]", "tmp_dis[" + str(size) + "]")
    os.system("g++ framework-main-2/*.cpp -D FUNCTION=1 -o framework-main-2/a1.out -lpthread")
    os.system("./framework-main-2/a1.out < " + params["MATRIX_PATH"])
    replace('./framework-main-2/RNBP_A1_A2.cpp', "int OPTION_B = 3;", "int OPTION_B = rand_distribution(rand_generator);")
    replace('./framework-main-2/reduce.cpp', "int limit = " + params["ITERATION"] + ";", "int limit = 100;")
    replace('./framework-main-2/BFI.cpp', "tmp_dis[" + str(size) + "]", "tmp_dis[16]")
elif params["ALGORITHM"] == "14":#bfi a2
    with open(params["MATRIX_PATH"], "r") as f:
        size = f.readline()
        size = size.strip()
        size = int(size.split(" ")[0])
    print("bfi a2")
    replace('./framework-main-2/reduce.cpp', "int limit = 100;", "int limit = " + params["ITERATION"] + ";")
    replace('./framework-main-2/RNBP_A1_A2.cpp', "int OPTION_B = rand_distribution(rand_generator);", "int OPTION_B = 4;")
    replace('./framework-main-2/BFI.cpp', "tmp_dis[16]", "tmp_dis[" + str(size) + "]")
    os.system("g++ framework-main-2/*.cpp -D FUNCTION=1 -o framework-main-2/a2.out -lpthread")
    os.system("./framework-main-2/a2.out < " + params["MATRIX_PATH"])
    replace('./framework-main-2/RNBP_A1_A2.cpp', "int OPTION_B = 4;", "int OPTION_B = rand_distribution(rand_generator);")
    replace('./framework-main-2/reduce.cpp', "int limit = " + params["ITERATION"] + ";", "int limit = 100;")
    replace('./framework-main-2/BFI.cpp', "tmp_dis[" + str(size) + "]", "tmp_dis[16]")
elif params["ALGORITHM"] == "15":#bfi rnbp
    with open(params["MATRIX_PATH"], "r") as f:
        size = f.readline()
        size = size.strip()
        size = int(size.split(" ")[0])
    print("bfi rnbp")
    replace('./framework-main-2/reduce.cpp', "int limit = 100;", "int limit = " + params["ITERATION"] + ";")
    replace('./framework-main-2/RNBP_A1_A2.cpp', "int OPTION_B = rand_distribution(rand_generator);", "int OPTION_B = 5;")
    replace('./framework-main-2/BFI.cpp', "tmp_dis[16]", "tmp_dis[" + str(size) + "]")
    os.system("g++ framework-main-2/*.cpp -D FUNCTION=1 -o framework-main-2/rnbp.out -lpthread")
    os.system("./framework-main-2/rnbp.out < " + params["MATRIX_PATH"])
    replace('./framework-main-2/RNBP_A1_A2.cpp', "int OPTION_B = 5;", "int OPTION_B = rand_distribution(rand_generator);")
    replace('./framework-main-2/reduce.cpp', "int limit = " + params["ITERATION"] + ";", "int limit = 100;")
    replace('./framework-main-2/BFI.cpp', "tmp_dis[" + str(size) + "]", "tmp_dis[16]")
elif params["ALGORITHM"] == "16":#bfi BP
    print("bfi BP")
    replace('./bp/boyarSLP.cpp', "TheMatrix.open(\"\");", "TheMatrix.open(\"" + params["MATRIX_PATH"] + "\");")
    replace('./bp/boyarSLP.cpp', "std::fstream f(\"\",", "std::fstream f(\"./matrices/result/bfiBP_" + params["MATRIX_PATH"].split("/")[-1] + "\", ")
    #NumMatrices = 1; replace to params["NUM_MATRICES"]
    replace('./bp/boyarSLP.cpp', "NumMatrices = 1;", "NumMatrices = " + params["NUM_MATRICES"] + ";")
    #Threshold = 0;
    replace('./bp/boyarSLP.cpp', "Threshold = 0;", "Threshold = " + params["THRESHOLD"] + ";")
    #DepthLimit = 0;
    replace('./bp/boyarSLP.cpp', "DepthLimit = 0;", "DepthLimit = " + params["DEPTH"] + ";")
    replace('./bp/boyarSLP.cpp', "int BFI = 0;", "int BFI = " + params["BFI"] + ";")
    os.system("g++ ./bp/boyarSLP.cpp")
    replace('./bp/boyarSLP.cpp', "TheMatrix.open(\"" + params["MATRIX_PATH"] + "\");", "TheMatrix.open(\"\");")
    replace('./bp/boyarSLP.cpp', "std::fstream f(\"./matrices/result/bfiBP_" + params["MATRIX_PATH"].split("/")[-1] + "\", ", "std::fstream f(\"\",")
    replace('./bp/boyarSLP.cpp', "NumMatrices = " + params["NUM_MATRICES"] + ";", "NumMatrices = 1;")
    replace('./bp/boyarSLP.cpp', "Threshold = " + params["THRESHOLD"] + ";", "Threshold = 0;")
    replace('./bp/boyarSLP.cpp', "DepthLimit = " + params["DEPTH"] + ";", "DepthLimit = 0;")
    replace('./bp/boyarSLP.cpp', "int BFI = " + params["BFI"] + ";", "int BFI = 0;")
    for k in range(int(params["ITERATION"])):
        print("iteration " + str(k))
        os.system("./a.out")
    time.sleep(0.5)
