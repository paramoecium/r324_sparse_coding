import numpy as np
import datetime
import time
from sklearn import mixture
import gc # garbage collection
import argparse
from gensim import corpora, models, similarities
from utils import *
import math

WINDOW_SIZE = 1 # mins

# time conversion
_d = lambda t: datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
time2number = lambda t_datetime: time.mktime(_d(t_datetime).timetuple()) + 1e-6 * _d(t_datetime).microsecond

def WordConstruction(wordID_list, number_wordType, outputFile):
    print "Word Construction:"
    documentSize = 600# 10 minutes
    print 'Document size: ' + str(documentSize) + ' sec.'
    documents = []
    count = 0
    #### Overlap every 5 minutes: move half length of documentSize each time
    ## the first document: 5 minutes 300 words
    ## the last document: 5 minutes 300 words
    ## other documents: 10 minutes 600 words and overlap for 5 minutes
    overlapParameter = 0.5
    # The first docment:
    words = wordID_list[0: 0 + int(documentSize * overlapParameter)]
    line_count = _wordCount(words, number_wordType)
    documents.append(line_count)
    # Other documents:
    while(count * documentSize * overlapParameter + 600 <= len(wordID_list)):
        #DELETE:words = wordID_list[count * documentSize: (count+1) * documentSize]
        startIdx = int(count * documentSize * overlapParameter)
        words = wordID_list[startIdx: startIdx + documentSize]
        line_count = _wordCount(words, number_wordType)
        documents.append(line_count)
        count = count + 1
    # The last document:
    startIdx = int(count * documentSize * overlapParameter)
    words = wordID_list[startIdx: startIdx + int(documentSize * overlapParameter)]
    line_count = _wordCount(words, number_wordType)
    documents.append(line_count)
    print 'Total Documents: ', len(documents)
    print "Write file:"
    # write to LDA format
    _write(documents, outputFile)

def _wordCount(words,n):
    # bug: word ID: 1 to n, not 0 to n-1
    #hist = [0 for x in range(n+1)]# bug DELETE
    # bug: word ID: 0 to n-1, not 1 to n
    hist = [0 for x in range(n)]# bug
    # count histogram
    try:
        for index in words:
            hist[index] += 1
    except IndexError:
        print 'IndexError: ', index
    # append into line index:countNumber
    line_count = ''
    numberOfUniqueWord = 0
    for index, countNumber in enumerate(hist):
        if countNumber:# filter out zero count
            numberOfUniqueWord = numberOfUniqueWord + 1
            line_count = line_count + str(index)+':' + str(countNumber) + ' '
    line_count = line_count.strip()
    line_count = str(numberOfUniqueWord) + ' ' + line_count
    return line_count

def _write(data, filename_w):
    #filename_w = '5sound_100clusters_.documents'
    with open(filename_w, 'w') as f1:
        for line in data:
            line = str(line) + '\n'
            f1.write(line)

def readCache(filename):
    length = 0
    with open(filename, 'r') as f1:
        for line in f1:
            item = line.split(' ')
            length = len(item)
            break
    print 'Read cache:'
    print 'Length: ', length
    columns = [i for i in range(length)]
    data = np.loadtxt(open(filename, 'r'), delimiter=' ', skiprows=0, usecols=columns, dtype='object')
    return data.astype(np.float)

def getDimension(filename):
    # assume at most two digit PCA dimension 
    item = 'Dimension'
    idx = filename.index(item)
    idxOfDimension = idx + len(item)
    if "DimensionNO" in filename:
        print "NO PCA"
        return "NO"
    if not filename[idxOfDimension+1].isdigit():# one digit
        dimension = int(filename[idxOfDimension])
    else:# two digits
        dimension = int(filename[idxOfDimension:idxOfDimension+2])
    return dimension
        
def getSensorName(readName):
    addName = ''
    if "allSound_" in readName:
        addName += "allSound_"
    if "allPIR_" in readName:
        addName += "allPIR_"
    if "allLight_" in readName:
        addName += "allLight_" 
    return addName
    ####################################
    ##Chang's hdp alternative help func#
    ####################################
def window(x_arr):
	window = WINDOW_SIZE * 60
	num_windows = int(math.ceil(len(x_arr) / window)) + 1
	print 'num_windows:', num_windows

	# From 00:00 to 23:59 , 1 mins, total 1440 mins
	# First interval is 1 mins, Last interval is 1 mins
	# Others are 2 mins (before 1 min, after 1 min)

	# return window array for input
	window_x_arr = np.zeros([num_windows, len(x_arr[0])])

	window_x_arr[0] = np.sum(x_arr[0:window], axis=0)
	window_x_arr[-1] = np.sum(x_arr[-window:], axis=0)

	for i in xrange(1, num_windows):
		data = x_arr[window*(i-1) : window*(i+1)]
		# vertical sum up
		window_x_arr[i] = np.sum(data, axis=0)

	return window_x_arr

def hdp_topic(window_x_arr, out_dir):
	dictionary = []
	corpus = []
	hdp = []
	hdp_corpus = []
	tmp = []
	for docu in window_x_arr:
		tmp2 = []
		for index, wordcount in enumerate(docu):
			if wordcount > 0:
				# Add the number of words into corpus
				for i in xrange(int(wordcount)):
					tmp2.append(str(index))
		tmp.append(tmp2)

	with Timer('HDP topic modeling'):
		dictionary = corpora.Dictionary(tmp)
		corpus = [dictionary.doc2bow(text) for text in tmp]
		hdp = models.hdpmodel.HdpModel(corpus, id2word=dictionary, \
			gamma=0.01, alpha=0.01)
		hdp_corpus = hdp[corpus]

	# hdp.print_topics(topics=20, topn=10)
	## Remove non-shown topic number
	topic_ind = 0
	topic_dict = dict()
	for m in hdp_corpus:
		for n in m:
			if not topic_dict.has_key(n[0]):
				topic_dict[n[0]] = topic_ind
				topic_ind += 1

	print 'Total topic number', topic_ind
	# import pdb; pdb.set_trace()
	with open('{}/hdp_topic'.format(out_dir), 'w') as op, Timer('Writing to file'):
		for ind, m in enumerate(hdp_corpus):
			op.write(str(len(m))+" ")
			for n in m:
				op.write(str(topic_dict[n[0]])+":"
					+str(n[1])+" ")
			op.write("\n")
	return topic_ind
#########################################
##             main                     #
#########################################
if __name__=='__main__':
	argparser = argparse.ArgumentParser()
	argparser.add_argument('data_filename', type=str, help='data_filename')
	argparser.add_argument('out_dir', type=str, help='the file of output data')
	args = argparser.parse_args()

	print '\
####################################\n\
#              DPGMM               #\n\
####################################'
	## DPGMM parameters:
	#n = 100
	n = 10
	a = 1
	####################################
	'''
	Input
		.cache file
	Output
		.documents
	'''
	readfilename = args.data_filename
	out_dir = args.out_dir

	reducedDimension = getDimension(readfilename)
	if 'SparseCoding' in readfilename:
		baseName = 'alpha{0}_{1}clusters_SparseCoding_Dimension{2}_5weka.documents'.format(a, n, reducedDimension)
	elif 'PCA' in readfilename:
		baseName = 'alpha{0}_{1}clusters_PCA_Dimension{2}_5weka.documents'.format(a, n, reducedDimension)
	addName = getSensorName(readfilename)
	outputFile = addName + baseName
	####################################
	print 'Reading...'
	data_reduced = readCache(readfilename)
	#for sparse coding only in case that DPGMM doesn't split data apart	
	if 'SparseCoding' in readfilename:       
		for v in range(len(data_reduced)):
			for i in range(len(data_reduced[0])):
				data_reduced[v][i] = data_reduced[v][i]*10
		print data_reduced
	print 'DPGMM...'
	## DPGMM learning
	t1 = time.time()
	dataDimension = len(data_reduced[0,:])
	levelRepresentation = []
	for idx in xrange(dataDimension):
		g = mixture.DPGMM(n_components=n, alpha=a)
		sensor_data = data_reduced[:,idx]
		x = sensor_data[0]
		for d in sensor_data[1:]:
			x = np.vstack((x, d))
		g.fit(x) # learn whole
		y = g.predict(x)
		levelRepresentation.append(y.reshape(-1,1))
		gc.collect()

	levelRepresentation = tuple(levelRepresentation)
	data_reduced = np.hstack(levelRepresentation)
	print 'Dicretized data:'
	print data_reduced
	t2 = time.time(); print 'Time: ', (t2-t1), ' sec.'; print ''
	####################################
	## construct word vector and word ID
	####################################
	print 'Construct word vector:'
	t1 = time.time()
	corpusLength = len(data_reduced[:,0])
	words = []
	wordsID = {} # hash_key to corresponding word index, for assignment
	wordIndex = 0
	wordID_list = []
	for i in xrange(corpusLength):
		hash_key = tuple(data_reduced[i,:])
		words.append(hash_key)
		if hash_key not in wordsID:
			wordsID[hash_key] = wordIndex
			wordIndex = wordIndex + 1
		wordID_list.append(wordsID[hash_key])
	t2 = time.time(); print 'Time: ', (t2-t1), ' sec.';
	gc.collect()
	numberOfWordType = wordIndex
	print 'Vocabulary size: ' + str(wordIndex)
	print 'wordID length: ' + str(len(wordsID)) 
	print ''

	print '\
####################################\n\
#                HDP               #\n\
####################################'
	####################################
	##     Chang's hdp alternative     #
	####################################
	window_x_arr = window(data_reduced)
	## Do HDP here
	print 'HDP...'
	topic_num = hdp_topic(window_x_arr, out_dir)
	# import pdb; pdb.set_trace()
	## Print original sensor data in windows
	with open('{}/sensor'.format(out_dir), 'w') as op, Timer('write file {}'.format(out_dir)):
		for line in window_x_arr:
			print line
			out_arr = list()
			for i,v in enumerate(line):
				if v != 0 and not np.isnan(v):
					out_arr.append(str(i)+":"+str(v))

			print >> op, len(out_arr), " ".join(out_arr)
	## Print parameters... date and window size
	filenames = []
	with open('timestamp', 'r') as fp:
		for line in fp:
			t_str = datetime.datetime.fromtimestamp(float(line)).strftime('%Y-%m-%d')
			if len(filenames) == 0 or filenames[-1] != t_str:
				filenames.append(t_str)
	with open('{}/settings'.format(out_dir), 'w') as op:
		print >> op, WINDOW_SIZE
		print >> op, topic_num
		for f in filenames:
			print >> op, f
	####################################
	## Write to LDA
	t1 = time.time()
	WordConstruction(wordID_list, numberOfWordType, outputFile)
	t2 = time.time(); print 'Time', (t2-t1), ' sec.'
	print 'output file: ', outputFile
