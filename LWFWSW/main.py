# *encoding=utf-8
#The source code of LWFWSW's algorithm in our framework is provided by the repository given in https://github.com/QunLiu-sdu/Towards-Low-Latency-Implementation
import random
import math
import copy
import time

from LWFWSW.Algorithm import getGraph
# from AlgorithmNorandom import getGraph


def start(matrixPath,theMaxNum):
    print("LWFWSW")
    print(matrixPath)
    print(theMaxNum)
    matrix = []

    with open(matrixPath, 'r') as f:
        f.readline()
        line = f.readline().replace('\n', '').replace(' ', '')
        line = line.replace(' ', '')
        length = len(line)
        while line:
            line = line.replace(' ', '')
            line = line.replace('\n', '')
            num = []
            for i in range(0, length):
                num.append(int(line[i]))
            matrix.append(num)
            line = f.readline()


    minV = []
    minE = []
    minD = []
    minnum = 10000000
    times = 0

    time1 = time.time()

    for i in range(0, theMaxNum):
        if i % 1000 == 0:
            print("current times:{}".format(i))
        result = getGraph(matrix)
        if result[0] <= minnum:
            if result[0] == minnum:
                times = times + 1
                print("min now:{}".format(result[0]))
                minnum = result[0]
                minV.append(result[1])
                minE.append(result[2])
                minD.append(result[3])
            else:
                times = 1
                print("min now:{}".format(result[0]))
                minnum = result[0]
                minV = []
                minE = []
                minD = []
                minV.append(result[1])
                minE.append(result[2])
                minD.append(result[3])

    print("min:{}".format(minnum))  # the minmum XOR gates
    print("V = {}".format(minV))  # nodes set
    print("E = {}".format(minE))  # edges set
    for D in minD:
        for key in D:
            if key[0] == 'o':
                D[key] = D[key] - 1
    # Notice that the output node has an additional depth for convenience.
    # When we calculate the depth of the graph, we needn't use the output nodes because the adders can represent them.
    # For example, when the output node has depth 4, the graph has the depth 3.
    print("D = {}".format(minD))  # the depth of each node.
    minDepthNum = -1
    for D in minD:
        for key in D:
            if key[0] == 'o':
                if D[key] > minDepthNum:
                    minDepthNum = D[key]
    print("depth:{}".format(minDepthNum))
    print("times:{}".format(times))
    time2 = time.time()
    print("time:{}".format(time2 - time1))

    V = minV[0]
    E = minE[0]
    numbermaxmax = len(matrix)  # size

    fundemental = []
    result = []
    import copy

    V_copy = copy.deepcopy(V)
    for node in V:
        a = node[0]
        if node[0] == 'i' or node[0] == 'o':
            V_copy.remove(node)
            fundemental.append(node)
    V = copy.deepcopy(V_copy)

    E_copy = copy.deepcopy(E)
    for nodes in E:
        for i in range(0, numbermaxmax):
            node = "oput{}".format(i)
            if nodes[1] == node:
                E_copy.remove(nodes)
                break
    E = copy.deepcopy(E_copy)

    while len(V) != 0:
        for node in V:
            Vnodes = []
            for nodes in E:
                if nodes[1] == node:
                    if nodes[0] not in fundemental:
                        continue
                    else:
                        Vnodes.append(nodes[0])
            if len(Vnodes) != 2:
                continue
            re = "{0} = {1} ^ {2}".format(node, Vnodes[0], Vnodes[1])
            result.append(re)
            V.remove(node)
            fundemental.append(node)
            break

    result_other = []
    numberSet = []
    for re in result:
        side_or = -1
        side_equal = -1
        for i in range(0, len(re)):
            if re[i] == '^':
                side_or = i
            if re[i] == '=':
                side_equal = i
        symbol1 = re[side_equal + 2]
        symbol2 = re[side_or + 2]
        number0 = int(re[5:(side_equal - 1)])
        numberSet.append(number0)
        number1 = -1
        number2 = -1
        if symbol1 == 'i':
            number1 = int(re[(side_equal + 6):(side_or - 1)])
        else:
            number1 = int(re[(side_equal + 7):(side_or - 1)])
        if symbol2 == 'i':
            number2 = int(re[(side_or + 6):])
        else:
            number2 = int(re[(side_or + 7):])
        node1 = ''
        node2 = ''
        if symbol1 == 'i':
            node1 = 'x'
        else:
            node1 = 'a'
        if symbol2 == 'i':
            node2 = 'x'
        else:
            node2 = 'a'
        new_re = 'a' + "{} = ".format(number0) + node1 + "{} ^ ".format(number1) + node2 + "{};".format(number2)
        new_re2 = ''
        if number0 < numbermaxmax:
            new_re2 = "// y{}".format(number0)
        new_re = new_re + new_re2
        result_other.append(new_re)

    number = 0
    for re in result_other:
        number = number + 1
        # print(re)

    numberSet.sort()
    # print(numberSet)
    # print(number)

    result_other_copy = []
    for i in range(0, len(numberSet)):
        if i != numberSet[i]:
            for re in result_other:
                side_or = -1
                side_equal = -1
                side_fen = -1  # ";"
                for j in range(0, len(re)):
                    if re[j] == '^':
                        side_or = j
                    if re[j] == '=':
                        side_equal = j
                    if re[j] == ';':
                        side_fen = j
                number0 = int(re[1:(side_equal - 1)])
                number1 = int(re[(side_equal + 3):(side_or - 1)])
                number2 = int(re[(side_or + 3):(side_fen)])
                if number0 == numberSet[i]:
                    result_other_copy.append("a{}".format(i) + re[(side_equal - 1):])
                elif number1 == numberSet[i]:
                    result_other_copy.append(re[0:(side_equal + 3)] + '{}'.format(i) + re[(side_or - 1):])
                elif number2 == numberSet[i]:
                    result_other_copy.append(re[0:(side_or + 3)] + '{}'.format(i) + re[side_fen:])
                else:
                    result_other_copy.append(re)
            result_other = copy.deepcopy(result_other_copy)
            result_other_copy = []
    for i in result_other:
        print(i)


