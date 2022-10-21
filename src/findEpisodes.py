
from bs4 import BeautifulSoup
from collections import Counter 
import requests
import operator
import re
from tqdm import tqdm

class Script(object):
    def __init__(self, show):
        self.show = show
        self.url = "https://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=" + show

    def get_movie(self):
        return self.movie

    def get_text(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text)
        return soup

    def parse_text(self):
        text = self.get_text().findAll('div', {"class":"main-content-left"})[0]
        ##text = re.sub(r'\W+', ' ', text) #remove puncation from the text
        #return text.split()
        return text

    def find_all_occurences(self):
        return Counter(self.parse_text())

    def get_all_occurences(self):
        sorted_occurences = sorted(self.find_all_occurences().items(), key=operator.itemgetter(1))
        return sorted_occurences


if __name__ == "__main__":

    #Load Shows
    shows = []
    with open('/Volumes/3-1TB-LaCie/data/moviescript_generator/shows.txt','r') as f:
        for line in f:
            shows.append(line.rstrip())

    episodes = []
    for show in tqdm(shows):
        db = Script(show)
        soup = db.get_text()
        text = db.parse_text()
        for item in text:
            item = str(item)
            starts = [match.start() for match in re.finditer(re.escape('.php?tv-show='), item)]
            for start in starts:
                substring = item[start+13:-1]
                if ('episode=' in substring):
                    elements = substring.split('>')
                    episode = elements[0][:-1]
                    episode = episode.replace('amp;','')
                    episode = 'https://www.springfieldspringfield.co.uk/view_episode_scripts.php?tv-show=' + episode
                    episodes.append(episode)

    #Write
    with open('/Volumes/3-1TB-LaCie/data/moviescript_generator/episodes.txt','w') as f:
        for episode in episodes:
            f.write(episode + '\n')