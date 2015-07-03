import argparse

from numpy.random import randn
from sklearn.decomposition import sparse_encode

import datetime
import numpy as np
from utils import *
from sklearn.decomposition import DictionaryLearning

SENSOR_DICT = {
	# PIR, 34 index is always broken and not provide any info
	'PIR': (1, 4, 13, 16, 18, 26, 31, 32, 37, 38, 39, 40),
	'Temp': (2, 5, 7, 14, 19, 27, 35),
	'Humi': (3, 6, 8, 15, 20, 28, 36),
	'Light': (9, 11, 22, 23, 41),
	'Sound': (10, 12, 24, 25, 29, 30, 42, 43, 44),
	'Magnet': (17, 21, 33),
	'WallBtn': (45,46,47,48),
}
DATATYPE_DICT = { # 0 means discrete, 1 means continuous
	'PIR': 0,
	'Temp': 1,
	'Humi': 1,
	'Light': 1,
	'Sound': 1,
	'Magnet': 1,
	'WallBtn': 0,
}

def sparse_coding(dimension, input_x, alpha, iteration, tolerance):
	#dl = DictionaryLearning(dimension)
	dl = DictionaryLearning(dimension, alpha, iteration, tolerance) 
	dl.fit(input_x)
	#np.set_printoptions(precision=3, suppress=True)
	#print code
	#print dl.components_
	print "error:", dl.error_[-1]
	
	return dl

def run(dimension,raw_data_dir,out_dir):
	with open('{}/filename.list'.format(raw_data_dir), 'r') as fp:
		filenames = fp.read().splitlines()
	sensor_data = list()
	for filename in filenames:
		path = '{}/{}'.format(raw_data_dir, filename)
		with Timer('open {} with ALL sensors'.format(filename)):
			#data = np.genfromtxt(path, usecols=range(1,49)
			data = np.genfromtxt(path, usecols=[1, 4, 13, 16, 18, 26, 31, 32, 37, 38, 39, 40, 9, 11, 22, 23, 41, 10, 12, 24, 25, 29, 30, 42, 43, 44]
				, delimiter=',').tolist()
			print "# of data:", len(data)
			sensor_data.extend(data)
	with Timer('Sparse Coding...'):
		print "# of ALL data as a whole:", len(sensor_data)
		dl = sparse_coding(dimension, sensor_data,out_dir, 1, 10000, 0.00001)
	with open('{}/atoms'.format(out_dir), "w") as op:
		for component in dl.components_:
			line = ', '.join(str(e) for e in component)
        		op.write( line + '\n')

	code = sparse_encode(input_x, dl.components_)

	with open('{}/codes'.format(out_dir), "w") as op:
		for coefficient in code:
			line = ', '.join(str(e) for e in coefficient)
        		op.write( line + '\n')	

	with open('{}/filename.list'.format(raw_data_dir), 'r') as fp:
		filenames = fp.read().splitlines()
  
def main():
	argparser = argparse.ArgumentParser()
	argparser.add_argument('raw_data_dir', type=str, help='the directory of list')
	argparser.add_argument('out_dir', type=str, help='the file of output data')
	argparser.add_argument('dimension', type=int, help='# of atoms in the dictionary')
	args = argparser.parse_args()
	args = vars(args)

	run(args['dimension'],args['raw_data_dir'],args['out_dir'])

if __name__ == '__main__':
	main()
