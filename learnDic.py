import argparse

from numpy.random import randn
from sklearn.decomposition import sparse_encode

import datetime
import numpy as np
from utils import *
from sklearn.decomposition import DictionaryLearning

def sparse_coding(dimension, input_x, out_dir):
	dl = DictionaryLearning(dimension)
	dl.fit(input_x)
	code = sparse_encode(input_x, dl.components_)

	np.set_printoptions(precision=3, suppress=True)
	print code
	print dl.components_
	print "error:", dl.error_[-1]
	with open('{}/atoms'.format(out_dir), "w") as op:
		for component in dl.components_:
			line = ', '.join(str(e) for e in component)
        		op.write( line + '\n')
	with open('{}/codes'.format(out_dir), "w") as op:
		for coefficient in code:
			line = ', '.join(str(e) for e in coefficient)
        		op.write( line + '\n')


def run(dimension,raw_data_dir,out_dir):
	with open('{}/filename.list'.format(raw_data_dir), 'r') as fp:
		filenames = fp.read().splitlines()
	sensor_data = list()
	for filename in filenames:
		path = '{}/{}'.format(raw_data_dir, filename)
		with Timer('open {} with ALL sensors'.format(filename)):
			data = np.genfromtxt(path, usecols=range(1,45)
				, delimiter=',').tolist()
			print "# of data:", len(data)
			sensor_data.extend(data)
	with Timer('Sparse Coding...'):
		print "# of ALL data as a whole:", len(sensor_data)
		sparse_coding(dimension, sensor_data,out_dir)
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
