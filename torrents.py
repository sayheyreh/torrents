from bs4 import BeautifulSoup;
import cfscrape;

domain = 'https://1337x.to/'

#input here
#this takes a search query as input and searches for it, then it returns the first movie link it finds
def takeInput(search_query):
    scraper = cfscrape.create_scraper(delay=10)
    search_query = search_query.strip().replace(' ','+')
    search_url = domain+'search/'+search_query+'/1/'
    print(search_url)
    results = scraper.get(search_url)
    search_soup = BeautifulSoup(results.content,'html.parser')
    a = search_soup.find('td',attrs={'class': 'coll-1 name'})
    for links in a.find_all('a'):
        if links.get('href').startswith('/torrent'):
            movie_url = domain+links.get('href')[1:]
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
for hash in soup.find_all('div', attrs={'class': 'infohash-box'}):
    info_hash = hash.span.text

#screenshots
screenshots = []
for src in soup.find_all('img', attrs={'class': 'img-responsive descrimg'}):
    screenshots.append(src.get('src'))

#cover image
for img in soup.find_all('img'):
    if img.get('src').startswith('/img'):
        cover_img = url+src.get('src')[1:]

#title, genres and description
genres=[]
for a in soup.find_all('div',attrs={'class': 'torrent-detail-info'}):
    #title
    title = a.h3.text.strip()
    #genres
    for genre in a.find_all('span'):
        genres.append(genre.text.strip())
    #description
    desc = a.p.text.strip()
