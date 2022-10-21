import os
import sys
import pandas as pd
import numpy as np
import pickle
from tqdm import tqdm

#---------------------------------------------------------------------
if __name__ == '__main__':

	#keywords
	word = "right"

	#Load
	N = pickle.load( open( "data/probMap.p", "rb"))
	
	#Loop
	script = ''
	for i in range(100):
		script = script + word + ' '
		values = N[word]
		indices = np.argsort(values[1])[::-1]
		randval = np.random.randint(30)
		index = indices[randval]
		word = values[0][index]
		
	print(script)

