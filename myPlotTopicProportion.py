import argparse
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle# legend
from utils import *

def get_color_settings(topic_num):
	##### color
    # 'bgrcmykw'
	color = ['b','g','r','c','m','y','k','olive', 'steelblue', 'purple', 'chocolate', \
	'coral', 'darkgoldenrod', 'darkgreen', \
	'darkkhaki', 'darkmagenta', 'deeppink', \
	'firebrick', 'peru','gainsboro', 'papayawhip', 'yellowgreen']

	if topic_num < len(color):
		color = color[:topic_num]
	elif topic_num > len(color):
		for i in xrange(topic_num-len(color)):
			color.append(np.random.rand(3,))
	return color

def build_y(topics, topic_num):
	total_doc = len(topics)
	yy = np.zeros([total_doc, topic_num])
	for ind, t in enumerate(topics):
		tmp = t.split()
		# 2, 1:0.2, 3:0.8
		total = 0
		for tt in tmp[1:]:
			tmp2 = tt.split(':')
			total += float(tmp2[1])
		for tt in tmp[1:]:
			tmp2 = tt.split(':')
			yy[ind][int(tmp2[0])] = float(tmp2[1]) / total

	return yy

def run(data_dir, out_dir):

	## Read settings
	dates = list()
	with open('{}/settings'.format(data_dir), 'r') as fp:
		window_size = int(fp.readline().strip())
		topic_num = int(fp.readline().strip())
		for line in fp:
			dates.append(line.strip())

	## Get different colors
	color = get_color_settings(topic_num)

	## Get data
	with open('{}/hdp_topic'.format(data_dir), 'r') as fp:
		topics = fp.read().split("\n")

	yy_topics = build_y(topics, topic_num)

    ##### legend
	legendList = []
	for idx in xrange(len(color)):
	    legendList.append('topic{0}'.format(idx))

	## x_time
	x_time = list()
	for d in dates:
		theDate = dt.datetime.strptime(d, '%Y-%m-%d')
		delta = dt.timedelta(minutes=window_size)
		segment_size = int(1440/window_size)
		for i in xrange(segment_size):
			x_time.append(theDate + i * delta)

	## Plot!
	for index, day in enumerate(dates):
		begin = index * segment_size
		end = (index+1) * segment_size

		x = x_time[begin:end]
		y = yy_topics[begin:end]

		#### compute entropy
		yy_entropy = []
		for idx in xrange(len(y)):
			entropy = 0
			for p in y[idx]:
				if p:
					entropy = entropy + (-1*p*np.log(p))
			yy_entropy.append(entropy)

		### compute entropy first derivative, use central gradient
		yy_entropy_1 = np.gradient(yy_entropy)

		### compute entropy second derivative, use central gradient
		# yy_entropy_2 = np.gradient(yy_entropy_1)
		
		fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)

        ### plot grid
		ax1.grid(True);
		ax2.grid(True)#plt.grid(True)
		ax3.grid(True)

		## stackPlot
		stack_coll = ax1.stackplot(x, y.transpose(), colors=color, linewidth=0.01)
		
		ax2.plot(x, yy_entropy)
		ax3.plot(x, yy_entropy_1)
		##### legend
		# make proxy artists
		proxy_rects = [Rectangle((0, 0), 1, 1, fc=pc.get_facecolor()[0]) for pc in stack_coll]
		# make the legend
		ax1.legend(proxy_rects, legendList, loc='upper right', bbox_to_anchor=(1.135,0.5), prop={'size':7.5})
		#
		ax1.axhline(y=1, color='black', linewidth=1)
		ax2.axhline(y=0, color='black', linewidth=1)
		ax3.axhline(y=0, color='black', linewidth=1)

		## set title
		dateOfFile = x_time[begin].strftime('%Y-%m-%d')
		ax1Title = 'Topic proportion {0}'.format(dateOfFile)
		ax2Title = 'Entropy {0}'.format(dateOfFile)
		ax3Title = 'First Derivative Entropy {0}'.format(dateOfFile)
		ax1.set_title(ax1Title, fontsize=7)
		ax2.set_title(ax2Title, fontsize=7)
		ax3.set_title(ax3Title, fontsize=7)

		fig.autofmt_xdate()
		plt.xlabel('time')
		#
		pathName = out_dir + "/" + dateOfFile
		# if begin == 1:
		# 	import pdb; pdb.set_trace()
		plt.savefig(pathName, bbox_inches='tight')
		plt.close()




def main():
	argparser = argparse.ArgumentParser()
	argparser.add_argument('raw_data_dir', type=str, help='the directory of list')
	argparser.add_argument('out_dir', type=str, help='the file of output data')
	args = argparser.parse_args()
	args = vars(args)

	mkdir_p(args['out_dir'])

	run(args['raw_data_dir'], args['out_dir'])

if __name__ == '__main__':
	main()
