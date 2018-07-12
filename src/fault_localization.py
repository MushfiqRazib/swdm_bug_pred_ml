#
# file fault_localization.py
# author: Muhammad Mushfiqur Rahman
# Email:mushfiq.rahman@tum.de
# date 2018-05-11

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
import re
import os
from operator import itemgetter
from configuration import Configuration
from file_loader import FileLoader


class FaultLocalization():
    def __init__(self, pathdir):
        self.conf = Configuration(pathdir)
        self.loader = FileLoader()
        self.num_of_failed_test_cases_cover_statement_Ncf = 0
        self.num_of_failed_test_cases_not_cover_statement_Nuf = 0
        self.num_of_successful_test_cases_cover_statement_Ncs = 0
        self.num_of_successful_test_cases_Ns = 0
        self.num_of_failed_test_cases_Nf = 0
        self.suspicious_values = []
        self.distinct_values = []
        self.suspicious_path = os.path.join(self.conf.ROOT_PATH, 'suspiciousness_ranking/')
        if not os.path.exists(self.suspicious_path):
            self.conf.handle_dir(self.suspicious_path)

    def update_values(self):
        self.num_of_failed_test_cases_cover_statement_Ncf = 0
        self.num_of_failed_test_cases_not_cover_statement_Nuf = 0
        self.num_of_successful_test_cases_cover_statement_Ncs = 0
        self.num_of_successful_test_cases_Ns = 0
        self.num_of_failed_test_cases_Nf = 0

    def suspicious_matrix_by_dstar(self, mat_arr):
        mat = np.array(mat_arr)
        #print(mat.shape)
        #print(mat)
        col = mat.shape[1] - 1
        #print(col)
        self.update_values()
        del self.suspicious_values[:]

        for i in range(0, col):
            self.update_values()
            for j in range(0, mat.shape[0]):
                if mat[j][col] == 0: # for fail test case
                    if mat[j][i] == 1:
                        self.num_of_failed_test_cases_cover_statement_Ncf += 1
                    if mat[j][i] == 0:
                        self.num_of_failed_test_cases_not_cover_statement_Nuf += 1

                if mat[j][col] == 1: # for pass test case
                    if mat[j][i] == 1:
                        self.num_of_successful_test_cases_cover_statement_Ncs += 1

            #print(self.num_of_failed_test_cases_cover_statement_Ncf)
            #print(self.num_of_successful_test_cases_cover_statement_Ncs)
            sum = self.num_of_failed_test_cases_not_cover_statement_Nuf + self.num_of_successful_test_cases_cover_statement_Ncs
            #print(sum)
            if sum == 0:
                dstar_value = 0
            else:
                dstar_value = pow(self.num_of_failed_test_cases_cover_statement_Ncf, 2)/sum
            #print('DStar value for ' + str(i) + ' th col value: ' + str(dstar_value))
            self.suspicious_values.append(dstar_value)

    def generate_ranking(self):
        susp_arr = np.array(self.suspicious_values)
        print('---processing ranking---')
        self.distinct_values = []
        dist_arr = np.unique(susp_arr)
        # dist_array needs to reverse for making descending order
        self.distinct_values = dist_arr[::-1]
        #print(self.distinct_values)
        #for x in range(distinct_values.shape[0]):

    def print_suspiciousness_ranking_table(self, filename):
        print('writing csv for :', filename)
        susp_arr = np.array(self.suspicious_values)
        with open(self.suspicious_path + filename +'.csv', 'w') as csvfile:
            columnTitleRow = "Method_Call_No,Suspiciousness,Ranking\n"
            csvfile.write(columnTitleRow)
            for i in range(0, susp_arr.shape[0]):
                for y in range(0, len(self.distinct_values)):
                    if susp_arr[i] == self.distinct_values[y]:
                        row = str(i+1) + ","+ str(susp_arr[i]) +"," + str(y+1) + "\n"
                        csvfile.write(row)
                        #print('DStar value for ' + str(i+1) + ' th col value: ' + str(susp_arr[i]) + ' Ranking - ' + str(y+1))

    def calculate_suspiciousness(self):
        for i in range(0, len(self.conf.PROJECTS_DATA_PATH)):
            for subdir, dirs, files in sorted(os.walk(self.conf.PROJECTS_DATA_PATH[i])):
                for file in sorted(files):
                    filepath = os.path.join(subdir, file)

                    if file == 'matrix':
                        print(filepath)
                        mat = self.loader.load_coverage_file(filepath)
                        self.suspicious_matrix_by_dstar(mat)
                        self.generate_ranking()
                        buggy_version = re.findall('\d+', filepath)
                        filename = self.conf.PROJECTS_ID[i] + '_' + buggy_version[0]
                        self.print_suspiciousness_ranking_table(filename)
        #mat = self.load_matrix()
        #mat_arr = np.asarray(mat)
        print('---Suspicious Ranking of Matrix Done----')
