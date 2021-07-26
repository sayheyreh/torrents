from bs4 import BeautifulSoup;
import requests;

url = 'https://www.1377x.to/torrent/4931612/The-Spy-Who-Loved-Me-1977-1080p-BluRay-10bit-x265-HazMatt-mkv/'
page = requests.get(url)

soup = BeautifulSoup(page.content,'html.parser')
for link in soup.find_all('a'):
    if link.get('href').startswith('magnet'):
        magnet = link.get('href')
    elif link.get('href').startswith('/download'):
        download_link = url+link.get('href')[1:]
for hash in soup.find_all('div', attrs={'class': 'infohash-box'}):
    info_hash = hash.span.text
screenshots = []
for src in soup.find_all('img', attrs={'class': 'img-responsive descrimg'}):
    screenshots.append(src.get('src'))
for img in soup.find_all('img'):
    if img.get('src').startswith('/img'):
        cover_img = url+src.get('src')[1:]
genres=[]
for a in soup.find_all('div',attrs={'class': 'torrent-detail-info'}):
    title = a.h3.text.strip()
    for genre in a.find_all('span'):
        genres.append(genre.text.strip())
    desc = a.p.text.strip()
