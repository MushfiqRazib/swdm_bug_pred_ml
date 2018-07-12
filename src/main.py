#
# file main.py
# author: Muhammad Mushfiqur Rahman
# Email:mushfiq.rahman@tum.de
# date 2018-05-02

from fault_localization import FaultLocalization
from test_suite_matrix_generation import TestSuiteMatrix
from dynamic_call_graph_metrics import DynamicCallGraphMatrix
from static_metrics_parsing import StaticMetricsParser
from ranking_class_label import SuspiciousRankingClassLabel
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', metavar='TYPE', type=str, help='input metrics: s/d/t/c/r')
    parser.add_argument('-p', metavar='FILE', type=str, help='Please input the folder path of spectra, matrix files')
    args = parser.parse_args()
    print(args.p)
    print(args.i)
    # for Fault Localization ranking calculation
    if args.i == 'r':
        fl = FaultLocalization(args.p)
        fl.calculate_suspiciousness()

    # for testsuite metrics
    if args.i == 't':
        testsuite = TestSuiteMatrix(args.p)
        testsuite.process_test_suite_properties()

    # for dynamic call graph
    if args.i == 'd':
        dcg = DynamicCallGraphMatrix(args.p)
        dcg.process_dynamic_call_graph()

    # for static metrics parsing
    if args.i == 's':
        static_metrics = StaticMetricsParser(args.p)
        static_metrics.parsing_static_metrics()

    # for class label
    # the input path p var = path of the 'suspiciousness_ranking/' file.
    if args.i == 'c':
        class_label = SuspiciousRankingClassLabel(args.p)
        class_label.process_class_label()

if __name__ == "__main__":
    main()
