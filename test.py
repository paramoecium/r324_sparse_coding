from numpy.random import randn
from sklearn.decomposition import sparse_encode
n = m = 100 # dimensions of our input
m = 200
input_x = randn(n, m)
new_dimensions = 10
#from sklearn.decomposition import MiniBatchDictionaryLearning
from sklearn.decomposition import DictionaryLearning
dl = DictionaryLearning(new_dimensions)
dl.fit(input_x)
code = sparse_encode(input_x, dl.components_)
import numpy
numpy.set_printoptions(precision=3, suppress=True)
print code
print len(code)
#print dl.components_
print "error:", dl.error_[-1]
