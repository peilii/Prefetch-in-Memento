#!/bin/bash

MALLOC_PYTHON_LIBRARY=/home/ziqiw/data_disk_2/cpython/mallocless_python_hook/libmallocless_python_hook.so LD_LIBRARY_PATH=/home/ziqiw/data_disk_2/cpython/mallocless_python_hook/ MALLOCLESS_LIB=/home/ziqiw/data_disk_2/cpython/mallocless_python_hook/libmallocless_python_hook.so /home/ziqiw/data_disk_2/cpython/python microbench.py $1