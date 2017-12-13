#!/usr/bin/env python
# encoding: utf-8
#https://code.tutsplus.com/tutorials/a-smooth-refresher-on-pythons-dictionaries--cms-25198

import pandas as pd
from matplotlib import pyplot
from pandas import datetime


def parser(x):
    nofrag, ms = x.split(".")
    m,s = divmod(int(nofrag), 60)
    h,m = divmod(m, 60)
    time = str(h) +"."+str(m)+"."+str(s)+"."+ms
    return datetime.strptime(time, "%H.%M.%S.%f")

data = pd.read_csv('accelerometeryData_03252017_1451.csv', header=None, index_col=0, date_parser=parser)
print(data.head())
print("Resample")
resample = data.resample('100L')        #Frequency of 10Hz
data_resampled = resample.mean()

print(data_resampled)
data_resampled.to_csv('resampledData_03252017_1451.csv', index=True, header=None)

#data.plot()
#pyplot.show()


#Questions
    #1. When sampling, the lowest frequency is 20Hz, but the data is inconsistent
    #2. Did 10 Hz, but that seems very infrequent to the point of not being relevant
    #3. Is this an interpolation problem? I don't think so. I think it's something wrong with the band.
