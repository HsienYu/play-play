import os
import sys
import pandas as pd
import numpy as np
import pickle
from tqdm import tqdm

#---------------------------------------------------------------------
if __name__ == '__main__':

	#Load
	N = pickle.load( open( "data/probMap.p", "rb"))
	print(N)

