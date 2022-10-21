import os
import sys
import pandas as pd
import numpy as np
import pickle
from tqdm import tqdm

#---------------------------------------------------------------------
if __name__ == '__main__':

	D = {}
	C = {}
	with open('data/scripts.txt','r') as f:
		for i in tqdm(range(116602)):
			line = f.readline()
			line = line.replace('.',' .')
			line = line.replace('?',' ?')
			line = line.replace('!',' !')
			tokens = line.split(' ')
			for m in range(len(tokens)-1):
				word1 = tokens[m]
				word2 = tokens[m+1]
				if word1 in C:
					value = C[word1]
					C[word1] = value + 1
				else:
					C[word1] = 1
				if word1 in D:
					words,values = D[word1]
					if word2 in words:
						index = words.index(word2)
						value = values[index] + 1
						values[index] = value
						D[word1] = (words,values)
					else:
						words.append(word2)
						values.append(1)
				else:
					words = [word2]
					values = [1]
					D[word1] = (words,values)

	
	#Normalize
	N = {}
	for word1 in D:
		count = C[word1]
		if (count > 50):
			words2,values = D[word1]
			totalval = np.sum(values)
			values = np.array(values)
			values = values.astype('float') / totalval
			N[word1] = (words2,values)

	#Store
	pickle.dump(N, open( "data/probMap.p", "wb" ) )



		