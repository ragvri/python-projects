# gets url of all the episodes of the series

from urllib.request import urlopen
from bs4 import BeautifulSoup

url_main = "http://animeheaven.eu/i.php?a=Hunter%20x%20Hunter%202011"  # the url  which has all the list of episodes
# in the series

obj = urlopen(url_main)

main_page_info = obj.read()

main_soup = BeautifulSoup(main_page_info, 'html.parser')

url_to_add_in_front = "http://animeheaven.eu/"

main_parse = main_soup.find_all(class_="infoepbox")
for foo in main_parse:
    link = foo.find_all("a")
    for x in link:
        url_to_episode = x.get('href')
        url_to_episode = url_to_add_in_front + url_to_episode
        print(url_to_episode)
        obj2 = urlopen(url_to_episode)
