#
# file static_metrics_parsing.py
# author: Muhammad Mushfiqur Rahman
# Email:mushfiq.rahman@tum.de
# date 2018-05-29

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
import pydotplus
import pyparsing
import json
from graphviz import Source
from operator import itemgetter
from configuration import Configuration
from file_loader import FileLoader

class StaticMetricsParser():
    def __init__(self, pathdir):
        self.conf = Configuration(pathdir)
        self.loader = FileLoader()
        self.total_pass_test_cases = 0
        self.static_metrics_list = []
        self.chart_list = []
        self.math_list = []
        self.time_list = []
        self.closure_list = []
        self.lang_list = []
        self.mockito_list = []
        self.static_feature_columns = ['Abstractness', 'Afferent Couplings', 'Average Block Depth',
                                       'Average Cyclomatic Complexity', 'Average Depth of Inheritance Hierarchy',
                                       'Average Lines Of Code Per Method', 'Average Number of Constructors Per Type',
                                       'Average Number of Fields Per Type','Average Number of Methods Per Type',
                                       'Average Number of Parameters', 'Average Number of Subtypes',
                                       'Comments Ratio', 'Difficulty', 'Distance', 'Efferent Couplings', 'Effort',
                                       'Instability', 'Lines of Code', 'Number of Characters', 'Number of Comments',
                                       'Number of Constructors', 'Number of Fields', 'Number of Lines',
                                       'Number of Methods', 'Number of Operands', 'Number of Operators',
                                       'Number of Packages', 'Number of Semicolons', 'Number of Types',
                                       'Number of Unique Operands', 'Number of Unique Operators', 'Program Length',
                                       'Program Vocabulary', 'Program Volume', 'Number of delivered bugs', 'Weighted Methods']


    def process_static_metrics_from_file(self):
        print('processing CodePro static metrics file from...')
        for i in range(0, len(self.conf.STATIC_METRICS_PROJECTS_ID)):
            for subdir, dirs, files in sorted(os.walk(self.conf.STATIC_METRICS_PROJECTS_PATH[i])):
                for file in sorted(files):
                    filepath = os.path.join(subdir, file)
                    print('processing...> ', filepath)
                    #print(file)
                    fname = file.replace(".csv", "")
                    fname_parts = fname.split('_', 1)
                    buggy_version = int(fname_parts[1])
                    projectname = fname_parts[0]
                    data_list = []
                    with open(filepath, 'r') as f:
                        reader = csv.reader(f)
                        next(reader) # skip header
                        next(reader)
                        data = []
                        data.append(projectname)
                        data.append(buggy_version)
                        for row in reader:
                            data.append(row)
                            # Halstead´s metrics - Number of delivered bugs calculation
                            if row[0] == 'Program Volume':
                                colname = 'Number of delivered bugs'
                                cal = float(row[1].replace(',', ''))
                                data.append([colname, str(round(cal/3000, 2))])
                                print([colname, round(cal/300, 2)])
                        #self.static_metrics_list[buggy_version-1] == data
                        if self.conf.STATIC_METRICS_PROJECTS_ID[i] == 'Chart':
                            self.chart_list.append(data)
                        if self.conf.STATIC_METRICS_PROJECTS_ID[i] == 'Lang':
                            self.lang_list.append(data)
                        if self.conf.STATIC_METRICS_PROJECTS_ID[i] == 'Math':
                            self.math_list.append(data)
                        if self.conf.STATIC_METRICS_PROJECTS_ID[i] == 'Time':
                            self.time_list.append(data)
                        if self.conf.STATIC_METRICS_PROJECTS_ID[i] == 'Closure':
                            self.closure_list.append(data)

                if self.conf.STATIC_METRICS_PROJECTS_ID[i] == 'Chart':
                    output_sorted_list = sorted(self.chart_list, key=itemgetter(1))
                    self.static_metrics_list.extend(output_sorted_list)
                if self.conf.STATIC_METRICS_PROJECTS_ID[i] == 'Lang':
                    output_sorted_list = sorted(self.lang_list, key=itemgetter(1))
                    self.static_metrics_list.extend(output_sorted_list)
                if self.conf.STATIC_METRICS_PROJECTS_ID[i] == 'Math':
                    output_sorted_list = sorted(self.math_list, key=itemgetter(1))
                    self.static_metrics_list.extend(output_sorted_list)
                if self.conf.STATIC_METRICS_PROJECTS_ID[i] == 'Time':
                    output_sorted_list = sorted(self.time_list, key=itemgetter(1))
                    self.static_metrics_list.extend(output_sorted_list)
                if self.conf.STATIC_METRICS_PROJECTS_ID[i] == 'Closure':
                    output_sorted_list = sorted(self.closure_list, key=itemgetter(1))
                    self.static_metrics_list.extend(output_sorted_list)

    def print_static_metrics(self):
        with open(self.conf.ROOT_PATH + 'static_metrics.csv', 'w') as csvfile:
            columnTitleRow = 'ProjectID, BugId'
            for i in range(len(self.static_feature_columns)):
                columnTitleRow +=  ', ' + self.static_feature_columns[i].replace(' ', '')
            csvfile.write(columnTitleRow+'\n')
            row = ''
            for i in range(len(self.static_metrics_list)):
                row += str(self.static_metrics_list[i][0]) + ', ' + str(self.static_metrics_list[i][1])
                for c in range(len(self.static_feature_columns)):
                    for x in range(2, len(self.static_metrics_list[i])):
                        if self.static_feature_columns[c] == self.static_metrics_list[i][x][0]:
                            text = str(self.static_metrics_list[i][x][1].replace(',', ''))
                            row += ', ' + text
                            break
                row += '\n'
            #print(row)
            csvfile.write(row)
            print('Static metrics file -> static_metrics.csv is saved.')

    def parsing_static_metrics(self):
        self.process_static_metrics_from_file()
        self.print_static_metrics()
