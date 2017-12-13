import pandas as pd
from pandas import datetime
from datetime import timedelta
import os
import numpy as np
import scipy
from scipy import interpolate, signal
import mne
from mne.time_frequency import tfr_array_stockwell
import csv

def featureExtraction(preprocessedDataAndLabels, path, study, session):
    time = preprocessedDataAndLabels[0]
    #add time to each of the raw data matrices
    right_interpolated = np.insert(preprocessedDataAndLabels[3], 0, values = time, axis = 1)
    left_interpolated = np.insert(preprocessedDataAndLabels[1], 0, values = time, axis = 1)
    trunk_interpolated = np.insert(preprocessedDataAndLabels[2], 0, values = time, axis = 1)
    label = preprocessedDataAndLabels[4]

    #filter the data - NEED HELP. NOT SURE WHAT TO USE
    b, a = signal.butter(2, 0.1,btype = 'highpass')
    w0 = signal.lfilter(b, a, right_interpolated)
    w1= signal.lfilter(b, a, left_interpolated)
    w2 = signal.lfilter(b, a, trunk_interpolated)
    
    #sos filter- filter data with 2nd order, high-pass filter with 0.1 fc
    #sos = np.matrix([[1, -2, 1, 1, -1.9985, .9985], [1, -1, 0, 1, -.9985, 0]])
    #w0 = np.array(signal.sosfilt(sos, right_interpolated))
    #w1 = np.array(signal.sosfilt(sos, left_interpolated))
    #w2 = np.array(signal.sosfilt(sos, trunk_interpolated))

    #downsample labels and time

    #stockwell transform- extracting features using 1 sec windows- feature 1
    #last dimension must be time

    featureVectorAndLabels = []
    f1 = [[],[],[]]
##    for i in [w0, w1, w2]:
##        arr = [[],[],[]]
##        for j in range(1, 4):
##            data = i[:,(j,0)] #must include time as the last column
##            minfreq = -1
##            Nyquist = 90
##            maxfreq_old = math.floor(len(data)/2)
##            maxfreq = math.floor(maxfreq_old*3 / (Nyquist / 2))
##            freqSteps = 51
##            window_size = 1
##            samplingfreq = round((maxfreq - minfreq+1)/freqSteps)
##            [st_power, freqs] = tfr_array_stockwell(data, samplingfreq, minfreq, maxfreq, n_fft = window_size)  ##NEED HELP
##            endst=51;
##            #this is from the matlab code, needs to be changed
##            fv1=abs(st(2:endst,:));
##            fv1=(downsample(fv1,10,5));
##            arr[j] = fv1
##        f1[i] = arr


    #windowing
    f234567 = []
    windowLength=90;
    for t in range(6,len(w0[1]), 10):
        winStart=t-windowLength/2
        winEnd=t+windowLength/2
        if winStart<1:
            winStart=1
        elif winEnd>len(w0[1]):
            winEnd=len(w0[1])
        windowedDataRight=w0[winstart:winEnd,1:]
        windowedDataLeft=w1[winstart:winEnd,1:]
        windowedDataTrunk=w2[winstart:winEnd,1:]
        windowedData = [windowedDataRight, windowedDataLeft, windowedDataTrunk]
        f3 = []
        f2 = []
        f4 = []
        f5 = []
        f6 = []
        f7 = []
        for i in range(0,3):
            windowRLT = windowedData[i]
            #f2- mean
            mean = np.mean(windowRLT, axis=0)
            f2.extend(mean[0] - mean[1])
            f2.extend(mean[1] - mean[2])
            f2.extend(mean[0] - mean[2])
            #f3- variance
            var = np.var(windowRLT, axis=0)
            f3.extend(var)
            #f4- correlation coefficient
            x = np.corrcoef(windowRLT[:,0], windowRLT[:,1])
            f4.extend(x[0,1])
            x = np.corrcoef(windowRLT[:,0], windowRLT[:,2])
            f4.extend(x[0,1])
            x = np.corrcoef(windowRLT[:,1], windowRLT[:,2])
            f4.extend(x[0,1])
            #f5-entropy
            #f6- first and second dominant frequencies
            for i in range(0,3):
                a= abs(np.fft.fft(windowRLT[:,i]))
                orderedNdx = [b[0] for b in sorted(enumerate(a),key=lambda i:i[1], reverse= True)]
                orderedAmps = [b[1] for b in sorted(enumerate(a),key=lambda i:i[1], reverse= True)]
                maxAmps = orderedAmps[0:2]
                maxNdx = orderedNdx[0:2]
                f6.extend(maxAmps)
                f6.extend(maxNdx)
            #f7- energy
            energy = np.mean(np.square(windowRLT), axis=0)
            f7.extend(energy)
        f2.extend(f3+f4+f5+f6+f7)
        f234567.append(f2)

    f234567 = np.array(f234567)
    f234567 = f234567.transpose()
    labelModified = list(label)
    for i,v in enumerate(label):
        if v==0:
            labelModified[i] = 1
        if v==400:
            labelModified[i] = 2
        if v==600:
            labelModified[i] = 3
        if v==800:
            labelModified[i] = 4
            
    featureVectorAndLabels.append(f1)
    featureVectorAndLabels.append(f234567)
    featureVectorAndLabels.append(labelModified)
    writer = csv.writer(open(path+'featureVectorAndLabel', 'w'))
    for row in featureVectorAndLabels:
        writer.writerow(row)
    print("Finished extracting features for session", session, "\n")
