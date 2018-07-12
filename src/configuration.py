#
# file configuration.py
# author: Muhammad Mushfiqur Rahman
# Email:mushfiq.rahman@tum.de
# date 2018-05-10

from __future__ import division
from os import listdir, makedirs
from os.path import isfile, join, dirname, exists, basename
import shutil
import itertools
import numpy as np
import math
import scipy.misc
import colorsys
import sys
import os

class Configuration():
    def __init__(self, pathdir):
        #self.ROOT_PATH = '/home/mra/praktikum/projectsdb/method-data/'
        self.ROOT_PATH = pathdir
        self.STATIC_METRICS_DATA_PATH = os.path.join(self.ROOT_PATH, 'staticmetrics/')
        self.DYNAMIC_CALL_GRAPH_PATH = os.path.join(self.ROOT_PATH, 'dynamic_call_graph/')

        #self.STATIC_METRICS_DATA_PATH = self.ROOT_PATH
        #self.DYNAMIC_CALL_GRAPH_PATH = self.ROOT_PATH
        #print(self.STATIC_METRICS_DATA_PATH)
        #print(self.DYNAMIC_CALL_GRAPH_PATH)
        self.LANG_ID = 'Lang'
        self.MATH_ID = 'Math'
        self.CHART_ID = 'Chart'
        self.CLOSURE_ID = 'Closure'
        self.TIME_ID = 'Time'
        self.MOCKITO_ID = 'Mockito'
        self.LANG_PATH = os.path.join(self.ROOT_PATH, self.LANG_ID +'/')
        self.MATH_PATH = os.path.join(self.ROOT_PATH, self.MATH_ID +'/')
        self.CHART_PATH = os.path.join(self.ROOT_PATH, self.CHART_ID +'/')
        self.CLOSURE_PATH = os.path.join(self.ROOT_PATH, self.CLOSURE_ID +'/')
        self.TIME_PATH = os.path.join(self.ROOT_PATH, self.TIME_ID +'/')
        self.MOCKITO_PATH = os.path.join(self.ROOT_PATH, self.MOCKITO_ID +'/')
        self.PROJECTS_ID = [self.CHART_ID, self.LANG_ID, self.MATH_ID, self.TIME_ID, self.CLOSURE_ID]
        self.PROJECTS_DATA_PATH = [self.CHART_PATH, self.LANG_PATH, self.MATH_PATH, self.TIME_PATH, self.CLOSURE_PATH]
        #self.PROJECTS_ID = [self.LANG_ID]
        #self.PROJECTS_DATA_PATH = [self.LANG_PATH]
        # variable for dynamic metrics
        self.LANG_CALL_GRAPH_PATH = os.path.join(self.DYNAMIC_CALL_GRAPH_PATH, self.LANG_ID + '/')
        self.TIME_CALL_GRAPH_PATH = os.path.join(self.DYNAMIC_CALL_GRAPH_PATH, self.TIME_ID + '/')
        self.CHART_CALL_GRPAH_PATH = os.path.join(self.DYNAMIC_CALL_GRAPH_PATH, self.CHART_ID + '/')
        self.CLOSURE_CALL_GRPAH_PATH = os.path.join(self.DYNAMIC_CALL_GRAPH_PATH, self.CLOSURE_ID + '/')
        self.MATH_CALL_GRPAH_PATH = os.path.join(self.DYNAMIC_CALL_GRAPH_PATH, self.MATH_ID + '/')
        self.MOCKITO_CALL_GRPAH_PATH = os.path.join(self.DYNAMIC_CALL_GRAPH_PATH, self.MOCKITO_ID + '/')

        self.CALL_GRAPH_PROJECTS_ID = [self.CHART_ID, self.LANG_ID, self.TIME_ID, self.CLOSURE_ID]
        self.DYNAMIC_CALL_GRAPH_PROJECTS_PATH = [self.CHART_CALL_GRPAH_PATH,
                                                 self.LANG_CALL_GRAPH_PATH,
                                                 self.TIME_CALL_GRAPH_PATH,
                                                 self.CLOSURE_CALL_GRPAH_PATH]
        # For shorter test seq.
        #self.CALL_GRAPH_PROJECTS_ID = [self.CHART_ID]
        #self.DYNAMIC_CALL_GRAPH_PROJECTS_PATH = [self.CHART_CALL_GRPAH_PATH]

        # variable for static metrics
        self.LANG_STATIC_METRICS_PATH = os.path.join(self.STATIC_METRICS_DATA_PATH, self.LANG_ID + '/')
        self.TIME_STATIC_METRICS_PATH = os.path.join(self.STATIC_METRICS_DATA_PATH, self.TIME_ID + '/')
        self.CHART_STATIC_METRICS_PATH = os.path.join(self.STATIC_METRICS_DATA_PATH, self.CHART_ID + '/')
        self.CLOSURE_STATIC_METRICS_PATH = os.path.join(self.STATIC_METRICS_DATA_PATH, self.CLOSURE_ID + '/')
        self.MATH_STATIC_METRICS_PATH = os.path.join(self.STATIC_METRICS_DATA_PATH, self.MATH_ID + '/')
        self.MOCKITO_STATIC_METRICS_PATH = os.path.join(self.STATIC_METRICS_DATA_PATH, self.MOCKITO_ID + '/')

        self.STATIC_METRICS_PROJECTS_ID = [self.CHART_ID, self.LANG_ID, self.MATH_ID, self.TIME_ID, self.CLOSURE_ID]
        self.STATIC_METRICS_PROJECTS_PATH = [self.CHART_STATIC_METRICS_PATH,
                                             self.LANG_STATIC_METRICS_PATH,
                                             self.MATH_STATIC_METRICS_PATH,
                                             self.TIME_STATIC_METRICS_PATH,
                                             self.CLOSURE_STATIC_METRICS_PATH]

        #self.PROJECTS_DATA_PATH = [self.LANG_PATH, self.MATH_PATH, self.CHART_PATH, self.TIME_PATH, self.CLOSURE_PATH, self.MOCKITO_PATH]

    def handle_dir(self, directory):
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory)
