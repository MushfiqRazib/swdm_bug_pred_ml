from __future__ import division
from os import listdir, makedirs
from os.path import isfile, join, dirname, exists, basename
import shutil
import itertools
import xml.etree.ElementTree as ET
import numpy as np
import math
import scipy.misc
import colorsys
import csv


class FileLoader():
    def __init__(self):
        success = False

    # load matrix, tests, spectra file...
    def load_file_supiciousness(self, path):
        #print('filepath >', path)
        with open(path, "r") as lines:
            array = []
            matrix_arr = []
            for line in lines:
                array.append(line.strip().split(' '))


            matrix_array = np.asarray(array)
            for k in matrix_array:
                matrix_arr.append([int(v) for v in k])

            #matrix_array = np.asarray(array)
            #matrix_array = map(int, matrix_array)
            #modified_matrix=  list(map(int, array))
            #return modified_matrix
            return matrix_arr

    # load matrix, tests, spectra file...
    def load_coverage_file(self, path):
        #print('filepath >', path)
        with open(path, "r") as lines:
            array = []
            matrix_arr = []
            for line in lines:
                array.append(line.strip().split(' '))

            matrix_array = np.asarray(array)
            #print(matrix_array[:, 0])

            if matrix_array[0][matrix_array.shape[1] - 1] == '+':
                mask = matrix_array[:, matrix_array.shape[1] - 1] == '+'
                matrix_array[:, matrix_array.shape[1] - 1][mask] = 1
                mask = matrix_array[:, matrix_array.shape[1] - 1] == '-'
                matrix_array[:, matrix_array.shape[1] - 1][mask] = 0

            #print(matrix_array[:, matrix_array.shape[1] -1 ])
            for k in matrix_array:
                matrix_arr.append([int(v) for v in k])

            #modified_matrix= [map(int, x) for x in matrix_array]
            #print(matrix_arr)
            return matrix_arr
            #return matrix_array

    # load tests file...
    def load_tests_file(self, path):
        with open(path, "r") as lines:
            line_list = []
            for line in lines:
                line_list.append(line.strip().split(','))

            matrix_array = np.array(line_list)
            return matrix_array

    def change_tab_with_space(self, filepath):
        with open(filepath+'matrix') as fin, open(filepath + 'matrix1', 'w') as fout:
            for line in fin:
                fout.write(line.replace('\t', ' '))
