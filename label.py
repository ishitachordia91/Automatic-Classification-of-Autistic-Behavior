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
#Label the raw data with the labels from raw annotation file
#
def label(rawData, rawAnnotation, session, study):
    phone_LabelStartEnd = rawAnnotation[0]
    vid1_LabelStartEnd = rawAnnotation[1]
    vid2_LabelStartEnd = rawAnnotation[2]
    trunk = rawData[0]
    leftwrist = rawData[1]
    rightwrist = rawData[2]

    #Round off the milliseconds
    vid1_LabelStartEnd[1] = roundDateTimeMilli(vid1_LabelStartEnd[1])
    vid1_LabelStartEnd[2] = roundDateTimeMilli(vid1_LabelStartEnd[2])
    #Change the start and end times of the labels into milliseconds
    #phone_LabelStartEnd[1] = dateTimeToMillisecond(phone_LabelStartEnd[1])
    #phone_LabelStartEnd[2] = dateTimeToMillisecond(phone_LabelStartEnd[2])
    vid1_LabelStartEnd[1] = dateTimeToMillisecond(vid1_LabelStartEnd[1])
    vid1_LabelStartEnd[2] = dateTimeToMillisecond(vid1_LabelStartEnd[2])
    #edit the first two sync rows so that they're the same
    vid1_LabelStartEnd[2][0] = vid1_LabelStartEnd[1][0]
    vid1_LabelStartEnd[1][0] = vid1_LabelStartEnd[1][0]-500
    vid1_LabelStartEnd[1][1] = vid1_LabelStartEnd[2][1]
    vid1_LabelStartEnd[2][1] = vid1_LabelStartEnd[2][1]+500
 
    #Create three vectors that have the original raw data times converted to milliseconds
    rawData_TimesMillis = [dateTimeToMillisecond(trunk[0]), dateTimeToMillisecond(leftwrist[0]),
                           dateTimeToMillisecond(rightwrist[0])]
    rawData_TimesMillis[0] = duplicatesDrop(rawData_TimesMillis[0])
    rawData_TimesMillis[1] = duplicatesDrop(rawData_TimesMillis[1])
    rawData_TimesMillis[2] = duplicatesDrop(rawData_TimesMillis[2])    
    
    #create a vector with time periods based on the sampling rate
    if(study == "Study1"):
        samplingPeriod = (1/60.0)*1000
    else:
        samplingPeriod = (1/90.0)*1000
        
    startTime = max(rawData_TimesMillis[0][0],rawData_TimesMillis[1][0],rawData_TimesMillis[2][0])
    endTime = min(rawData_TimesMillis[0][len(rawData_TimesMillis[0])-1],rawData_TimesMillis[1][len(rawData_TimesMillis[1])-1],
                  rawData_TimesMillis[2][len(rawData_TimesMillis[2])-1])
    samplingRateVector = np.arange(startTime, endTime, samplingPeriod)
    
    #interpolate the data so there is 1 data point for each time period in sampling rate vector
    trunk_interpolated = [np.interp(samplingRateVector, rawData_TimesMillis[0], trunk[1]),
                          np.interp(samplingRateVector, rawData_TimesMillis[0], trunk[2]),
                          np.interp(samplingRateVector, rawData_TimesMillis[0], trunk[3])]
    leftwrist_interpolated = [np.interp(samplingRateVector, rawData_TimesMillis[1], leftwrist[1]),
                          np.interp(samplingRateVector, rawData_TimesMillis[1], leftwrist[2]),
                          np.interp(samplingRateVector, rawData_TimesMillis[1], leftwrist[3])]
    rightwrist_interpolated = [np.interp(samplingRateVector, rawData_TimesMillis[2], rightwrist[1]),
                          np.interp(samplingRateVector, rawData_TimesMillis[2], rightwrist[2]),
                          np.interp(samplingRateVector, rawData_TimesMillis[2], rightwrist[3])]
          
   #upsample the data for study1 so its 90Hz
    if(study == "Study1"):
        trunk_interpolated = [multirate.resample(trunk_interpolated[0], 9, 6),
                              multirate.resample(trunk_interpolated[1], 9, 6),
                              multirate.resample(trunk_interpolated[2], 9, 6)]
        leftwrist_interpolated = [multirate.resample(leftwrist_interpolated[0], 9, 6),
                                  multirate.resample(leftwrist_interpolated[1], 9, 6),
                                  multirate.resample(leftwrist_interpolated[2], 9, 6)]
        rightwrist_interpolated = [multirate.resample(rightwrist_interpolated[0], 9, 6),
                                   multirate.resample(rightwrist_interpolated[1], 9, 6),
                                   multirate.resample(rightwrist_interpolated[2], 9, 6)]
        samplingPeriod = (1/90.0)*1000
        samplingRateVector = np.arange(startTime, endTime+samplingPeriod, samplingPeriod)
        #don't thinki need this one
        rawData_TimesMillis = [multirate.resample(rawData_TimesMillis[0], 9, 6),
                                   multirate.resample(rawData_TimesMillis[1], 9, 6),
                                   multirate.resample(rawData_TimesMillis[2], 9, 6)]

    #label raw data using annotations- only video 1 annotations were used in the final study
    vid1_Label = np.zeros(len(samplingRateVector))
    for row in range(0, len(vid1_LabelStartEnd[0])):
        startTime = vid1_LabelStartEnd[1][row]
        endTime = vid1_LabelStartEnd[2][row]
        label = vid1_LabelStartEnd[0][row]
        #get index of first value in samplingRateVector that startTime is within 5.55ms
        startIndex = np.where(np.logical_and(samplingRateVector >= (startTime-5.55),
                                                   samplingRateVector <= (startTime+5.55)))[0][0]
        endIndex = np.where(np.logical_and(samplingRateVector >= (endTime-5.55),
                                                   samplingRateVector <= (endTime+5.55)))[0][0]
        vid1_Label = fillArrayWithValue(vid1_Label, startIndex, endIndex, label)

    times = samplingRateVector
    times = times - times[0] +1 #tr, tl, tt

    #Sync the videos up
    indexSyncLabel = [i for i,v in enumerate(vid1_Label) if v == 50]
    timesSyncLabel = [v for i,v in enumerate(samplingRateVector) if i in indexSyncLabel]
    normalizedStartTimeSyncLabel = [abs(x- vid1_LabelStartEnd[2][0]) for x in timesSyncLabel]
    normalizedEndTimeSyncLabel = [abs(x- vid1_LabelStartEnd[1][1]) for x in timesSyncLabel]
    endIndexArr = [i for i,v in enumerate(normalizedEndTimeSyncLabel) if v < 2500]
    startIndexArr = [i for i,v in enumerate(normalizedStartTimeSyncLabel) if v < 1500]
    if(len(endIndexArr) > 0 and len(startIndexArr) > 0):
        sR = indexSyncLabel[startIndexArr[len(startIndexArr)-1]]
        eR = indexSyncLabel[endIndexArr[0]]
    if(len(endIndexArr) > 0 and len(startIndexArr) == 0):
        sR = 0
        eR = indexSyncLabel[endIndexArr[0]]
    if(len(endIndexArr) == 0 and len(startIndexArr) > 0):
        sR = indexSyncLabel[startIndexArr[len(startIndexArr)-1]]
        eR = None
    vid1_Label = vid1_Label[sR+1:eR]
    times = times[sR+1:eR]
    leftwrist_interpolated = np.array(leftwrist_interpolated).transpose()
    leftwrist_interpolated = leftwrist_interpolated[sR+1:eR]
    trunk_interpolated = np.array(trunk_interpolated).transpose()
    trunk_interpolated = trunk_interpolated[sR+1:eR]
    rightwrist_interpolated = np.array(rightwrist_interpolated).transpose()
    rightwrist_interpolated = rightwrist_interpolated[sR+1:eR]
        
    preprocessedDataAndLabels = [times, leftwrist_interpolated, trunk_interpolated, rightwrist_interpolated, vid1_Label]
    print("Finished labeling session", session, "\n")
    return preprocessedDataAndLabels            

#
#Input- a panda datetime column with hours, minutes, seconds, and microseconds
#Output- a vector where each datetime is converted to milliseconds
#

def dateTimeToMillisecond(data_pdTimestamp):
    msTimes = []
    for d in data_pdTimestamp:
        timeInMilliseconds = d.hour*60*60*1000 + d.minute*60*1000 + d.second*1000 + d.microsecond/1000
        msTimes.append(timeInMilliseconds)
    return msTimes

def roundDateTimeMilli(arr):
    for i, val in enumerate(arr):
        ms = val.microsecond
        ms = ms/1000
        if ms>90:
            ms=ms
        elif ms<1:
            ms=ms*100;
        else:
            ms=10*(ms-floor(ms))
        ms= ms*1000
        arr[i] = arr[i].replace(microsecond = ms)
    return arr


#
#Input- an array, the start and end indeces, the value to fill with
#Output- the array replaced with the value from indeces start_i to end_i
#

def fillArrayWithValue(arr, start_i, end_i, value):
    i = start_i
    intVal = 0         ##BE CAREFUL ABOUT sync and "good data"
    if(value == "rock" or value == "Rock"):
        intVal = 400
    elif(value == "flap" or value == "Flap"):
        intVal = 800
    elif(value == "flap-rock" or value == "Flap-Rock"):
        intVal = 600
    elif(value == "sync"):
        intVal = 50
    while i <= end_i:
        arr[i] = intVal
        i += 1
    return arr

#
#Remove duplicate elements in an array
#
            
def duplicatesDrop(arr):
    seen = set()
    seen_add = seen.add
    return [x for x in arr if not (x in seen or seen_add(x))]
