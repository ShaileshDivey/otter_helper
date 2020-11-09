import os, sys, configparser, datetime, shutil, json
import pandas as pd
import yaml
from nbconvert import PythonExporter
from nbconvert import PDFExporter
from sys import exit
from pathlib import Path
from bs4 import BeautifulSoup
from shutil import copyfile
import glob
import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.preprocessors import CellExecutionError
import argparse
import os
import numpy as np

CWD = os.getcwd()
TESTS_DIR = 'tests'
CONFIG_DIR = 'config'
GRADE_FILE= 'final_grades.csv'
ROSTER_FILE= 'roster.xlsx'
METADATA= 'meta.json'
REQUIREMENTS_FILE = 'requirements.txt'
ASSIGNMENTS_DIR = 'assignments'
OUTPUT_DIR = 'output'
GRADE_DIR = ''
JSON_DIR = 'json'
NOTEBOOKS_DIR = 'notebooks'
META_KEY = 'identifier'
META_FILE = 'filename'
GRADES_KEY = 'identifier'
GRADES_FILE = 'file'
ROSTER_DIR = 'roster'
TMP_DIR='tmp'
CONFIG_DIR='config'
MISSING='MISSING'
MODULES_DIR='modules'
CONFIG_FILE= 'config.yml'

def load_yaml(file):
    """
    Loada a .yml file.
    """
    with open(file) as f:
        return yaml.safe_load(f)

def get_config(course, assignment, base_dir):
    """
    This sets some useful configuration based on the config file.
    """
    config_file = base_dir / CONFIG_DIR / course / CONFIG_FILE
    cf = load_yaml(config_file)
    cf['grade_assignment']=assignment
    cf['base_path']= base_dir
    cf['assignments_path']= base_dir / ASSIGNMENTS_DIR / course / assignment
    cf['roster_path']=base_dir / CONFIG_DIR / course / ROSTER_FILE
    cf['grades_output_path']=  base_dir /  OUTPUT_DIR /  course / assignment
    cf['json_output_path']= base_dir / OUTPUT_DIR / course / assignment / JSON_DIR
    cf['tmp_path'] = base_dir / TMP_DIR
    cf['grade_file']= base_dir / TMP_DIR / GRADE_FILE
    # #make required directories
    if not os.path.exists(cf['grades_output_path']):
         os.makedirs(cf['grades_output_path'])

    return cf

def prepare_grade(cf,  cleanup=True):
    """
    This will get the submissions in a format to be graded.
    """
    #Cleanup if it exists.
    if cleanup==True and os.path.exists(cf['tmp_path']):
        shutil.rmtree(cf['tmp_path'])
    #Create the directorys
    if not os.path.exists(cf['tmp_path']):
        os.makedirs(cf['tmp_path'])

    submissions=[]
    #Getting submissions differently for github and blackboard
    if cf['assignments'][cf['grade_assignment']]['type'] == 'gc':
        ids= [os.path.join(o) for o in os.listdir(cf['assignments_path']) if os.path.isdir(os.path.join(cf['assignments_path'],o))]
        ids=ignore_dir(ids, cf['ignore'])
        #Loop
        for id in ids:
            submission={}
            submission['identifier'] = id
            #TBD need to alert if more than 1 file.
            status=get_file(cf['assignments_path'], id, cf['assignments'][cf['grade_assignment']]['extension'])
            submission['filename']=id+"_"+status['file']
            submissions.append(submission)
            copyfile(cf['assignments_path'] / id / status['file'], cf['tmp_path'] / submission['filename'])
            #Move files
            #submission[id]=(os.path.join(id,status['file']))

    elif cf['assignments'][cf['grade_assignment']]['type'] == 'bb':
        files=[os.path.join(o) for o in os.listdir(cf['assignments_path']) ]
        for file in files:
            if file.endswith(cf['assignments'][cf['grade_assignment']]['extension']):
                submission={}
                submission['identifier']=file.split('_')[1]
                submission['filename']=file
                submissions.append(submission)
                copyfile(cf['assignments_path'] / file, cf['tmp_path'] / file)
    else:
        print("The type is incorrect.")
    #It will grade all submissions by default.
    with open(cf['tmp_path'] /METADATA, 'w') as fp:
        json.dump(submissions, fp, indent=4)

    if cf['assignments'][cf['grade_assignment']]['extension'] !=  '.xlsx':
        copy_path(cf['base_path'] / cf['assignments'][cf['grade_assignment']]['tests_path'], cf['tmp_path'] / TESTS_DIR, overwrite = False)
        copyfile(cf['base_path'] / cf['assignments'][cf['grade_assignment']]['requirements'], cf['tmp_path'] / REQUIREMENTS_FILE)
        if 'files' in cf['assignments'][cf['grade_assignment']]:
            for file in cf['assignments'][cf['grade_assignment']]['files']:
                f=file.split('/')[-1]
                copyfile(cf['base_path'] / file, cf['tmp_path'] / f)
    return submissions

#Ignore Directories
def ignore_dir(dir_list, ignore):
    return (list(set(dir_list) - set(ignore)))

def copy_path(from_path, to_path, overwrite=True):
    if os.path.exists(to_path) and overwrite==True:
        shutil.rmtree(to_path)
    shutil.copytree(from_path, to_path)

def get_file(path, id, extension='.ipynb'):
    #Count the number of submission files
    status={}
    status['id']=id
    status['path'] = path / id
    files = glob.glob1(status['path'],"*"+extension)
    status['submission_count'] = len(files)

    #Different actions depending on number of submissions.
    if status['submission_count']==0:
        status['status_code']=1
        status['status_description']='1. No submission.'
        status['file']=MISSING
        print("warning: ", id, " is missing assignment." )
    elif status['submission_count']>1:
        print("warning: ", id, "submitted >1 notebook." )
        status['status_code']=2
        biggest_file=0
        for x in files:
            size = os.path.getsize(os.path.join(path,x))
            if size > biggest_file:
                status['file']=x
                biggest_file=size
        status['status_description']='2. Multiple files. Grading largest file: '+str(status['file'])
    else:
        status['status_code']=2
        status['file']=files[0]
        status['status_description']='2. Grading '+ str(status['file'])
    return status

def excel_grader(cf):
    solution = pd.read_excel(cf['base_path'] / cf['assignments'][cf['grade_assignment']]['solution_path'], sheet_name=cf['assignments'][cf['grade_assignment']]['solution_sheet'])
    #solution['qv']=solution['question'].astype(str)+solution['variable'].astype(str)
    solution['qv']=solution['variable'].astype(str)
    solution['answer']=solution['answer'].astype(np.float64)
    with open(cf['tmp_path'] / METADATA) as f:
        assignments=json.load(f)
    grades=pd.DataFrame()
    #Iterate on the different assignments.
    for assignment in assignments:
        grow=len(grades)
        grades.loc[grow,GRADES_KEY]= assignment[META_KEY]
        grades.loc[grow,GRADES_FILE]= assignment[META_FILE]
        try:
            submission = pd.read_excel(cf['tmp_path'] / assignment[META_FILE], sheet_name=cf['assignments'][cf['grade_assignment']]['solution_sheet'])
        except:
            print("Error opening ",assignment[META_FILE])
            grades.loc[grow,'STATUS']= "FILE-ERROR"
            continue

        submission.columns = submission.columns.str.lower()
        print(assignment[META_FILE], submission.columns)
        #submission['qv']=submission['question'].astype(str)+solution['variable'].astype(str)
        submission['qv']=solution['variable'].astype(str)
        total=0
        for index, srow in submission.iterrows():
            #print('match',srow['qv'], solution['qv'])
            match_row=solution.loc[solution['qv'] == srow['qv'],:]
            #print(match_row)
            #correct = np.float64(match_row['value'].ravel()[0])
            #answer = np.float64(match_row['value'].ravel()[0])
            if len(match_row)>0:
                correct=match_row['answer'].values[0]
                answer=srow['answer']
                tol=match_row['tolerance'].values[0]
                points=match_row['points'].values[0]
                grades.loc[grow,"sub-"+srow['qv']]=answer
                grades.loc[grow,"answer-"+srow['qv']]=correct
                grades.loc[grow,'pos-'+srow['qv']]=points
                #print(match_row['value'].values[0], type(match_row['value'].values[0]))
                #print(srow['value'], type(srow['value']) )
                #if match_row['value'].ravel()[0]==srow['value']:
                #if 5.0 ==
                #    grades.loc[grow,srow['qv']]=match_row['points']
                if not isinstance(answer, str):
                    if np.isclose(correct,answer, tol):
                        grades.loc[grow,'pts-'+srow['qv']]=match_row['points'].values[0]
                        total+=match_row['points'].values[0]
                    else:
                        grades.loc[grow,'pts-'+srow['qv']]=0
                else:
                    grades.loc[grow,'pts-'+srow['qv']]=np.nan

        grades.loc[grow,'total']=total
        grades.loc[grow,'possible']=solution['points'].sum()
        grades.loc[grow,'STATUS']= "GRADED"
        grow+=1
    grades.to_csv(cf['grade_file'],index=False)
    return grades

def prepare_blackboard_upload(cf, archive=True, details=True):
    #Read in the grading
    grades=pd.read_csv(cf['grade_file'])

    #This loads the blackboard template.
    blackboard=pd.read_excel(cf['roster_path'], sheet_name='blackboard')
    #This renames the blackboard column.
    blackboard.rename(columns={'ASSIGNMENT': cf['assignments'][cf['grade_assignment']]['bb_column']}, inplace=True)

    #Match up Github to Userid using the roster file.
    if cf['assignments'][cf['grade_assignment']]['type'] == 'gc':
        github=pd.read_excel(cf['roster_path'], sheet_name='github')
        grades=grades.merge(github, left_on='identifier', right_on='github_id', how = 'left')

    elif cf['assignments'][cf['grade_assignment']]['type'] == 'bb':
        grades.rename(columns={'identifier': 'Username'}, inplace=True)

    grades.sort_values(by=['Username'], inplace=True)

    #Iterate through blackboard.
    #counter
    complete = 0
    incomplete = 0

    for index, row in blackboard.iterrows():
        match_row=grades.loc[grades['Username'] == row['Username'],:]
        #print(match_row)
        if len(match_row)>0:
            complete =complete+1
            text=""

            for x in match_row.columns:
                text=text+x+": "+str( match_row[x].ravel()[0])+"<br>"
                blackboard.loc[index,cf['assignments'][cf['grade_assignment']]['bb_column']]=match_row['total'].ravel()[0]
                blackboard.loc[index,'Feedback Format']='HTML'
                if details:
                    blackboard.loc[index,'Feedback to Learner']=cf['message_complete']+text
                else:
                    blackboard.loc[index,'Feedback to Learner']=cf['message_complete']
        else:
            incomplete =incomplete+1
            blackboard.loc[index,cf['assignments'][cf['grade_assignment']]['bb_column']]=0
            blackboard.loc[index,'Feedback to Learner']=cf['message_incomplete']
            incomplete=incomplete+1

    #blackboard_df.loc[index,blackboard_total_col]=mangrade_df.loc[mangrade_df[mangrade_match_col] == row[blackboard_match_col],'total'].ravel()[0]
    blackboard.to_csv(cf['tmp_path'] / 'upload.csv', index = False)
    print("complete:", complete,"\nIncomplete:",incomplete,"\nTotal:",complete+incomplete)
    if archive:
        print("Archiving files in ")
        copy_path(cf['tmp_path'],cf['grades_output_path'])
    return blackboard
