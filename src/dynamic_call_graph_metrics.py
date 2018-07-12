#
# file dynamic_call_graph_metrics.py
# author: Muhammad Mushfiqur Rahman
# Email:mushfiq.rahman@tum.de
# date 2018-06-05

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

class DynamicCallGraphMatrix():
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

        self.dynamic_call_graph_metrics_list = []
        self.dynamic_call_graph_metrics_math_data = []
        self.dynamic_call_graph_metrics_list_chart = []
        self.dynamic_call_graph_metrics_list_lang = []
        self.dynamic_call_graph_metrics_list_math = []
        self.dynamic_call_graph_metrics_list_time = []
        self.dynamic_call_graph_metrics_list_closure = []
        self.dynamic_call_graph_metrics_list_mockito = []


    def get_ranking_by_spectra(self, projectName, bug_version, spectraLineNum):
        if spectraLineNum == None:
            return
        #print('spectraLineNum>' + str(spectraLineNum))
        rankPath = os.path.join(self.conf.ROOT_PATH, 'suspiciousness_ranking/' + projectName + '_' + str(bug_version) + '.csv')
        with open(rankPath, 'r') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for lineno, row in enumerate(readCSV):
                if lineno == spectraLineNum:
                    #print(row)
                    return row[2]

    def get_featurenode_linenum_from_spectra(self, projectName, bug_version, faultMethodFeatureName):
        #print('project>' + projectName + ' id> ' + str(bug_version) + ' methodName> ' + faultMethodFeatureName)
        filepath = os.path.join(self.conf.ROOT_PATH, projectName + '/' + str(bug_version) + '/spectra')
        with open(filepath, 'r') as spectra:
             for num, line in enumerate(spectra, 1):
                 if faultMethodFeatureName in line.strip():
                     return num

    def process_math_dynamic_metrics_from_call_graph(self):
        for subdir, dirs, files in sorted(os.walk(self.conf.MATH_CALL_GRPAH_PATH)):
            for file in sorted(files):
                filepath = os.path.join(subdir, file)
                print(filepath)
                buggy_version = re.findall('\d+', filepath)
                fname = file.replace(".dot", "")
                faultNodes = fname.strip()
                #print(faultNodes)
                #print('buggy_version> '+ str(buggy_version[0]) + ' dot file name: ' + fname)

                # load matrix file
                matrix_filepath = os.path.join(self.conf.ROOT_PATH, self.conf.MATH_ID + '/'+ str(buggy_version[0]) + '/matrix')
                mat = self.loader.load_coverage_file(matrix_filepath)
                mat_arr = np.asarray(mat)
                #print(mat_arr.shape)
                pass_fail_col_arr = mat_arr[:, mat_arr.shape[1] - 1]
                test_case_result_col_arr = np.asarray(pass_fail_col_arr)
                unique_value, unique_counts = np.unique(test_case_result_col_arr, return_counts=True)
                #print(unique_value)
                #print(unique_counts)

                total_test_case_coverage_by_dynamic_call_graph = 0
                # total test cases that cover/execute for this dynamic call graph
                getSpectraLineNum = self.get_featurenode_linenum_from_spectra(self.conf.MATH_ID, buggy_version[0], faultNodes)
                #print(str(getSpectraLineNum))
                if getSpectraLineNum != None:
                    fault_node_feature_col_arr = mat_arr[:, getSpectraLineNum-1]
                    for t in range(0, len(fault_node_feature_col_arr)):
                        if fault_node_feature_col_arr[t] == 1:
                            total_test_case_coverage_by_dynamic_call_graph += 1

                cnt = 0
                diffu_feature_modified_list = []
                diffu_feature_added_list = []
                #faultNodeInDegList = []
                #if getSpectraLineNum != None:
                faultNodeInDegList = []
                faultNodeOutDegList = []
                faultClass_CBO = 0
                faultClass_RFC_List = []
                faultClass_RFC = 0

                # dot file edge calculation begin>
                node_split = faultNodes.split('#', 1)
                faultNodeClassName = node_split[0]
                file = open(filepath, 'r')#READING DOT FILE
                with open(filepath, 'r') as file:
                    text= file.readlines()
                    for row in text:
                        #print(row)
                        line_split = row.split('->', 1)
                        #print(len(line_split))
                        if len(line_split) > 1:
                            sourceNode = line_split[0].strip().replace('"', '')
                            #sourceNode
                            #print(sourceNode)
                            dNode = line_split[1].strip().replace('"', '')
                            destNode = dNode.replace(";", "")
                            #print(destNode)
                            if sourceNode.strip() == faultNodes:
                                #print(sourceNode)
                                faultNodeOutDegList.append(destNode)
                            if destNode.strip() == faultNodes:
                                #print(destNode)
                                faultNodeInDegList.append(sourceNode)
                            # calculate CBO
                            if faultNodeClassName in sourceNode or faultNodeClassName in destNode:
                                faultClass_CBO += 1
                                #print(e.to_string())
                                if faultNodeClassName in sourceNode and faultNodeClassName in destNode:
                                    faultClass_CBO -= 1
                            #calculate RFC
                            if faultNodeClassName in sourceNode:
                                if sourceNode not in faultClass_RFC_List:
                                    faultClass_RFC_List.append(sourceNode)
                            if faultNodeClassName in destNode:
                                if destNode not in faultClass_RFC_List:
                                    faultClass_RFC_List.append(destNode)

                #ource(text)
                #graph = pydotplus.Graph(filepath)
                #print(graph.to_string())
                #edgeList = graph.get_edges()
                #print(edgeList)
                #nodeList = graph.get_nodes()
                #print(nodeList)

                outDegCount = len(faultNodeOutDegList)
                inDegCount = len(faultNodeInDegList)
                faultClass_RFC = len(faultClass_RFC_List) + outDegCount
                no_of_test_cases_covers_fault_node = 0
                no_of_test_cases_passes_for_fault_node = 0
                no_of_test_cases_fails_for_fault_node = 0
                print('OutDeg> ' + str(outDegCount) + ' InDeg> ' + str(inDegCount) + ' CBO> ' + str(faultClass_CBO)  + ' RFC> ' + str(faultClass_RFC))
                if outDegCount != 0 and inDegCount != 0:
                    #print('OutDeg> ' + str(outDegCount) + ' InDeg> ' + str(inDegCount) + ' CBO> ' + str(faultClass_CBO)  + ' RFC> ' + str(faultClass_RFC))
                    # code for matrix file
                    getSpectraLineNum = self.get_featurenode_linenum_from_spectra(self.conf.MATH_ID, buggy_version[0], faultNodes)
                    rank = self.get_ranking_by_spectra(self.conf.MATH_ID, buggy_version[0], getSpectraLineNum)
                    #print(str(getSpectraLineNum))
                    if getSpectraLineNum != None:
                        fault_node_feature_col_arr = mat_arr[:, getSpectraLineNum-1]
                        # fault node test coverage pass/fail info calculation
                        for t in range(0, len(fault_node_feature_col_arr)):
                            if fault_node_feature_col_arr[t] == 1:
                                no_of_test_cases_covers_fault_node += 1
                                if pass_fail_col_arr[t] == 1:
                                    no_of_test_cases_passes_for_fault_node += 1
                                else:
                                    no_of_test_cases_fails_for_fault_node += 1
                        #print('Total test cases for fn>', no_of_test_cases_covers_fault_node)
                        #print('pass for fn>', no_of_test_cases_passes_for_fault_node)
                        #print('fail for fn>', no_of_test_cases_fails_for_fault_node)
                    output_row = [self.conf.MATH_ID,
                              # + '_' + str(buggy_version),
                              int(buggy_version[0]),
                              faultNodes,
                              rank,
                              inDegCount,
                              outDegCount,
                              inDegCount + outDegCount,
                              faultClass_CBO,
                              faultClass_RFC,
                              no_of_test_cases_covers_fault_node,
                              no_of_test_cases_passes_for_fault_node,
                              no_of_test_cases_fails_for_fault_node,
                              total_test_case_coverage_by_dynamic_call_graph,
                              "/".join(faultNodeInDegList),
                              "/".join(faultNodeOutDegList)]
                    diffu_feature_modified_list.append(output_row)
                else:
                    #print('OutDeg> ' + str(outDegCount) + ' InDeg> ' + str(inDegCount) + ' CBO> ' + str(faultClass_CBO) + ' RFC> ' + str(faultClass_RFC))
                    impl_action = 'Unknown'
                    output_row = [self.conf.MATH_ID, int(buggy_version[0]), impl_action, 9999, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '']
                    diffu_feature_added_list.append(output_row)

                if len(diffu_feature_modified_list) > 0:
                    self.dynamic_call_graph_metrics_list_math.append(diffu_feature_modified_list[0])
                else:
                    self.dynamic_call_graph_metrics_list_math.append(diffu_feature_added_list[0])

        print('============== Printing ' + self.conf.MATH_ID + ' Projects Dynamic Call Graph Metrics Features =================')
        output_sorted_list = sorted(self.dynamic_call_graph_metrics_list_math, key=itemgetter(1))
        self.dynamic_call_graph_metrics_math_data.extend(output_sorted_list)
        #print(output_sorted_list)
        print('============== Finished Printing ' + self.conf.MATH_ID + ' Projects Dynamic Call Graph Metrics Version ================')

    def print_math_dynamic_call_graph_metrics(self):
        result_arr = np.array(self.dynamic_call_graph_metrics_math_data)
        #print(result_arr.shape)
        with open(self.conf.ROOT_PATH + 'dynamic_call_graph_math_data.csv', 'w') as csvfile:
            # PassedTestRuntime, FailedTestRuntime,
            columnTitleRow = 'ProjectID, '\
                             'BugId, '\
                             'FaultNodeName, '\
                             'Rank, '\
                             'FaultNode_InDegree, '\
                             'FaultNode_OutDegree, '\
                             'FaultNodeDegreeCentrality, '\
                             'CBO, '\
                             'RFC, '\
                             'NoOfTestCasesExecuteFaultMethod, '\
                             'NoOfTestCasesPassesCoversFaultNode, '\
                             'NoOfTestCasesFailsCoversFaultNode, '\
                             'NoOfTestCasesExecutesDynamicCallGraph, '\
                             'InDegreeMethodCallsList, '\
                             'OutDegreeMethodCallsList\n'

            csvfile.write(columnTitleRow)
            for i in range(0, result_arr.shape[0]):
                row = (str(result_arr[i][0]) + ', ' +
                      str(result_arr[i][1]) + ', ' +
                      str(result_arr[i][2]) + ', ' +
                      str(result_arr[i][3]) + ', ' +
                      str(result_arr[i][4]) + ', ' +
                      str(result_arr[i][5]) + ', ' +
                      str(result_arr[i][6]) + ', ' +
                      str(result_arr[i][7]) + ', ' +
                      str(result_arr[i][8]) + ', ' +
                      str(result_arr[i][9]) + ', ' +
                      str(result_arr[i][10]) + ', ' +
                      str(result_arr[i][11]) + ', ' +
                      str(result_arr[i][12]) + ', ' +
                      str(result_arr[i][13]) + ', ' +
                      str(result_arr[i][14]) + '\n')
                csvfile.write(row)
            print('Math Dynamic Call Graph Metrics file is saved.')

    def process_dynamic_metrics_from_call_graph(self):
        for i in range(0, len(self.conf.CALL_GRAPH_PROJECTS_ID)):
            for subdir, dirs, files in sorted(os.walk(self.conf.DYNAMIC_CALL_GRAPH_PROJECTS_PATH[i])):
                for file in sorted(files):
                    filepath = os.path.join(subdir, file)
                    print(filepath)
                    fn = file.replace(".dot", "")
                    buggy_version = int(fn) #re.findall('\d+', filepath)
                    graph = pydotplus.graphviz.graph_from_dot_file(filepath)
                    edgeList = graph.get_edge_list()
                    nodeList = graph.get_node_list()
                    faultNodes = []

                    # load matrix file
                    matrix_filepath = os.path.join(self.conf.ROOT_PATH, self.conf.CALL_GRAPH_PROJECTS_ID[i] + '/'+ str(buggy_version) + '/matrix')
                    mat = self.loader.load_coverage_file(matrix_filepath)
                    mat_arr = np.asarray(mat)
                    #print(mat_arr.shape)
                    pass_fail_col_arr = mat_arr[:, mat_arr.shape[1] - 1]
                    test_case_result_col_arr = np.asarray(pass_fail_col_arr)
                    unique_value, unique_counts = np.unique(test_case_result_col_arr, return_counts=True)
                    #print(unique_value)
                    #print(unique_counts)

                    total_test_case_coverage_by_dynamic_call_graph = 0
                    for n in nodeList:
                        #nodeName = n.get_name()
                        colorName = json.loads(n.obj_dict['attributes']['fillcolor'])
                        nodeName = json.loads(n.get_name())
                        if colorName.strip() == "red":
                            faultNodes.append(json.loads(n.get_name()))

                        # total test cases that cover/execute for this dynamic call graph
                        getSpectraLineNum = self.get_featurenode_linenum_from_spectra(self.conf.CALL_GRAPH_PROJECTS_ID[i], buggy_version, nodeName)
                        #print(str(getSpectraLineNum))
                        if getSpectraLineNum != None:
                            fault_node_feature_col_arr = mat_arr[:, getSpectraLineNum-1]
                            for t in range(0, len(fault_node_feature_col_arr)):
                                if fault_node_feature_col_arr[t] == 1:
                                    total_test_case_coverage_by_dynamic_call_graph += 1
                    #print(nodeList)
                    #print(faultNodes)
                    cnt = 0
                    diffu_feature_modified_list = []
                    diffu_feature_added_list = []
                    for node in range(0, len(faultNodes)):
                        faultNodeInDegList = []
                        faultNodeOutDegList = []
                        faultClass_CBO = 0
                        faultClass_RFC_List = []
                        faultClass_RFC = 0
                        for e in edgeList:
                            cnt += 1
                            dottedEdge = False
                            att = e.obj_dict['attributes']
                            node_split = faultNodes[node].split('#', 1)
                            faultNodeClassName = node_split[0]
                            sourceNode = json.loads(e.get_source())
                            destNode = json.loads(e.get_destination())
                            if len(att) > 0:
                                if att['style'] == 'dotted':
                                    dottedEdge = True
                                    # for RFC calculation
                                    if faultNodeClassName in sourceNode:
                                        if sourceNode not in faultClass_RFC_List:
                                            faultClass_RFC_List.append(sourceNode)
                                    if faultNodeClassName in destNode:
                                        if destNode not in faultClass_RFC_List:
                                            faultClass_RFC_List.append(destNode)
                            if dottedEdge != True:
                                # calculate in/out degree
                                if sourceNode.strip() == faultNodes[node]:
                                    faultNodeOutDegList.append(destNode)
                                if destNode.strip() == faultNodes[node]:
                                    faultNodeInDegList.append(sourceNode)
                                # calculate CBO
                                if faultNodeClassName in sourceNode or faultNodeClassName in destNode:
                                    faultClass_CBO += 1
                                    #print(e.to_string())
                                    if faultNodeClassName in sourceNode and faultNodeClassName in destNode:
                                        faultClass_CBO -= 1
                                #calculate RFC
                                if faultNodeClassName in sourceNode:
                                    if sourceNode not in faultClass_RFC_List:
                                        faultClass_RFC_List.append(sourceNode)
                                if faultNodeClassName in destNode:
                                    if destNode not in faultClass_RFC_List:
                                        faultClass_RFC_List.append(destNode)
                        outDegCount = len(faultNodeOutDegList)
                        inDegCount = len(faultNodeInDegList)
                        faultClass_RFC = len(faultClass_RFC_List) + outDegCount
                        #print(faultClass_CBO)

                        if outDegCount != 0 and inDegCount != 0:
                            print('OutDeg> ' + str(outDegCount) + ' InDeg> ' + str(inDegCount) + ' CBO> ' + str(faultClass_CBO)  + ' RFC> ' + str(faultClass_RFC))
                            # code for matrix file
                            getSpectraLineNum = self.get_featurenode_linenum_from_spectra(self.conf.CALL_GRAPH_PROJECTS_ID[i], buggy_version, faultNodes[node])
                            #print(str(getSpectraLineNum))
                            if getSpectraLineNum != None:
                                fault_node_feature_col_arr = mat_arr[:, getSpectraLineNum-1]
                                # fault node test coverage pass/fail info calculation
                                no_of_test_cases_covers_fault_node = 0
                                no_of_test_cases_passes_for_fault_node = 0
                                no_of_test_cases_fails_for_fault_node = 0
                                for t in range(0, len(fault_node_feature_col_arr)):
                                    if fault_node_feature_col_arr[t] == 1:
                                        no_of_test_cases_covers_fault_node += 1
                                        if pass_fail_col_arr[t] == 1:
                                            no_of_test_cases_passes_for_fault_node += 1
                                        else:
                                            no_of_test_cases_fails_for_fault_node += 1
                                #print('Total test cases for fn>', no_of_test_cases_covers_fault_node)
                                #print('pass for fn>', no_of_test_cases_passes_for_fault_node)
                                #print('fail for fn>', no_of_test_cases_fails_for_fault_node)


                            output_row = [self.conf.CALL_GRAPH_PROJECTS_ID[i],
                                      # + '_' + str(buggy_version),
                                      buggy_version,
                                      faultNodes[node],
                                      inDegCount,
                                      outDegCount,
                                      inDegCount + outDegCount,
                                      faultClass_CBO,
                                      faultClass_RFC,
                                      no_of_test_cases_covers_fault_node,
                                      no_of_test_cases_passes_for_fault_node,
                                      no_of_test_cases_fails_for_fault_node,
                                      total_test_case_coverage_by_dynamic_call_graph,
                                      "/".join(faultNodeInDegList),
                                      "/".join(faultNodeOutDegList)]
                            diffu_feature_modified_list.append(output_row)
                        else:
                            #print('OutDeg> ' + str(outDegCount) + ' InDeg> ' + str(inDegCount) + ' CBO> ' + str(faultClass_CBO) + ' RFC> ' + str(faultClass_RFC))
                            impl_action = 'Unknown'
                            output_row = [self.conf.CALL_GRAPH_PROJECTS_ID[i], buggy_version, impl_action, 0, 0, 0, 0, 0, 0, 0, 0, 0, '', '']
                            diffu_feature_added_list.append(output_row)

                    if len(diffu_feature_modified_list) > 0:
                        #lowRank = self.get_ranking(diffu_feature_modified_list[0][0], diffu_feature_modified_list[0][1], diffu_feature_modified_list[0][2])
                        spectraLineNum = self.get_featurenode_linenum_from_spectra(self.conf.CALL_GRAPH_PROJECTS_ID[i], diffu_feature_modified_list[0][1], diffu_feature_modified_list[0][2])
                        lowRank = self.get_ranking_by_spectra(self.conf.CALL_GRAPH_PROJECTS_ID[i], diffu_feature_modified_list[0][1], spectraLineNum)
                        #print('lowRank> ', lowRank)
                        #low rank == highest suspicious value.
                        index = 0
                        #print('length> ' + str(len(diffu_feature_modified_list)))
                        if len(diffu_feature_modified_list) > 1:
                            for x in range(1, len(diffu_feature_modified_list)):
                                spectraLineNum = self.get_featurenode_linenum_from_spectra(self.conf.CALL_GRAPH_PROJECTS_ID[i], diffu_feature_modified_list[x][1], diffu_feature_modified_list[x][2])
                                curRank = self.get_ranking_by_spectra(self.conf.CALL_GRAPH_PROJECTS_ID[i], diffu_feature_modified_list[x][1], spectraLineNum)
                                #print('curRank> ', curRank)
                                if curRank < lowRank:
                                    lowRank = curRank
                                    index = x
                                    #print('survivedindex>', diffu_feature_modified_list[index][2])
                            #print(index)
                            #print('length> ' + str(len(diffu_feature_modified_list)))
                            resultarr = diffu_feature_modified_list[index]
                            diffu_feature_modified_list = []
                            diffu_feature_modified_list.append(resultarr)
                            #print('modified length>' + str(len(diffu_feature_modified_list)))
                            #print('modified arr>', diffu_feature_modified_list)

                        if self.conf.CALL_GRAPH_PROJECTS_ID[i] == 'Chart':
                            self.dynamic_call_graph_metrics_list_chart.append(diffu_feature_modified_list[0])
                        elif self.conf.CALL_GRAPH_PROJECTS_ID[i] == 'Lang':
                            self.dynamic_call_graph_metrics_list_lang.append(diffu_feature_modified_list[0])
                        elif self.conf.CALL_GRAPH_PROJECTS_ID[i] == 'Time':
                            self.dynamic_call_graph_metrics_list_time.append(diffu_feature_modified_list[0])
                        else:
                            self.dynamic_call_graph_metrics_list_closure.append(diffu_feature_modified_list[0])
                    else:
                        if self.conf.CALL_GRAPH_PROJECTS_ID[i] == 'Chart':
                            self.dynamic_call_graph_metrics_list_chart.append(diffu_feature_added_list[0])
                        elif self.conf.CALL_GRAPH_PROJECTS_ID[i] == 'Lang':
                            self.dynamic_call_graph_metrics_list_lang.append(diffu_feature_added_list[0])
                        elif self.conf.CALL_GRAPH_PROJECTS_ID[i] == 'Time':
                            self.dynamic_call_graph_metrics_list_time.append(diffu_feature_added_list[0])
                        else:
                            self.dynamic_call_graph_metrics_list_closure.append(diffu_feature_added_list[0])


            print('============== Printing ' + self.conf.CALL_GRAPH_PROJECTS_ID[i] + ' Projects Dynamic Call Graph Metrics Features =================')
            if self.conf.CALL_GRAPH_PROJECTS_ID[i] == 'Chart':
                output_sorted_list = sorted(self.dynamic_call_graph_metrics_list_chart, key=itemgetter(1))
                self.dynamic_call_graph_metrics_list.extend(output_sorted_list)
                #print(output_sorted_list)
            if self.conf.CALL_GRAPH_PROJECTS_ID[i] == 'Lang':
                output_sorted_list = sorted(self.dynamic_call_graph_metrics_list_lang, key=itemgetter(1))
                #print(output_sorted_list)
                self.dynamic_call_graph_metrics_list.extend(output_sorted_list)
            if self.conf.CALL_GRAPH_PROJECTS_ID[i] == 'Time':
                output_sorted_list = sorted(self.dynamic_call_graph_metrics_list_time, key=itemgetter(1))
                #print(output_sorted_list)
                self.dynamic_call_graph_metrics_list.extend(output_sorted_list)
            if self.conf.CALL_GRAPH_PROJECTS_ID[i] == 'Closure':
                output_sorted_list = sorted(self.dynamic_call_graph_metrics_list_closure, key=itemgetter(1))
                #print(output_sorted_list)
                self.dynamic_call_graph_metrics_list.extend(output_sorted_list)
            print('============== Finished Printing ' + self.conf.CALL_GRAPH_PROJECTS_ID[i] + ' Projects Dynamic Call Graph Metrics Version ================')

    def print_dynamic_call_graph_metrics(self):
        #print(len(self.dynamic_call_graph_metrics_list))
        #print(self.dynamic_call_graph_metrics_list)
        result_arr = np.array(self.dynamic_call_graph_metrics_list)
        #print(result_arr.shape)
        with open(self.conf.ROOT_PATH + 'dynamic_call_graph_metrics.csv', 'w') as csvfile:
            # PassedTestRuntime, FailedTestRuntime,
            columnTitleRow = 'ProjectID, '\
                             'BugId, '\
                             'FaultNodeName, '\
                             'FaultNode_InDegree, '\
                             'FaultNode_OutDegree, '\
                             'FaultNodeDegreeCentrality, '\
                             'CBO, '\
                             'RFC, '\
                             'NoOfTestCasesExecuteFaultMethod, '\
                             'NoOfTestCasesPassesCoversFaultNode, '\
                             'NoOfTestCasesFailsCoversFaultNode, '\
                             'NoOfTestCasesExecutesDynamicCallGraph, '\
                             'InDegreeMethodCallsList, '\
                             'OutDegreeMethodCallsList\n'

            csvfile.write(columnTitleRow)
            for i in range(0, result_arr.shape[0]):
                row = (str(result_arr[i][0]) + ', ' +
                      str(result_arr[i][1]) + ', ' +
                      str(result_arr[i][2]) + ', ' +
                      str(result_arr[i][3]) + ', ' +
                      str(result_arr[i][4]) + ', ' +
                      str(result_arr[i][5]) + ', ' +
                      str(result_arr[i][6]) + ', ' +
                      str(result_arr[i][7]) + ', ' +
                      str(result_arr[i][8]) + ', ' +
                      str(result_arr[i][9]) + ', ' +
                      str(result_arr[i][10]) + ', ' +
                      str(result_arr[i][11]) + ', ' +
                      str(result_arr[i][12]) + ', ' +
                      str(result_arr[i][13]) + '\n')
                csvfile.write(row)
            print('Dynamic Call Graph Metrics file is saved.')

    def process_dynamic_call_graph(self):
        #self.calculate_oo_metrics()
        self.process_dynamic_metrics_from_call_graph()
        self.print_dynamic_call_graph_metrics()
        self.process_math_dynamic_metrics_from_call_graph()
        self.print_math_dynamic_call_graph_metrics()


'''
def calculate_oo_metrics(self):
    filepath = os.path.join(self.conf.DYNAMIC_CALL_GRAPH_PATH, self.conf.CHART_ID +'/')
    #graph = pydotplus.graphviz.graph_from_dot_file(filepath + '1.dot')
    graph = pydotplus.graphviz.graph_from_dot_file(filepath + '2.dot')
    edgeList = graph.get_edge_list()
    nodeList = graph.get_node_list()

    # load matrix file
    filepath = os.path.join(self.conf.ROOT_PATH, self.conf.CHART_ID + '/2/matrix')
    mat = self.loader.load_coverage_file(filepath)
    mat_arr = np.asarray(mat)
    #print(mat_arr.shape)
    pass_fail_col_arr = mat_arr[:, mat_arr.shape[1] - 1]
    test_case_result_col_arr = np.asarray(pass_fail_col_arr)
    unique_value, unique_counts = np.unique(test_case_result_col_arr, return_counts=True)
    #print(unique_value)
    #print(unique_counts)

    faultNodes = []
    total_test_case_coverage_by_dynamic_call_graph = 0
    for n in nodeList:
        #nodeName = n.get_name()
        colorName = json.loads(n.obj_dict['attributes']['fillcolor'])
        nodeName = json.loads(n.get_name())
        if colorName.strip() == "red":
            faultNodes.append(json.loads(n.get_name()))

        # total test cases that cover/execute for this dynamic call graph
        getSpectraLineNum = self.get_featurenode_linenum_from_spectra(self.conf.CHART_ID, 2, nodeName)
        #print(getSpectraLineNum)
        if getSpectraLineNum != None:
            fault_node_feature_col_arr = mat_arr[:, getSpectraLineNum-1]
            for t in range(0, len(fault_node_feature_col_arr)):
                if fault_node_feature_col_arr[t] == 1:
                    total_test_case_coverage_by_dynamic_call_graph += 1
    #print(nodeList)
    #print(faultNodes)
    cnt = 0
    diffu_feature_modified_list = []
    diffu_feature_added_list = []

    for node in range(0, len(faultNodes)):
        faultNodeInDegList = []
        faultNodeOutDegList = []
        faultClass_CBO = 0
        faultClass_RFC_List = []
        faultClass_RFC = 0
        for e in edgeList:
            cnt += 1
            dottedEdge = False
            att = e.obj_dict['attributes']
            node_split = faultNodes[node].split('#', 1)
            faultNodeClassName = node_split[0]
            sourceNode = json.loads(e.get_source())
            destNode = json.loads(e.get_destination())
            #print(faultNodeClassName)
            if len(att) > 0:
                if att['style'] == 'dotted':
                    dottedEdge = True
                    # for RFC calculation
                    if faultNodeClassName in sourceNode:
                        if sourceNode not in faultClass_RFC_List:
                            faultClass_RFC_List.append(sourceNode)
                    if faultNodeClassName in destNode:
                        if destNode not in faultClass_RFC_List:
                            faultClass_RFC_List.append(destNode)
            if dottedEdge != True:
                # calculate in/out degree
                if sourceNode.strip() == faultNodes[node]:
                    faultNodeOutDegList.append(destNode)
                if destNode.strip() == faultNodes[node]:
                    faultNodeInDegList.append(sourceNode)
                # calculate CBO
                if faultNodeClassName in sourceNode or faultNodeClassName in destNode:
                    #print(faultNodeClassName)
                    faultClass_CBO += 1
                    #print(e.to_string())
                    if faultNodeClassName in sourceNode and faultNodeClassName in destNode:
                        faultClass_CBO -= 1
                #calculate RFC
                if faultNodeClassName in sourceNode:
                    if sourceNode not in faultClass_RFC_List:
                        faultClass_RFC_List.append(sourceNode)
                if faultNodeClassName in destNode:
                    if destNode not in faultClass_RFC_List:
                        faultClass_RFC_List.append(destNode)

        outDegCount = len(faultNodeOutDegList)
        inDegCount = len(faultNodeInDegList)
        faultClass_RFC = len(faultClass_RFC_List) + outDegCount

        if outDegCount != 0 and inDegCount != 0:
            # code for matrix file
            getSpectraLineNum = self.get_featurenode_linenum_from_spectra(self.conf.CHART_ID, 2, faultNodes[node])
            #print(getSpectraLineNum)
            if getSpectraLineNum != None:
                fault_node_feature_col_arr = mat_arr[:, getSpectraLineNum-1]
                # fault node test coverage pass/fail info calculation
                no_of_test_cases_covers_fault_node = 0
                no_of_test_cases_passes_for_fault_node = 0
                no_of_test_cases_fails_for_fault_node = 0
                for t in range(0, len(fault_node_feature_col_arr)):
                    if fault_node_feature_col_arr[t] == 1:
                        no_of_test_cases_covers_fault_node += 1
                        if pass_fail_col_arr[t] == 1:
                            no_of_test_cases_passes_for_fault_node += 1
                        else:
                            no_of_test_cases_fails_for_fault_node += 1
                #print('Total test cases for fn>', no_of_test_cases_covers_fault_node)
                #print('pass for fn>', no_of_test_cases_passes_for_fault_node)
                #print('fail for fn>', no_of_test_cases_fails_for_fault_node)

        #print(outDegCount)
        #print(inDegCount)
        #print(faultClass_CBO)
        #print(faultClass_RFC)
    #print('total_test_case_cover_dcg>', total_test_case_coverage_by_dynamic_call_graph)
'''
