from bs4 import BeautifulSoup,SoupStrainer;
import cfscrape;
import json

domain = 'https://1337x.to/'

#input here
#this takes a search query as input and searches for it, then it returns the first movie link it finds
def takeInput(search_query):
    scraper = cfscrape.create_scraper()
    search_query = search_query.strip().replace(' ','+')
    search_url = domain+'search/'+search_query+'/1/'
    print(search_url)
    results = scraper.get(search_url)
    search_soup = BeautifulSoup(results.content,'html.parser')
    if search_soup.p.text.strip() == 'No results were returned. Please refine your search.':
        print(search_soup.p.text.strip())
        return None
    else:
        a = search_soup.find('td',attrs={'class': 'coll-1 name'})
        links = a.find_all('a')
        movie_url = domain+links[1].get('href')[1:]
        return movie_url

url = takeInput(input('Enter query: '))
if url != None:
    print(url)
    scraper = cfscrape.create_scraper()
    page = scraper.get(url)

    soup = BeautifulSoup(page.content,'html.parser')
    #magnet and download
    for link in soup.find_all('a'):
        #magnet
        if link.get('href').startswith('magnet'):
            magnet = link.get('href')
        #download
        elif '.torrent' in link.get('href'):
            download_link = link.get('href')
    #hash info
    info_hash = soup.find('div', attrs={'class': 'infohash-box'}).span.text

    #screenshots
    try:
        screenshots = []
        for src in soup.find_all('img', attrs={'class': 'img-responsive descrimg'}):
            screenshots.append(src.get('src'))
    except AttributeError:
        print('no screenshots')
        
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

    #summary
    summary = soup.find('div',attrs={'id': 'description'}).text
    text_remove = soup.find('div',attrs={'id':'description'}).strong.text
    summary = summary.replace(text_remove,'')


    vars = {
        'title' : title,
        'description' : desc,
        'genres' : genres,
        'summary': summary,
        'hash-info' : info_hash,
        'screenshots' : screenshots,
        'magnet' : magnet,
        'download' : download_link 
    }
    y = json.dumps(vars)
    print(y)