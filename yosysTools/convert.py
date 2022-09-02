'''
t0 = x1 + x9
t1 = x4 + t0
y15 = x15 + t1
t3 = x2 + x14
t4 = x4 + t3
y11 = x11 + t4
t6 = x5 + t4
y5 = t1 + t6
t8 = x2 + x10
t9 = x12 + t8
y12 = x5 + t9
t11 = x0 + x15
t12 = x5 + t11
y0 = x11 + t12
t14 = x6 + x8
t15 = x1 + t14
y1 = x12 + t15
t17 = x3 + t12
t18 = x12 + t17
y8 = x8 + t18
t20 = x6 + t17
y6 = y12 + t20
t22 = x0 + t18
t23 = y0 + t22
y7 = x7 + t23
t25 = y11 + t22
y3 = y12 + t25
t27 = x1 + x13
t28 = y1 + t27
y13 = t23 + t28
t30 = y8 + t22
t31 = t0 + t30
y9 = t28 + t31
t33 = t1 + t27
y4 = t31 + t33
t35 = x2 + x7
y2 = t33 + t35
t37 = t4 + y2
y14 = y4 + t37
t39 = t1 + t37
y10 = t8 + t39
'''

'''
t0 = x1 + x9
t1 = x4 + t0
t2 = x15 + t1
t3 = x2 + x14
t4 = x4 + t3
t5 = x11 + t4
t6 = x5 + t4
t7 = t1 + t6
t8 = x2 + x10
t9 = x12 + t8
t10 = x5 + t9
t11 = x0 + x15
t12 = x5 + t11
t13 = x11 + t12
t14 = x6 + x8
t15 = x1 + t14
t16 = x12 + t15
t17 = x3 + t12
t18 = x12 + t17
t19 = x8 + t18
t20 = x6 + t17
t21 = t10 + t20
t22 = x0 + t18
t23 = t13 + t22
t24 = x7 + t23
t25 = t5 + t22
t26 = t10 + t25
t27 = x1 + x13
t28 = t16 + t27
t29 = t23 + t28
t30 = t19 + t22
t31 = t0 + t30
t32 = t28 + t31
t33 = t1 + t27
t34 = t31 + t33
t35 = x2 + x7
t36 = t33 + t35
t37 = t4 + t36
t38 = t34 + t37
t39 = t1 + t37
t40 = t8 + t39
'''
inputs = []
#read in the file
with open('/Users/mehmetalidemir/Downloads/matricesrnbp.txt', 'r') as f:
    #txt split by "----------"
    input = []
    for line in f:
        if line == "----------\n":
            inputs.append(input)
            input = []
        else:
            input.append(line.replace("\n", "").replace("+", "").replace("=", "").replace("  ", " "))
print(inputs)
inputs.pop(0)
#print(inputs[0])

'''
['t0 = x1 + x9', 't1 = x4 + t0', 'y15 = x15 + t1', 't3 = x2 + x14', 't4 = x4 + t3', 'y11 = x11 + t4', 't6 = x5 + t4', 'y5 = t1 + t6', 't8 = x2 + x10', 't9 = x12 + t8', 'y12 = x5 + t9', 't11 = x0 + x15', 't12 = x5 + t11', 'y0 = x11 + t12', 't14 = x6 + x8', 't15 = x1 + t14', 'y1 = x12 + t15', 't17 = x3 + t12', 't18 = x12 + t17', 'y8 = x8 + t18', 't20 = x6 + t17', 'y6 = y12 + t20', 't22 = x0 + t18', 't23 = y0 + t22', 'y7 = x7 + t23', 't25 = y11 + t22', 'y3 = y12 + t25', 't27 = x1 + x13', 't28 = y1 + t27', 'y13 = t23 + t28', 't30 = y8 + t22', 't31 = t0 + t30', 'y9 = t28 + t31', 't33 = t1 + t27', 'y4 = t31 + t33', 't35 = x2 + x7', 'y2 = t33 + t35', 't37 = t4 + y2', 'y14 = y4 + t37', 't39 = t1 + t37', 'y10 = t8 + t39']
'''

for i in range(len(inputs)):
    for j in range(len(inputs[i])):
        inputs[i][j] = inputs[i][j].split(" ")
#remove + and =

#convert y to t
for a in range(len(inputs)):
    for j in range(len(inputs[a])):
        if inputs[a][j][0].find("y") != -1:
            findElement = inputs[a][j][0]
            inputs[a][j][0] = "t" + str(j)
            replaceElement = inputs[a][j][0]
            for i in range(len(inputs[a])):
                for k in range(len(inputs[a][i])):
                    if inputs[a][i][k] == findElement:
                        inputs[a][i][k] = replaceElement

for i in range(len(inputs[0])):
        print(inputs[0][i])
newFile = open("/Users/mehmetalidemir/Downloads/matricesrnbp2.txt", "w")
for i in range(len(inputs)):
    for j in range(len(inputs[i])):
        newFile.write(inputs[i][j][0] + " = " + inputs[i][j][1] + " + " + inputs[i][j][2] + "\n")
    newFile.write("----------\n")
newFile.close()





