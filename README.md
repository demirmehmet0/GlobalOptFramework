#### If you use our framework, please cite this paper as: M. K. Pehlivanoglu and M. A. Demir, "A Framework for Global Optimization of Linear Layers in SPN Block Ciphers," 2022 15th International Conference on Information Security and Cryptography (ISCTURKEY), 2022, pp. 13-18, doi: 10.1109/ISCTURKEY56345.2022.9931793.


In this folder, there are a total of 2 files and 6 folders


Each of these folders represents an algorithm.


The parameter file must be edited for the framework to work.
Values ​​in parameters.txt should be set as:


ALGORITHM - The algorithm to be compiled 

        ALGORITHM=1 - XZLBZ                             -> (MATRIX_PATH, ITERATION)
        
        ALGORITHM=2 - BP                                -> (MATRIX_PATH, NUM_MATRICES, THRESHOLD, DEPTH)
        
        ALGORITHM=3 - RNBP                              -> (MATRIX_PATH, ITERATION)
        
        ALGORITHM=4 - A1                                -> (MATRIX_PATH, ITERATION)
        
        ALGORITHM=5 - A2                                -> (MATRIX_PATH, ITERATION)
        
        ALGORITHM=6 - Paar1                             -> (MATRIX_PATH, NUM_MATRICES, THRESHOLD)
        
        ALGORITHM=7 - Paar2                             -> (MATRIX_PATH, NUM_MATRICES, THRESHOLD)
        
        ALGORITHM=8 - LWFWSW                            -> (MATRIX_PATH, ITERATION)
        
        ALGORITHM=9 - BFI                               -> (MATRIX_PATH, ITERATION)
        
        ALGORITHM=10 - BFI-Paar1                        -> (MATRIX_PATH, ITERATION)
        
        ALGORITHM=11 - BFI-RPaar1                       -> (MATRIX_PATH, ITERATION)
        
        ALGORITHM=12 - BFI-BP                           -> (MATRIX_PATH, ITERATION)
        
        ALGORITHM=13 - BFI-A1                           -> (MATRIX_PATH, ITERATION)
        
        ALGORITHM=14 - BFI-A2                           -> (MATRIX_PATH, ITERATION)
        
        ALGORITHM=15 - BFI-RNBP                         -> (MATRIX_PATH, ITERATION)
        
        ALGORITHM=16 - BFI-BP-depthConstrained          -> (MATRIX_PATH, NUM_MATRICES, THRESHOLD, DEPTH, BFI)

MATRIX_PATH - The path to the matrix file

        MATRIX_PATH=path/to/matrix/file
        

ITERATION - The number of iterations to be performed

        ITERATION=10
        
An example command will be:

        python3 main.py


The matrix formats to be sent to the algorithms are given in the matrices folder.

The source code of BP algorithm in our framework is provided by the repository given in https://github.com/siweisun/involutory_mds/tree/master/Code_for_BoyarSLP

The source code of Paar's algorithm(Paar1-Paar2) in our framework is provided by the repository given in https://github.com/rub-hgi/shorter_linear_slps_for_mds_matrices

The source code of BFI's algorithm(Algorithm-9-10-11-12-13-14-15) in our framework is provided by the repository given in https://github.com/DaLin10512/framework

The source code of LWFWSW's algorithm in our framework is provided by the repository given in https://github.com/QunLiu-sdu/Towards-Low-Latency-Implementation

The source code of A1-A2-RNBP's algorithm in our framework is provided by the repository given in https://github.com/thomaspeyrin/XORreduce

The source code of XZLBZ's algorithm in our framework is provided by the repository given in https://github.com/xiangzejun/Optimizing_Implementations_of_Linear_Layers

