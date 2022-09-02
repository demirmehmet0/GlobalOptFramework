import random
import math
import copy
import time


def getGraph(my_matrix):
    """
    get the graph of matrix
    :param my_matrix: matrix
    :return: the graph and the set of nodes and edges and depth
    """

    def getAdderDepth(list):
        """
        get the depth of one number
        :param number: a number
        :return: depth
        """
        if list.count(1) == 0:
            return -1
        else:
            return int(math.ceil(math.log(list.count(1), 2)))

    def getTwoNodesXor(list1, list2):
        """
        get XOR values
        """
        return [list1[j] ^ list2[j] for j in range(0, len(list1))]

    V = []  # node
    E = []  # edge
    matrix = dict()  # {node : value}
    adderCount = 0  # the number of adders
    adderDeleted = 0
    matrixLength = len(my_matrix)  # length
    X = dict()
    P = dict()  # predecessor set
    W = dict()  # working set

    # initialization
    for i in range(0, matrixLength):
        matrix["oput{0}".format(i)] = my_matrix[i]  # output initialization

    for num in range(0, matrixLength):  # V initialization
        iput = "iput{0}".format(num)
        oput = "oput{0}".format(num)
        V.append(iput)
        V.append(oput)
    outputDict = dict()

    for key in matrix:  # adders initialization
        symbol = 0
        if outputDict == {}:
            adder = "adder{}".format(adderCount)
            outputDict[adder] = matrix[key]
            adderCount = adderCount + 1
            V.append(adder)
            E.append([adder, key])
        else:
            for nodeAndVector in outputDict:  # repeat
                if matrix[key] == outputDict[nodeAndVector]:
                    E.append([nodeAndVector, key])
                    symbol = 1
                    break
            if symbol == 1:
                continue
            else:  # no repeat
                adder = "adder{}".format(adderCount)
                adderCount = adderCount + 1
                outputDict[adder] = matrix[key]
                V.append(adder)
                E.append([adder, key])

    # find the depth
    maxAD = [getAdderDepth(matrix[key]) for key in matrix]
    S = 0
    for i in maxAD:
        if i > S:
            S = i
    # find the Hamming weight
    max_weight_sum = [matrix[key].count(1) for key in matrix]
    max_weight = 0
    for i in max_weight_sum:
        if i > max_weight:
            max_weight = i

    i = 0
    for key in matrix:
        X["adder{}".format(i)] = matrix[key]
        i = i + 1
    s = S  # start from the maximum depth
    W = copy.deepcopy(X)  # working set initialization

    if s == 1:  # in this case, we needn't use the algorithm
        P = W
    while s > 1:  # in this case, we haven't the complete graph
        while len(W):  # each node in W need to be calculated
            symbol = 0
            W_key = []  # the name of nodes in W
            for key in W:
                W_key.append(key)
            random.shuffle(W_key)

            # type1, the depth of the node is less than s
            for nodeAndVector in W_key:
                if getAdderDepth(W[nodeAndVector]) < s:
                    P[nodeAndVector] = W[nodeAndVector]
                    W.pop(nodeAndVector)
                    symbol = 1
                    break
            if symbol:
                continue

            P_key = []  # the name of nodes in P
            for key in P:
                P_key.append(key)
            random.shuffle(P_key)

            # When the maximum hamming weight is 3, we can get the predecessors easily.
            if len(W_key) > 1 and max_weight == 3:  # weight = 3
                for key1 in W_key:
                    for key2 in W_key:
                        if key1 != key2:
                            key1XorKey2 = [0 for i in range(0, matrixLength)]  # new predecessor
                            for i in range(0, matrixLength):
                                if W[key1][i] == 1 and W[key2][i] == 1:
                                    key1XorKey2[i] = 1

                            key1Pre = getTwoNodesXor(W[key1], key1XorKey2)
                            key2Pre = getTwoNodesXor(W[key2], key1XorKey2)
                            if (key1XorKey2.count(1) == 2 and key1Pre.count(1) == 1 and key2Pre.count(1) == 1):
                                symbol = 1
                                adder1 = "adder{0}".format(adderCount)  # new adder or predecessor
                                adderCount = adderCount + 1
                                adder2 = "adder{0}".format(adderCount)
                                adderCount = adderCount + 1
                                adder3 = "adder{0}".format(adderCount)
                                adderCount = adderCount + 1
                                V.append(adder1)  # node
                                V.append(adder2)
                                V.append(adder3)
                                P[adder1] = key1XorKey2
                                P[adder2] = key1Pre
                                P[adder3] = key2Pre
                                E.append([adder1, key1])  # edge
                                E.append([adder1, key2])
                                E.append([adder2, key1])
                                E.append([adder3, key2])
                                W.pop(key1)  # delete node from W
                                W.pop(key2)
                                break
                    if symbol == 1:
                        break
            if symbol == 1:
                continue

            # type2, find the node can be calculated by XOR
            sum = []  # calculate all the values from XOR
            for node1 in P_key:
                for node2 in P_key:
                    if P[node1] != P[node2]:
                        vector = [[P[node1][i] ^ P[node2][i] for i in range(0, matrixLength)], node1, node2]  # [value, node1, node2]
                        count = 0
                        for lis in sum:
                            if (lis[1] == node1 and lis[2] == node2) or (lis[2] == node1 and lis[1] == node2):
                                count = 1
                        if count == 0:
                            sum.append(vector)
            random.shuffle(sum)
            for nodeAndVector in W_key:
                nodeEqualSum = 0
                for nodes in sum:
                    if nodes[0] == W[nodeAndVector]:
                        nodeEqualSum = 1  # we find the predecessors of type2
                        E.append([nodes[1], nodeAndVector])
                        E.append([nodes[2], nodeAndVector])
                        W.pop(nodeAndVector)
                        break
                if nodeEqualSum == 1:
                    symbol = 1
                    break
            if symbol == 1:
                continue

            # type3
            for nodeAndVector in W_key:
                for nodeAndVector2 in P_key:
                    nodeNew = getTwoNodesXor(W[nodeAndVector], P[nodeAndVector2])
                    if getAdderDepth(nodeNew) < s:  # we find the new predecessor in type3
                        symbol = 1
                        adder = "adder{0}".format(adderCount)
                        V.append(adder)
                        E.append([adder, nodeAndVector])
                        E.append([nodeAndVector2, nodeAndVector])
                        adderCount = adderCount + 1
                        P[adder] = nodeNew
                        W.pop(nodeAndVector)
                        break
                if symbol == 1:
                    break
            if symbol == 1:
                continue

            # type4
            if len(W_key) > 1:  # when W has one node, this step will be ignored
                for key1 in W_key:
                    for key2 in W_key:
                        if key1 != key2:
                            key1XorKey2 = [0 for i in range(0, matrixLength)]
                            for i in range(0, matrixLength):
                                if W[key1][i] == 1 and W[key2][i] == 1:
                                    key1XorKey2[i] = 1

                            key1Pre = getTwoNodesXor(W[key1], key1XorKey2)  # new node
                            key2Pre = getTwoNodesXor(W[key2], key1XorKey2)
                            if getAdderDepth(key1XorKey2) < s and getAdderDepth(key1Pre) < s and getAdderDepth(
                                    key2Pre) < s:

                                symbol = 1
                                adder1 = "adder{0}".format(adderCount)  # new predecessor
                                adderCount = adderCount + 1
                                adder2 = "adder{0}".format(adderCount)
                                adderCount = adderCount + 1
                                adder3 = "adder{0}".format(adderCount)
                                adderCount = adderCount + 1
                                V.append(adder1)  # new node
                                V.append(adder2)
                                V.append(adder3)
                                P[adder1] = key1XorKey2
                                P[adder2] = key1Pre
                                P[adder3] = key2Pre
                                E.append([adder1, key1])  # new edge
                                E.append([adder1, key2])
                                E.append([adder2, key1])
                                E.append([adder3, key2])
                                W.pop(key1)  # delete
                                W.pop(key2)
                                break
                    if symbol == 1:
                        break
            if symbol == 1:
                continue

            # type5:split
            for key in W_key:
                number_1 = W[key].count(1)  # maximum hamming weight
                number_1_max = 2 ** (s - 1)  # minimum hamming weight
                number_1_min = number_1 - 2 ** (s - 1)
                possibleNumberCount = [i for i in range(number_1_min, number_1_max + 1)]
                random.shuffle(possibleNumberCount)
                numberCount = possibleNumberCount[0]  # the hamming weight of predecessor

                numberSite = []  # the site of 1
                for i in range(0, matrixLength):
                    if W[key][i] == 1:
                        numberSite.append(i)
                random.shuffle(numberSite)
                newNode1 = [0 for i in range(0, matrixLength)]
                for i in range(0, numberCount):
                    newNode1[numberSite[i]] = 1
                newNode2 = [0 for i in range(0, matrixLength)]
                for i in range(0, matrixLength):
                    if (W[key][i] == 1) and (newNode1[i] == 0):
                        newNode2[i] = 1

                # # type5'
                # add_one_in_node_list = []
                # for i in range(0, matrixLength):
                #     if i not in numberSite:
                #         add_one_in_node_list.append(i)
                # random.shuffle(add_one_in_node_list)
                # add_one_random = [0, 1]
                # if (number_1 == 5 and newNode1.count(1) != 4 and newNode2.count(1) != 4) or (
                #         number_1 == 6 and newNode1.count(1) != 4 and newNode2.count(1) != 4):
                #     random.shuffle(add_one_random)
                #     if add_one_random[0] == 1:
                #         add_one_site = add_one_in_node_list[0]
                #         newNode1[add_one_site] = 1
                #         newNode2[add_one_site] = 1

                # find
                symbol = 1
                adder1 = "adder{0}".format(adderCount)
                adderCount = adderCount + 1
                adder2 = "adder{0}".format(adderCount)
                adderCount = adderCount + 1
                V.append(adder1)
                V.append(adder2)
                E.append([adder1, key])
                E.append([adder2, key])
                P[adder1] = newNode1
                P[adder2] = newNode2
                W.pop(key)
                break
            if symbol == 1:
                continue

        s = s - 1  # to pre-depth

        if s > 1:  # from W to P
            W = copy.deepcopy(P)
            P = dict()

    # now we have s=1
    for key in P:  # P has some nodes which have hamming weight 2
        if P[key].count(1) == 1:  # this is the input node
            V.remove(key)
            adderDeleted = adderDeleted + 1
            number = -1
            for i in range(0, len(P[key])):
                if P[key][i] == 1:
                    number = i
                    break
            for nodes in E:
                if nodes[0] == key:
                    nodes[0] = 'iput{}'.format(number)
        else:  # the node has hamming weight 2
            for i in range(0, len(P[key])):
                if P[key][i] == 1:
                    node = 'iput{}'.format(i)
                    E.append([node, key])

    return run(V, E)


def run(V, E):  # the logic of the function comes from [] and we implemented it by ourselves

    def get_bi(B, E, D):
        if len(B) == 0:
            return -1
        for i in range(0, len(B)):
            bi = B[i]
            for j in range(0, len(E)):
                if E[j][1] == bi:
                    if D[E[j][0]] == -1:
                        break
            else:
                break
        return bi

    D = dict()
    B = []
    addersNumber = 0
    for node in V:
        if node[0] == 'a':
            addersNumber = addersNumber + 1
        if node[0] == 'i':
            D[node] = 0
        else:
            D[node] = -1
            B.append(node)

    z = 0

    while len(B) != 0:
        bi = get_bi(B, E, D)
        S = []
        for i in range(0, len(E)):
            if E[i][1] == bi:
                S.append(E[i])
        while len(S) != 0:
            if len(S) == 1:
                if S[0][0] not in V:
                    V.append(S[0][0])
                if S[0] not in E:
                    E.append(S[0])
                D[bi] = D[S[0][0]] + 1
                del S[0]
            else:
                sorted(S, key=(lambda x: D[E[i][0]]))
                # print("sorted S:{}".format(S))
                s1 = S[0]
                s2 = S[1]
                del S[0:2]
                if len(S) == 0:
                    if s1[0] not in V:
                        V.append(s1[0])
                    if s2[0] not in V:
                        V.append(s2[0])
                    if s1 not in E:
                        E.append(s1)
                    if s2 not in E:
                        E.append(s2)
                    D[bi] = max(D[s1[0]], D[s2[0]]) + 1
                else:
                    z = z + 1
                    Az = 'adder{}'.format(addersNumber + z - 1)
                    V.append(Az)
                    # print("V:{}".format(V))
                    E.append([s1[0], Az])
                    E.append([s2[0], Az])
                    if s1 in E:
                        E.remove(s1)
                    if s2 in E:
                        E.remove(s2)
                    # print("E:{}".format(E))
                    S.append([Az, bi])
                    D[Az] = max(D[s1[0]], D[s2[0]]) + 1
        B.remove(bi)
    num = 0
    for node in V:
        if node[0] == 'a':
            num = num + 1
    result = [num, V, E, D]
    return result


if __name__ == "__main__":

    # # SmallScale_AES
    # matrix = [
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    #     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    #     [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    #     [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #     [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    #     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    #     [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #     [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #     [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    #     [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    #     [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    #     [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # ]

    matrix = []

    with open('matrix.txt', 'r') as f:
        line = f.readline().replace('\n', '')
        length = len(line)

        while line:
            num = []
            for i in range(0, length):
                num.append(int(line[i]))
            matrix.append(num)
            line = f.readline()

    theMaxNum = 2000

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
                print("min now：{}".format(result[0]))
                minnum = result[0]
                minV.append(result[1])
                minE.append(result[2])
                minD.append(result[3])
            else:
                times = 1
                print("min now：{}".format(result[0]))
                minnum = result[0]
                minV = []
                minE = []
                minD = []
                minV.append(result[1])
                minE.append(result[2])
                minD.append(result[3])

    print("min：{}".format(minnum))  # the minmum XOR gates
    print(minV)  # nodes set
    print(minE)  # edges set
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
    print("times：{}".format(times))
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
