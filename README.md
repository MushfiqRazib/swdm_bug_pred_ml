# swdm_bug_pred_ml
Exploring the Relationship between Design Metrics and Software Diagnosability using Machine Learning (IN2106, IN0012, IN4238)
# Software Design Metrics Extraction Tools For Bug Prediction by Machine Learning
This tool used Defects4J 5 projects Chart, Closure, Lang, Math and Time project to diagnose 345 bugs properties.
Defects4J: https://github.com/rjust/defects4j 

# COMMAND INFO
metrics-command: -i <r, c, s, t, d>__
r: fault localization suspiciousness ranking__
c: class generation
s: static metrics extraction
t: test suite matrix metrics extraction
d: dynamic metris extraction

path-command: -p <path-to-fault-localization-projects, path-to-dynamic-call-grpah>

# HOW TO RUN 
# STEP 1: FAULT LOCALIZATION SCRIPT TO GENERATE SUSPICIOUS RANKING FILE
 run the script using command: python main.py -i <metrics-command> -p <path-command>__
 Ex: python main.py -i r -p '/home/mra/Desktop/test/'__
 Fault Localization coverage information file i.e. spectra, matrix file location: '/home/mra/Desktop/test/'
 
 N.B.: To run other scripts, at first suspicious ranking file must have to generate. 
       So, STEP is mandatory.
 
# STEP 2: CLASS METRICS SCRIPT TO GENERATE CLASS LABEL FILE FROM SUSPICIOUSNESS RANKING FILES
  run the script using command: python main.py -i <metrics-command> -p <path-command>
  Ex: python main.py -i c -p '/home/mra/Desktop/test/'
  IMPORTANT: spectra_faulty_methods_diffu.csv file must be in the <path-command/spectra_faulty_methods_diffu.csv>
  before run the command.
  
# STEP 3: STATIC METRICS SCRIPT TO GENERATE STATIC METRICS FILE FROM 'staticmetrics' folder
  run the script using command: python main.py -i <metrics-command> -p <path-command>
  Ex: python main.py -i s -p '/home/mra/Desktop/test/'
  IMPORTANT: 'staticmetrics' folder contains all the codepro generated static metrics .csv file.
            And it should be located to <path-command/staticmetrics> i.e. '/home/mra/Desktop/test/staticmetrics/'

# STEP 4: TEST SUITE METRICS SCRIPT TO GENERATE TEST SUITE METRICS FROM SPECTRA, MATRIX FILE
  run the script using command: python main.py -i <metrics-command> -p <path-command>
  Ex: python main.py -i t -p '/home/mra/Desktop/test/'
  
# STEP 5: DYNAMIC METRICS SCRIPT TO GENERATE DYNAMIC METRICS FROM DYNAMIC CALL GRAPH, SPECTRA, MATRIX FILES
  run the script using command: python main.py -i <metrics-command> -p <path-command>
  Ex: python main.py -i d -p '/home/mra/Desktop/test/'
  IMPORTANT: 'dynamic_call_graph' folder contains all the dynamic call graph files. So, before run the command, 
  this folder should be under the <path-command>.
  For example '/home/mra/Desktop/test/dynamic_call_graph/'

# STEP 6:HOW TO RUN getcoverageinfo.py FILE
INPUT: script requires <path-to-defects4j> as command line argument
OUTPUT: output of the script is ~/Desktop/Defects4JCoverage.csv that lists Project, DefectId, and StatementCoverage for all the defects of Defects4J
HOW TO RUN: run the script using command: python getcoverageinfo.py <path-to-defects4j>
 REQUIREMENTS AND DEPENDENCIES: script requires Defects4J installed on system"
