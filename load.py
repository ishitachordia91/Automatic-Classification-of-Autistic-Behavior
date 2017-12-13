import pandas as pd
from pandas import datetime
from datetime import timedelta
import os
import numpy as np
import scipy
from scipy import interpolate, signal
import mne
from mne.time_frequency import tfr_array_stockwell

#
#Load all the data and extract the necessary columns
#
def load(session, study, path):
    if(study == "Study1"):
        trunk = pd.read_csv(path+study+'/'+session +'/MITes_01_RawCorrectedData_Trunk.RAW_DATA.csv', header=None)
        leftwrist = pd.read_csv(path+study+'/'+session +'/MITes_08_RawCorrectedData_Left-wrist.RAW_DATA.csv', header=None)
        rightwrist = pd.read_csv(path+study+'/'+session +'/MITes_11_RawCorrectedData_Right-wrist.RAW_DATA.csv', header=None)
        #get the label, start time, and end time. vid1_LabelStartEnd[0] gives me the label 
        video1Annotation = pd.read_excel(path+study+'/'+session +'/Annotator1Stereotypy.annotation.xlsx', skiprows=1)
        phoneAnnotation = pd.read_excel(path+study+'/'+session +'/Phone.annotation.xlsx', skiprows=1)
        vid1_LabelStartEnd = [video1Annotation['/ANNOTATION/LABEL'],pd.to_datetime(video1Annotation['/ANNOTATION/START_DT']),
                              pd.to_datetime(video1Annotation['/ANNOTATION/STOP_DT'])]
        vid1_LabelStartEnd = removeDuplicates(2, vid1_LabelStartEnd, 2)
        vid1_LabelStartEnd = replaceTerm(0, vid1_LabelStartEnd, "Good Data", "sync")
        phone_LabelStartEnd = [phoneAnnotation['/ANNOTATION/LABEL'],pd.to_datetime(phoneAnnotation['/ANNOTATION/START_DT']),
                               pd.to_datetime(phoneAnnotation['/ANNOTATION/STOP_DT'])]
        rawAnnotation = [phone_LabelStartEnd, vid1_LabelStartEnd, vid1_LabelStartEnd]
    else:
        trunk = pd.read_csv(path+study+'/'+session +'/Wocket_02_RawCorrectedData_Torso.csv', header=None)
        leftwrist = pd.read_csv(path+study+'/'+session +'/Wocket_01_RawCorrectedData_Left-Wrist.csv', header=None)
        rightwrist = pd.read_csv(path+study+'/'+session +'/Wocket_00_RawCorrectedData_Right-Wrist.csv', header=None)
        #get the label, start time, and end time. vid1_LabelStartEnd[0] gives me the label 
        phoneAnnotation = pd.read_excel(path+study+'/'+session +'/Phone.annotation.xlsx', skiprows=1)
        video1Annotation = pd.read_excel(path+study+'/'+session +'/Annotator1Stereotypy.annotation.xlsx', skiprows=1)
        video2Annotation = pd.read_excel(path+study+'/'+session +'/Annotator2Stereotypy.annotation.xlsx', skiprows=1)
        vid1_LabelStartEnd = [video1Annotation['/ANNOTATION/LABEL'],pd.to_datetime(video1Annotation['/ANNOTATION/START_DT']),
                              pd.to_datetime(video1Annotation['/ANNOTATION/STOP_DT'])]
        vid1_LabelStartEnd = removeDuplicates(2, vid1_LabelStartEnd, 2)
        vid1_LabelStartEnd = replaceTerm(0, vid1_LabelStartEnd, "Good Data", "sync")
        vid2_LabelStartEnd = [video2Annotation['/ANNOTATION/LABEL'],pd.to_datetime(video2Annotation['/ANNOTATION/START_DT']),
                              pd.to_datetime(video2Annotation['/ANNOTATION/STOP_DT'])]
        phone_LabelStartEnd = [phoneAnnotation['/ANNOTATION/LABEL'],pd.to_datetime(phoneAnnotation['/ANNOTATION/START_DT']),
                               pd.to_datetime(phoneAnnotation['/ANNOTATION/STOP_DT'])]
        rawAnnotation = [phone_LabelStartEnd, vid1_LabelStartEnd, vid2_LabelStartEnd]
    #format the raw data times
    trunk[0] = pd.to_datetime(trunk[0], unit = 'ms')
    rightwrist[0] = pd.to_datetime(rightwrist[0], unit = 'ms')
    leftwrist[0] = pd.to_datetime(leftwrist[0], unit = 'ms')
    rawData = [trunk, leftwrist,rightwrist]
    print("Finished loading data for session", session, "\n")
    return rawData, rawAnnotation 

#
#Find the search term in the col of the arr and replace the searchTerm with the ReplaceTerm
#
def replaceTerm(col, arr, searchTerm, replaceTerm):
    for row, _ in enumerate(arr[col]):
        if(arr[col][row] == searchTerm):
            arr[col][row] = replaceTerm
    return arr

#
#Remove duplicates in the array based on checkCol starting at the start row for multidimensional array
#

def removeDuplicates(start, arr, checkCol):
    numCols = len(arr)
    output = [[] for i in range(numCols)]
    for row, _ in enumerate(arr[0]):
        if row < start:
            for c in range(0, numCols):
                output[c].append(arr[c][row])
    for row, _ in enumerate(arr[0]):
        if row >= start:
            if arr[checkCol][row-1] != arr[checkCol][row]:
                for c in range(0, numCols):
                    output[c].append(arr[c][row])
    return output
