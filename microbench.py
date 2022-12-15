import os
from ctypes import *
if os.getenv("MALLOCLESS_LIB", None) is None:
    raise ValueError("Did not find environmental variable MALLOCLESS_LIB")
libmallocless = CDLL(os.getenv("MALLOCLESS_LIB", None))

# Using byte string, not unicode, for printf
libmallocless.zsim_magic_op_print_str(b"---------------------------------------------------------------\n")

import random
random.seed(100)

import sys
sys.path.append("/home/ziqiw/.local/lib/python3.8/site-packages")

libmallocless.zsim_magic_op_start_sim()

size = 64

def workload1():
    # Do some simple computation
    x = [random.random() for i in range(size)]
    for i in range(size):
        x[i] = i * i

def workload2():
    # Sort a list of random numbers
    x = [random.random() for i in range(size)]
    x.sort()

def workload3():
    # Perform matrix multiplication
    A = [[random.random() for i in range(size)] for j in range(size)]
    B = [[random.random() for i in range(size)] for j in range(size)]
    C = [[0 for i in range(size)] for j in range(size)]
    for i in range(size):
        for j in range(size):
            for k in range(size):
                C[i][j] += A[i][k] * B[k][j]

workload = int(sys.argv[2]) if len(sys.argv) > 2 else 1
if workload == 1:
    workload1()
elif workload == 2:
    workload2()
else:
    workload3()


libmallocless.zsim_magic_op_end_sim()