import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}
res = requests.get('https://www.imdb.com/chart/top/', headers=headers)
print(res)
soup = BeautifulSoup(res.text,'lxml')
# print(soup)
divs = soup.find_all('div', class_='sc-b189961a-0 hBZnfJ cli-children')
print(len(divs))
# print(divs[0].find('a').find('h3').text)
# print('https://www.imdb.com/'+ divs[0].find('a').attrs['href'])
# print(divs[0].find('span', class_='ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating').attrs['aria-label'])

movies = []
for div in divs:
    m_info = {}
    m_info['name'] = div.find('a').find('h3').text
    m_info['link'] = 'https://www.imdb.com/'+ div.find('a').attrs['href']
    m_info['rating'] = div.find('span', class_='ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating').attrs['aria-label'].replace('IMDb rating:','').strip()
    movies.append(m_info)

print(movies)

df = pd.DataFrame(movies)

df.to_excel('IMDB_Rating.xlsx')


