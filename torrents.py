from bs4 import BeautifulSoup;
import requests;

url = 'https://www.1377x.to/torrent/4931542/Captain-America-The-First-Avenger-2011-UHD-BluRay-2160p-DD-5-1-HDR-x265-BHDStudio/'
page = requests.get(url)

soup = BeautifulSoup(page.content,'html.parser')

