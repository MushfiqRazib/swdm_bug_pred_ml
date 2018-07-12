#
# file ranking_class_label.py
# author: Muhammad Mushfiqur Rahman
# Email:mushfiq.rahman@tum.de
# date 2018-06-11

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
import matplotlib.pyplot as plt
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

class SuspiciousRankingClassLabel():
    def __init__(self, pathdir):
        self.conf = Configuration(pathdir)
        self.loader = FileLoader()
        self.NO_VALUE = 'Unknown'
        self.rank_list = []
        self.class_label = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
        self.numeric_class_label = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.class_label_6 = ['A', 'B', 'C', 'D', 'E', 'F']
        self.numeric_class_label_6 = [1, 2, 3, 4, 5, 6]

    def get_ranking_by_faultmethod(self, projectName, bug_version, spectraLineNum):
        rankPath = os.path.join(self.conf.ROOT_PATH, 'suspiciousness_ranking/' + projectName + '_' + str(bug_version) + '.csv')
        #print('p>' + projectName + ' b>' + bug_version + ' l>' + str(spectraLineNum))
        if spectraLineNum == None:
            suspicious_sum_avg = 0
            ranking_sum_avg = 0
            lastlinenum = 0
            with open(rankPath, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                next(reader)
                for lineno, row in enumerate(reader):
                    suspicious_sum_avg += float(row[1])
                    ranking_sum_avg += int(row[2])
                    lastlinenum = lineno
            #print('suspicious_sum_avg>', suspicious_sum_avg)
            #print('ranking_sum_avg>', ranking_sum_avg)
            #print('lastlinenum>', lastlinenum)
            output = [projectName, int(bug_version), round((suspicious_sum_avg/lastlinenum),2), int(ranking_sum_avg/lastlinenum)]
            return output
        else:
            with open(rankPath, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for lineno, row in enumerate(reader):
                    if lineno == spectraLineNum:
                        output = [projectName, int(bug_version), round(float(row[1]), 2), int(row[2])]
                        return output

    def get_line_number_from_spectra(self, projectName, bug_version, faultMethodName):
        #print('get_line_number_from_spectra- project>' + projectName + ' id> ' + str(bug_version) + ' methodName> ' + faultMethodName)
        filepath = os.path.join(self.conf.ROOT_PATH, projectName + '/' + str(bug_version) + '/spectra')
        with open(filepath, 'r') as spectra:
             for num, line in enumerate(spectra, 1):
                 if faultMethodName in line.strip():
                     return num

    def get_class_label_6(self, val):
        if val <= 10:
            return self.class_label_6[0].strip()
        if val > 10 and val <= 20:
            return self.class_label_6[1].strip()
        if val > 20 and val <= 30:
            return self.class_label_6[2].strip()
        if val > 30 and val <= 40:
            return self.class_label_6[3].strip()
        if val > 40 and val <= 50:
            return self.class_label_6[4].strip()
        if val >50:
            return self.class_label_6[5].strip()

    def get_class_label_11(self, val):
        if val<=10:
            return self.class_label[0].strip()
        if val> 10 and val<=20:
            return self.class_label[1].strip()
        if val> 20 and val<=30:
            return self.class_label[2].strip()
        if val> 30 and val<=40:
            return self.class_label[3].strip()
        if val> 40 and val<=50:
            return self.class_label[4].strip()
        if val> 50 and val<=60:
            return self.class_label[5].strip()
        if val> 60 and val<=70:
            return self.class_label[6].strip()
        if val> 70 and val<=80:
            return self.class_label[7].strip()
        if val> 80 and val<=90:
            return self.class_label[8].strip()
        if val> 90 and val<=100:
            return self.class_label[9].strip()
        if val> 100:
            return self.class_label[10].strip()

    def get_numeric_class_label_6(self, val):
        if val <= 10:
            return self.numeric_class_label_6[0]
        if val > 10 and val <= 20:
            return self.numeric_class_label_6[1]
        if val > 20 and val <= 30:
            return self.numeric_class_label_6[2]
        if val > 30 and val <= 40:
            return self.numeric_class_label_6[3]
        if val > 40 and val <= 50:
            return self.numeric_class_label_6[4]
        if val > 50:
            return self.numeric_class_label_6[5]

    def get_numeric_class_label_11(self, val):
        if val<=10:
            return self.numeric_class_label[0]
        if val> 10 and val<=20:
            return self.numeric_class_label[1]
        if val> 20 and val<=30:
            return self.numeric_class_label[2]
        if val> 30 and val<=40:
            return self.numeric_class_label[3]
        if val> 40 and val<=50:
            return self.numeric_class_label[4]
        if val> 50 and val<=60:
            return self.numeric_class_label[5]
        if val> 60 and val<=70:
            return self.numeric_class_label[6]
        if val> 70 and val<=80:
            return self.numeric_class_label[7]
        if val> 80 and val<=90:
            return self.numeric_class_label[8]
        if val> 90 and val<=100:
            return self.numeric_class_label[9]
        if val> 100:
            return self.numeric_class_label[10]

    def process_suspicious_ranking_class_label(self):
        print('processing suspicious ranking from spectra and matrix file...')
        filepath = os.path.join(self.conf.ROOT_PATH, 'spectra_faulty_methods_diffu.csv')
        print(filepath)
        #print(file)
        data_list = []
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            next(reader) # skip header
            for row in reader:
                projectname = row[0]
                bugid = int(row[1])
                faultmethodname = row[2].strip()
                print('processing > ' + projectname + ' bugid >' + bugid + ' faultmethod >' + faultmethodname)
                if faultmethodname == self.NO_VALUE:
                    #print('p>' + projectname + ' b>' + bugid + ' m>' + faultmethodname)
                    output = self.get_ranking_by_faultmethod(projectname, bugid, None)
                    # adding 11 class both numeric and categorical
                    output.append(self.get_class_label_11(output[3]).strip())
                    output.append(self.get_numeric_class_label_11(output[3]))

                    # adding 6 class both numeric and categorical
                    output.append(self.get_class_label_6(output[3]).strip())
                    output.append(self.get_numeric_class_label_6(output[3]))
                    self.rank_list.append(output)
                else:
                    getSpectraLineNum = self.get_line_number_from_spectra(projectname, bugid, faultmethodname)
                    #print('p>' + projectname + ' b>' + bugid + ' line>' + str(getSpectraLineNum))
                    output = self.get_ranking_by_faultmethod(projectname, bugid, getSpectraLineNum)
                    # adding 11 class both numeric and categorical
                    output.append(self.get_class_label_11(output[3]).strip())
                    output.append(self.get_numeric_class_label_11(output[3]))

                    # adding 6 class both numeric and categorical
                    output.append(self.get_class_label_6(output[3]).strip())
                    output.append(self.get_numeric_class_label_6(output[3]))
                    self.rank_list.append(output)
            #print(self.rank_list)

    # ranks value distribution and visualization
    def ranking_value_visualization(self):
        print('ranks value distribution and visualization')
        ranks = []
        for i in range(0, len(self.rank_list)):
            ranks.append(self.rank_list[i][3])
        print(ranks)
        dist_list = np.asarray(ranks)
        act_unq, act_unq_cnt = np.unique(dist_list, return_counts=True)
        # histogram 1
        fig, ax = plt.subplots()
        fig.canvas.set_window_title('Suspiciousness Ranking distribution image...')
        indices = np.arange(len(act_unq))
        width = 0.65
        rects = plt.bar(indices, act_unq_cnt, width, color='green')
        plt.xlabel("Raking values", fontsize=12)
        plt.ylabel("No. of total bugs", fontsize=12)
        plt.xticks(indices, act_unq, rotation='vertical')
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width()/2., 1.05*height, '%d' % int(height), fontsize=10, ha='center', va='bottom')
        plt.savefig('summary-bar.png')
        plt.show()

    def print_suspicious_ranking_class_label(self):
        print('saving generated ranking file...')
        with open(self.conf.ROOT_PATH + 'suspicious_ranking_class.csv', 'w') as csvfile:
            # PassedTestRuntime, FailedTestRuntime,
            columnTitleRow = 'ProjectID, '\
                             'BugId, '\
                             'Suspiciousness, '\
                             'Ranking, '\
                             'Class11, '\
                             'NumericClass11, '\
                             'Class6, '\
                             'NumericClass6,\n'
            csvfile.write(columnTitleRow)
            for i in range(0, len(self.rank_list)):
                row = (str(self.rank_list[i][0]) + ',' +
                       str(self.rank_list[i][1]) + ',' +
                       str(self.rank_list[i][2]) + ',' +
                       str(self.rank_list[i][3]) + ',' +
                       str(self.rank_list[i][4]) + ',' +
                       str(self.rank_list[i][5]) + ',' +
                       str(self.rank_list[i][6]) + ',' +
                       str(self.rank_list[i][7]) + '\n')
                csvfile.write(row)
            print('Ranking class file is saved.')

    def process_class_label(self):
        self.process_suspicious_ranking_class_label()
        self.print_suspicious_ranking_class_label()
