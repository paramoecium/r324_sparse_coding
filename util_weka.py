import numpy as np
from setting import *

def load_weikaFormat(filename, sensors):
    print 'Loading: (weka)'
    myCols = _str2Index(sensors)
    data = np.loadtxt(open(filename, 'r'), delimiter=', ', skiprows=0, usecols=myCols, dtype='object')
    time = np.loadtxt(open(filename, 'r'), delimiter=', ', skiprows=0, usecols={0}, dtype='object')
    return data, time

def _str2Index(sensorIDs):
    # input: "101S54_Sound"
    # output: the corresponding index in weka format
    sensorIndex = []
    for sensorID in sensorIDs:
        if sensorID[2].isdigit():# three digit
            nodeID = sensorID[0:3]
            sensorName = sensorID[3:]
            index = FEATURE_MAPPING[nodeID][sensorName]
        else:# two digit
            nodeID = sensorID[0:2]
            sensorName = sensorID[2:]
            index = FEATURE_MAPPING[nodeID][sensorName]
        sensorIndex.append(index)
    return sensorIndex

if __name__=='__main__':
    print 'Start:'
    filename = '2014-09-01'
    data = np.loadtxt(open(filename, 'r'), delimiter=', ', skiprows=0, dtype='object')
    print len(data), ' ', len(data[0])
    print data[0:2]
    print data[0, 45:49]
    exit(0)
    #########################
    sensors = ['101S54_Sound', '101S4_PIR']
    filename = '2014-09-01'
    data, time = load_weikaFormat(filename, sensors)
    data_tuple = load_weikaFormat(filename, sensors)
    print len(data)
    print data[0:5]
    print time[0:5]
    print 'data tuple: ', data_tuple
