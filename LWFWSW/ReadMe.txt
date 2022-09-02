Towards Low-Latency Implementation of Linear Layers in FSE 2022


In this folder, there are a total of 6 files and 1 folder

matrix.txt - the matrix we need to optimize.
Algorithm.py - the algorithm for the backward framework.
main.py - the process for deal with the output.
run.py - the main process to run our algorithm for multiprocessing in python.

This program requires Python3.

In main.py, we need to choose one method (1. from Algorithm or 2. from AlgorithmNorandom   import getGraph). Type 1 may have the larger search space while Type 2 has less running time. 
Type 2 can also find the 103/3 circuit for AES MixColumns.

An example is shown as follows.
	matrix.txt - a given matrix
		0001100110001000
		1001110101000100
		0100011000100010
		0010001100010001
		1000000110011000
		0100100111010100
		0010010001100010
		0001001000110001
		1000100000011001
		0100010010011101
		0010001001000110
		0001000100100011
		1001100010000001
		1101010001001001
		0110001000100100
		0011000100010010

	We create a folder 'result'.
	Then, we run 'python3 run.py' to optimize the matrix.
	All the results can be seen in the folder 'result'.
