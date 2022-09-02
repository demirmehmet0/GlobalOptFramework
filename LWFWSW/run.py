from multiprocessing import cpu_count
import os

number_cpu = cpu_count()
# number_cpu = 64

for i in range(number_cpu):
    # os.system("python3 main_1.py >./result/result{}.txt &".format(i))
    os.system("python3 main.py >./result/result{}.txt &".format(i))