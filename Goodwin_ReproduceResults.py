#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
from pandas import datetime
from datetime import timedelta
import os
import numpy as np
import scipy
from scipy import interpolate, signal
import mne
from mne.time_frequency import tfr_array_stockwell
import label
import load
import featureExtraction

path = '/Users/ishitachordia/Documents/Thomas_Agata_Research/GoodwinData/test/'
study = 'Study0'

##README: there are four parts of this: loadData, labelData, featureExtraction, classification.
#Look at stereotypyMain.m to see how Goodwin did it- we need to follow it exactly
#preprocessedDataAndLabels is exactly the same as Goodwin. When I start back up, start with featureExtraction
#Steps To Do:
#1. You load the Hd.mat in python and use it to filter the preprocessedData
#2. Figure out how to do Stockwell transform
#3. Classify then using what they did + Neural nets
##When I start back up, you can run matlab code by going on https://mycloud.gatech.edu/Citrix/GTMyCloudWeb/
##Documentation: https://docs.google.com/document/d/12cjQ6QPVeTjPgOZZtoWGJ0Wqh9KEk20LOLi3qEW17D4/edit#
##How accelerometer data works: http://stackoverflow.com/questions/5871429/accelerometer-data-how-to-interpret
	
if __name__ == '__main__':
    for studyType in os.listdir(path):
          study = studyType
          if(studyType != '.DS_Store'):
              for session in os.listdir(path+study):
                  if(session != '.DS_Store'):
                      rawData, rawAnnotation = load.load(session, study, path)
                      preprocessedDataAndLabels = label.label(rawData, rawAnnotation, session, study)
                      featureExtraction.featureExtraction(preprocessedDataAndLabels, path, study, session) 
