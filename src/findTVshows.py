import os
import sys
import pandas as pd
import numpy as np
import requests
import re
from bs4 import BeautifulSoup
from tqdm import tqdm
#--------------------------------------------------------------------------------
if __name__ == '__main__':

	#Clear
	os.system('clear')

	shows = {}
	findStr = 'href="/episode_scripts.php?tv-show='
	for i in tqdm(range(287)):
		url = 'https://www.springfieldspringfield.co.uk/tv_show_episode_scripts.php?page=' + str(i+1)
		r = requests.get(url).text
		for j in range(len(r) - len(findStr)):
			curstring = r[j:j+len(findStr)]
			if (curstring == findStr):
				epstr = r[j:j+100]
				elements = epstr.split('"')
				show = elements[1]
				elements = show.split('=')
				shows[elements[-1]] = 1

	shows = list(shows.keys())
	with open('/Volumes/3-1TB-LaCie/data/moviescript_generator/shows2.txt','w') as f:
		for item in shows:
			f.write(item + '\n')
