from bs4 import BeautifulSoup;
import requests;

url = 'https://www.1377x.to/torrent/4931612/The-Spy-Who-Loved-Me-1977-1080p-BluRay-10bit-x265-HazMatt-mkv/'
page = requests.get(url)

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

