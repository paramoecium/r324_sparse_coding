import numpy as np 
from matplotlib.mlab import PCA as mlabPCA
import datetime
import time
from sklearn import mixture
import sys
import argparse

import gc # garbage collection
# my util function
from util_weka import load_weikaFormat

# time conversion
_d = lambda t: datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
time2number = lambda t_datetime: time.mktime(_d(t_datetime).timetuple()) + 1e-6 * _d(t_datetime).microsecond

def writeCache(outputFilename, data):
    print 'Writing Cache: ', outputFilename 
    with open(outputFilename, 'w') as f1:
        data_str = data.astype(np.str)
        for line in data_str:
            line_write = ' '.join(line) + '\n'
            f1.write(line_write)

def getIO(sensorStr, baseName):
    ## sensorsStr: 'SPL' (in order)
    sensors = []
    addName = ''
    soundStr = 'allSound_'
    pirStr = 'allPIR_'
    lightStr = 'allLight_'
    ####################################
    ## Sepecify sensors
    sensors_sounds = ['101S54_Sound', '100S67_Sound', '100S69_Sound', '99S67_Sound', '102S58_Sound', '101S56_Sound', '102S56_Sound',     '99S61_Sound', '102S57_Sound']
    sensors_lights = ['99S65_Light', '99S60_Light', '100S65_Light', '100S60_Light', '102S55_Light']
    # remove problemetic '102S21_PIR'
    sensors_PIR = ['101S4_PIR', '102S12_PIR', '102S32_PIR', '102S33_PIR', '99S24_PIR', '100S3_PIR', '99S4_PIR', '102S31_PIR', '100S24_PIR', '100S14_PIR', '102S34_PIR', '102S11_PIR']
    ####################################
    if 'S' in sensorStr:
        sensors += sensors_sounds
        addName += soundStr
    if 'P' in sensorStr:
        sensors += sensors_PIR
        addName += pirStr
    if 'L' in sensorStr:
        sensors += sensors_lights
        addName += lightStr
    wholeName_outputFile = addName + baseName
    return sensors, wholeName_outputFile

def getBasename(name):
    # format: merge-year-month-daytoyear-month-day.dat
    name = name.split('.')[0].split('-')
    name = ''.join(name[1:])
    return name

if __name__=='__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('wekaFilePath', type=str, help='wekaFilePath, eg:merge-2014-09-01to2014-09-07.dat')
    argparser.add_argument('specifiedSensors', type=str, help='specifiedSensors, eg: SPL')
    args = argparser.parse_args()
    args = vars(args)
    print 'Start: word costruction'
    ## Input: raw data; weka format
    ## Output: .PCAcache
    ####################################
    # Weka format
    ####################################
    ## parameter setting
    wekaFilePath = args['wekaFilePath']

    ## Sparse Codings parameters:
    reducedDimension = 3
    baseName = getBasename(wekaFilePath)
    baseName = baseName + '_SparseCodingDimension{0}_weka.cache'.format(reducedDimension) 

    ####################################
    # Input argument: i.e. "SPL"
    specifiedSensors = args['specifiedSensors']
    ####################################
    allsensors, outputFile = getIO(specifiedSensors, baseName)

    ####################################
    # Load weka format
    ####################################
    ## loading data, return numpy array
    dataArray, t = load_weikaFormat(wekaFilePath, allsensors)
    ## convert the type: str to float
    #bug: make sure no '?'
    dataArray = dataArray.astype(np.float)
    gc.collect()
    
    ####################################
    ## Dimension Reduction: Sparse Coding
    ####################################
    print 'Sparse Coding:'
    # normalize every column respectively
    from sklearn.preprocessing import MinMaxScaler
    normalizer = MinMaxScaler() # feature range (0,1)
    dataArray_normalized = normalizer.fit_transform(dataArray)
    print dataArray_normalized
    # reduce to the specified dimension
    from learnDic import sparse_coding
    from sklearn.decomposition import sparse_encode
        
    dl = sparse_coding(reducedDimension, dataArray_normalized, 0.2, 1000, 0.0001)
    code = sparse_encode(dataArray_normalized, dl.components_)
    data_reduced = code
    print data_reduced
    print dl.components_    
    print 'iteration:', dl.n_iter_
    '''
    ####################################
    ## Dimension Reduction: PCA
    ####################################
    print 'PCA:'
    myPCA = mlabPCA(dataArray)
    data_reduced = myPCA.Y[:,0:reducedDimension]# reduce to the specified dimension
    print dataArray
    print data_reduced
    ####################################
	'''
    ####################################
    print 'data_reduced dimension: ', reducedDimension, data_reduced.shape
    writeCache(outputFile, data_reduced)
    print 'Output file: ', outputFile 
    print 'Done'
