from bs4 import BeautifulSoup,SoupStrainer;
import cfscrape;

domain = 'https://1337x.to/'

#input here
#this takes a search query as input and searches for it, then it returns the first movie link it finds
def takeInput(search_query):
    scraper = cfscrape.create_scraper()
    search_query = search_query.strip().replace(' ','+')
    search_url = domain+'search/'+search_query+'/1/'
    print(search_url)
    results = scraper.get(search_url)
    
    strainer = SoupStrainer('td', attrs={'class': 'coll-1-name'})
    search_soup = BeautifulSoup(results.content,'html.parser')
    a = search_soup.find('td',attrs={'class': 'coll-1 name'})
    links = a.find_all('a')
    movie_url = domain+links[1].get('href')[1:]
    return movie_url

url = takeInput(input('Enter query: '))
scraper = cfscrape.create_scraper()
page = scraper.get(url)

soup = BeautifulSoup(page.content,'html.parser')
#magnet and download
for link in soup.find_all('a'):
    #magnet
    if link.get('href').startswith('magnet'):
        magnet = link.get('href')
    #download
    elif link.get('href').startswith('/download'):
        download_link = url+link.get('href')[1:]

#hash info
info_hash = soup.find('div', attrs={'class': 'infohash-box'}).span.text

#screenshots
screenshots = []
for src in soup.find_all('img', attrs={'class': 'img-responsive descrimg'}):
    screenshots.append(src.get('src'))

#cover image
a = soup.find('div',attrs={'class':'torrent-image'})
cover_img = a.find('img').get('src')

#title, genres and description
genres=[]
a = soup.find('div',attrs={'class': 'torrent-detail-info'})
#title
title = a.h3.text.strip()
#genres
for genre in a.find_all('span'):
    genres.append(genre.text.strip())
#description
desc = a.p.text.strip()

print(desc)