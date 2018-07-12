#
# file test_suite_matrix_generation.py
# author: Muhammad Mushfiqur Rahman
# Email:mushfiq.rahman@tum.de
# date 2018-06-22

from __future__ import division
from os import listdir, makedirs
from os.path import isfile, join, dirname, exists, basename
import os
import shutil
import itertools
import xml.etree.ElementTree as ET
import numpy as np
import math
import scipy.misc
import colorsys
import csv
import re
from operator import itemgetter
from configuration import Configuration
from file_loader import FileLoader

class TestSuiteMatrix():
    def __init__(self, pathdir):
        self.conf = Configuration(pathdir)
        self.loader = FileLoader()
        self.total_pass_test_cases = 0
        self.total_fail_test_cases = 0
        self.total_runtime_of_pass_test_cases = 0
        self.total_runtime_of_fail_test_cases = 0
        self.test_suite_activity_matrix_density = 0
        self.test_suite_matrix_diversity = 0
        self.test_suite_matrix_uniqueness = 0
        self.test_suite_matrix_ddu = 0
        self.test_suite_matrix_sparsity = 0
        self.test_suite_matrix_density = 0

        self.test_suite_list = []
        self.test_suite_list_chart = []
        self.test_suite_list_lang = []
        self.test_suite_list_math = []
        self.test_suite_list_time = []
        self.test_suite_list_closure = []
        self.test_suite_list_mockito = []

    # calculate below metrics according to test suite paper.
    # Paper Title: "A Test-suite Diagnosability Metric for Spectrum-based Fault Localization Approaches"
    # self.test_suite_matrix_density,
    # self.test_suite_matrix_sparsity,
    # self.test_suite_activity_matrix_density,
    # self.test_suite_matrix_diversity,
    # self.test_suite_matrix_uniqueness,
    # self.test_suite_matrix_ddu
    def calculate_test_suite_matrix_ddu(self, matrix):
        mat_arr = np.asarray(matrix)
        row = mat_arr.shape[0]
        col = mat_arr.shape[1] - 1 # excluding pass/fail column
        sum = 0
        sparsity_sum = 0
        for i in range(0, row):
            for j in range(0, col):
                if mat_arr[i][j] == 1:
                    sum += mat_arr[i][j]
                if mat_arr[i][j] == 0:
                    sparsity_sum += 1

        self.test_suite_matrix_density  = sum/(row * col)
        #The number of zero-valued elements divided by the total number of elements is called the sparsity of the matrix
        #Conceptually, sparsity corresponds to systems that are loosely coupled.
        self.test_suite_matrix_sparsity = sparsity_sum/(row * col)
        # DDU metrics calculation
        # activity matrix density calculation
        self.test_suite_activity_matrix_density = 1 - abs(1 - 2 * self.test_suite_matrix_density)
        modified_matrix = np.delete(mat_arr, mat_arr.shape[1] - 1, 1)
        dt = np.dtype((np.void, modified_matrix.dtype.itemsize * modified_matrix.shape[1]))
        contg_arr = np.ascontiguousarray(modified_matrix).view(dt)
        unq, cnt = np.unique(contg_arr, return_counts=True)

        # calculate matrix diversity and matrix uniqueness.
        no_of_test_share_similar_activity = 0
        for i in range(0, len(cnt)):
            no_of_test_share_similar_activity += cnt[i] * (cnt[i] - 1)

        if no_of_test_share_similar_activity == 0:
            self.test_suite_matrix_diversity = 1
        else:
            self.test_suite_matrix_diversity = 1 - no_of_test_share_similar_activity/(row * (row-1))
        dt = np.dtype((np.void, modified_matrix.dtype.itemsize * modified_matrix.shape[0]))
        data_f = np.asfortranarray(modified_matrix).view(dt)
        u, c = np.unique(data_f, return_counts=True)
        self.test_suite_matrix_uniqueness = len(c)/col

        # calculate matrix DDU
        self.test_suite_matrix_ddu = self.test_suite_activity_matrix_density * self.test_suite_matrix_diversity * self.test_suite_matrix_uniqueness

    def load_tests_matrix_file(self):
        print('---loading tests matrix file ---')
        for i in range(0, len(self.conf.PROJECTS_ID)):
            for subdir, dirs, files in sorted(os.walk(self.conf.PROJECTS_DATA_PATH[i])):
                for file in sorted(files):
                    filepath = os.path.join(subdir, file)
                    #print(filepath)
                    '''
                    if file == 'tests':
                        tests_list = self.loader.load_tests_file(filepath)
                        tests_arr = np.asarray(tests_list)
                        #print(tests_arr[1][1])
                        pass_fail_col_arr = tests_arr[:, tests_arr.shape[1] - 2]
                        #print(pass_fail_col_arr)
                        pass_fail_time_ns_col_arr = tests_arr[:, tests_arr.shape[1] - 1]
                        #print(pass_fail_time_ns_col_arr)
                        pass_test_case_sec = 0.0
                        fail_test_case_sec = 0.0
                        for x in range(1, len(pass_fail_col_arr)):
                            get_ns = int(pass_fail_time_ns_col_arr[x])
                            if pass_fail_col_arr[x] == 'PASS':
                                pass_test_case_sec = pass_test_case_sec + float(get_ns/1000000000)
                            else:
                                fail_test_case_sec = fail_test_case_sec + float(get_ns/1000000000)
                        #print(pass_test_case_sec)
                        #print(fail_test_case_sec)
                        self.total_runtime_of_pass_test_cases = pass_test_case_sec
                        self.total_runtime_of_fail_test_cases = fail_test_case_sec'''

                    if file == 'matrix':
                        buggy_version = re.findall('\d+', filepath)
                        print('Processing: ' + filepath)
                        mat = self.loader.load_coverage_file(filepath)
                        mat_arr = np.asarray(mat)
                        #print(mat_arr.shape)
                        #print(mat_arr.shape[1])
                        pass_fail_col_arr = mat_arr[:, mat_arr.shape[1] - 1]
                        #print(pass_fail_col_arr)
                        test_case_arr = np.asarray(pass_fail_col_arr)
                        unique_value, unique_counts = np.unique(test_case_arr, return_counts=True)
                        if len(unique_value) == 2:
                            self.total_pass_test_cases = unique_counts[1]
                            self.total_fail_test_cases = unique_counts[0]
                        else:
                            if unique_value[0] == 1:
                                self.total_pass_test_cases = unique_counts[0]
                            else:
                                self.total_fail_test_cases = unique_counts[0]

                        self.calculate_test_suite_matrix_ddu(mat_arr)
                        output_row = [self.conf.PROJECTS_ID[i] + '_' + buggy_version[0],
                                      int(buggy_version[0]),
                                      self.total_pass_test_cases,
                                      self.total_fail_test_cases,
                                      self.test_suite_matrix_density,
                                      self.test_suite_matrix_sparsity,
                                      self.test_suite_activity_matrix_density,
                                      self.test_suite_matrix_diversity,
                                      self.test_suite_matrix_uniqueness,
                                      self.test_suite_matrix_ddu]

                        if self.conf.PROJECTS_ID[i] == 'Chart':
                            self.test_suite_list_chart.append(output_row)
                        elif self.conf.PROJECTS_ID[i] == 'Lang':
                            self.test_suite_list_lang.append(output_row)
                        elif self.conf.PROJECTS_ID[i] == 'Math':
                            self.test_suite_list_math.append(output_row)
                        elif self.conf.PROJECTS_ID[i] == 'Time':
                            self.test_suite_list_time.append(output_row)
                        elif self.conf.PROJECTS_ID[i] == 'Closure':
                            self.test_suite_list_closure.append(output_row)
                        else:
                            self.test_suite_list_mockito.append(output_row)

            print('============== Printing ' + self.conf.PROJECTS_ID[i] + ' Projects Buggy Versions Test Suite Features =================')
            if self.conf.PROJECTS_ID[i] == 'Chart':
                output_sorted_list = sorted(self.test_suite_list_chart, key=itemgetter(1))
                #print(output_sorted_list)
                self.test_suite_list.extend(output_sorted_list)
            if self.conf.PROJECTS_ID[i] == 'Lang':
                output_sorted_list = sorted(self.test_suite_list_lang, key=itemgetter(1))
                #print(output_sorted_list)
                self.test_suite_list.extend(output_sorted_list)
            if self.conf.PROJECTS_ID[i] == 'Math':
                output_sorted_list = sorted(self.test_suite_list_math, key=itemgetter(1))
                #print(output_sorted_list)
                self.test_suite_list.extend(output_sorted_list)
            if self.conf.PROJECTS_ID[i] == 'Time':
                output_sorted_list = sorted(self.test_suite_list_time, key=itemgetter(1))
                #print(output_sorted_list)
                self.test_suite_list.extend(output_sorted_list)
            if self.conf.PROJECTS_ID[i] == 'Closure':
                output_sorted_list = sorted(self.test_suite_list_closure, key=itemgetter(1))
                #print(output_sorted_list)
                self.test_suite_list.extend(output_sorted_list)
            if self.conf.PROJECTS_ID[i] == 'Mockito':
                output_sorted_list = sorted(self.test_suite_list_mockito, key=itemgetter(1))
                #print(output_sorted_list)
                self.test_suite_list.extend(output_sorted_list)
            print('============== Finished Printing ' + self.conf.PROJECTS_ID[i] + ' Projects Buggy Version ================')

    def print_test_suite_matrix_properties(self):
        result_arr = np.array(self.test_suite_list)
        with open(self.conf.ROOT_PATH + 'test_suite_matrix_characteristics.csv', 'w') as csvfile:
            # PassedTestRuntime, FailedTestRuntime,
            columnTitleRow = "ProjectID_BugId, BugId, TotalPassTest, TotalFailTest, MatrixDensity, MatrixSparsity, ActiveMatrixDensity, MatrixDiversity, MatrixUniqueness, MatrixDDU\n"
            csvfile.write(columnTitleRow)
            for i in range(0, result_arr.shape[0]):
                row = str(result_arr[i][0]) + ", " + str(result_arr[i][1]) + ", " + str(result_arr[i][2]) + ", " + str(result_arr[i][3]) + ", " + str(result_arr[i][4]) + ", " + str(result_arr[i][5]) + ", " + str(result_arr[i][6]) + ", " + str(result_arr[i][7]) + ", " + str(result_arr[i][8])  + ", " + str(result_arr[i][9]) + "\n"
                csvfile.write(row)
            print('Test Suite characteristics file is saved.')

    def process_test_suite_properties(self):
        print('---preparing test suite characteristics---')
        #self.test_method()
        self.load_tests_matrix_file()
        self.print_test_suite_matrix_properties()


'''
def test_method(self):
    print('---loading tests matrix file ---')
    mat = self.loader.load_coverage_file('/home/mra/praktikum/projectsdb/method-data/Closure/90/matrix')
    #self.loader.change_tab_with_space('/home/mra/praktikum/projectsdb/method-data/Closure/2/')
    print(len(mat[0]))
    #print(mat[0])
    for i,v in enumerate(mat):
        if(len(v)!=len(mat[0])):
            print(len(v))
            print(v)
            #print('mat[v]', mat[v])
            print('bad element {} at {}'.format(v,i))

    mat_arr = np.asarray(mat)
    #print(mat_arr)
    print(mat_arr.shape)
    self.calculate_test_suite_matrix_ddu(mat_arr)
'''
