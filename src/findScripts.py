import requests
from collections import Counter 
from bs4 import BeautifulSoup
from tqdm import tqdm
import operator
import re
import sys
import numpy as np

#--------------------------------------------------------------------------------
class MovieScript(object):
    def __init__(self, url):
        self.movie = url
        self.url = url

    def get_movie(self):
        return self.movie

    def get_text(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text,features="html.parser")
        return soup

    def parse_text(self):
        
        try:
            text = self.get_text().findAll('div', {"class":"scrolling-script-container"})[0].text.lower()
            text = text.replace("'",'')
            text = re.sub(r'[^a-zA-Z0-9.]', ' ',text)
        except:
            text = ''
        return text 

    def find_all_occurences(self):
        return Counter(self.parse_text())

    def get_all_occurences(self):
        sorted_occurences = sorted(self.find_all_occurences().items(), key=operator.itemgetter(1))
        return sorted_occurences

#--------------------------------------------------------------------------------
if __name__ == "__main__":

    #Load Episodes
    episodes = []
    with open('/Volumes/3-1TB-LaCie/data/moviescript_generator/episodes.txt','r') as f:
        for line in f:
            episodes.append(line.rstrip())

    #Generate seperate threads
    skip = int(sys.argv[1])
    indices = np.arange(len(episodes))
    #print(len(indices))
    indices = indices[skip::8]
    #print(len(indices))
    #print(indices[:10])
   
    #Loop Through Episodes
    for i in tqdm(range(len(indices))):
        index = indices[i]
        episode = episodes[index]
        elements = episode.split('=')
        epno = elements[-1]
        elements = elements[-2].split('&')
        show = elements[0]
        show = show.replace('_','-')
        savename = show + '_' + epno
        db = MovieScript(episode)
        soup = db.get_text()
        text = db.parse_text()
        text = text.replace('  ',' ')
        text = text.replace('  ',' ')
        text = text.replace('  ',' ')
        with open('/Volumes/3-1TB-LaCie/data/moviescript_generator/scripts/' + str(savename) + '.txt','w') as f:   
            f.write(text + '\n')



