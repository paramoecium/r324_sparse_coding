from svm import svm_problem, svm_parameter
from svmutil import svm_train, svm_predict, svm_save_model, svm_read_problem
import argparse

label = {
	'vacant':1,
	'meeting':2,
	'selfStudy':3,
}

if __name__=='__main__':
	argparser = argparse.ArgumentParser()
	argparser.add_argument('topicFilePath', type=str, help='hdp_topic file')
	argparser.add_argument('labelFilePath', type=str, help='hdp_topic file')
	argparser.add_argument('outputDir', type=str, help='directory to save svm model')
	args = argparser.parse_args()
	args = vars(args)

	# with open(args.filePath, 'r') as fr:
	topicNum, X_train = svm_read_problem(args['topicFilePath'])
	X_train = X_train[1:] # abandon the first instance
	print X_train
	Y_train = []
	with open(args['labelFilePath'], 'r') as fp:
		for line in fp:
			line = line.rstrip().split(';')
			Y_train.append(label[ line[1] ])
	print Y_train
	prob = svm_problem(Y_train, X_train)
	param = svm_parameter('-v 12 -q')
	model = svm_train(prob, param)
	print model
	#svm_save_model('{}/svm_model'.format(args['outputDir']),model)
