from bs4 import BeautifulSoup
import cfscrape;
import json
from flask import Flask,render_template,request,jsonify

app = Flask(__name__)
app.config["DEBUG"] = True
domain = 'https://1337x.to/'

#input here
#this takes a search query as input and searches for it, then it returns the first movie link it finds
def takeInput(search_query):
    if len(search_query)>2:
        search_query = search_query.replace(' ','+')
    scraper = cfscrape.create_scraper()
    search_url = domain+'category-search/'+search_query+'/Movies/1/'
    print(search_url)
    results = scraper.get(search_url)
    search_soup = BeautifulSoup(results.content,'html.parser')
    print(search_url)
    if search_soup.title.text.strip() == 'No results were returned. Please refine your search.':
        print(search_soup.p.text.strip())
        return None
    elif search_soup.title.text.strip() == 'Error something went wrong.':
        print(search_soup.p.text.strip())
        return None
    else:
        print(search_url)
        a = search_soup.find('td',attrs={'class': 'coll-1 name'})
        links = a.find_all('a')
        movie_url = domain+links[1].get('href')[1:]
        return movie_url

@app.route('/',methods=('GET','POST'))
def index():
    if request.method=='POST':
        query = request.form.get('query')
        url = takeInput(query)
    return render_template('index.html')

@app.route('/<query>',method=('POST','GET'))
def search_torrent(query):
    url=takeInput(query)
    return jsonify(get_json(url))

def get_json(url):
    if url != None:
        print(url)
        scraper = cfscrape.create_scraper()
        page = scraper.get(url)

        soup = BeautifulSoup(page.content,'html.parser')

        #magnet and download
        try:
            for link in soup.find_all('a'):
                #magnet
                if link.get('href').startswith('magnet'):
                    magnet = link.get('href')
                #download
                elif '.torrent' in link.get('href'):
                    download_link = link.get('href')
        except:
            magnet=''
            download=''
        
        
        #hash info
        try:
            info_hash = soup.find('div', attrs={'class': 'infohash-box'}).span.text
        except:
            info_hash=''

        #screenshots
        screenshots = []
        try:
            for src in soup.find_all('img', attrs={'class': 'img-responsive descrimg'}):
                screenshots.append(src.get('src'))
        except:
            print('no screenshots')
            
        #cover image
        try:
            a = soup.find('div',attrs={'class':'torrent-image'})
            cover_img = a.find('img').get('src')
        except:
            cover_img=''

        #title, genres and description
        genres=[]
        try:
            a = soup.find('div',attrs={'class': 'torrent-detail-info'})
        except:
            print('details')
        #title
        try:
            title = a.h3.text.strip()
        except:
            try:
                title = soup.find('div',attrs={'class':'box-info-heading clearfix'}).h1.text.strip()
            except:
                title=''
        #genres
        try:
            for genre in a.find_all('span'):
                genres.append(genre.text.strip())
        except:
            print('no genres')

        #description
        try:
            desc = a.p.text.strip()
        except:
            desc=''

        #summary
        try:
            summary = soup.find('div',attrs={'id': 'description'}).text
            text_remove = soup.find('div',attrs={'id':'description'}).strong.text
            summary = summary.replace(text_remove,'')
        except:
            summary=''

        vars = {
            'title' : title,
            'description' : desc,
            'genres' : genres,
            'summary': summary,
            'hash-info' : info_hash,
            'cover_image' : cover_img,
            'screenshots' : screenshots,
            'magnet' : magnet,
            'download' : download_link 
        }
        return vars
    return {'error':'movie not found'}
app.run()