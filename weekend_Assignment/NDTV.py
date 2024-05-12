
import requests
from dateparser import parse
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime , timedelta
import re

source = 'NDTV'
# last_date = datetime.today().date() - timedelta(days=1)
today = datetime.today().date()

titles = []

def extract_date_from_string(string):
    # Define the regex pattern to match the date format
    pattern = r"([a-zA-Z]+) (\d{1,2}), (\d{4})"

    # Search for the pattern in the string
    match = re.search(pattern, string)

    if match:
        # Extract the matched groups
        month_str, day_str, year_str = match.groups()

        # Convert month string to its numerical representation
        month = datetime.strptime(month_str, "%B").month

        # Convert strings to integers
        day = int(day_str)
        year = int(year_str)

        # Create a datetime object
        date = datetime(year, month, day).date()
        
        return date
    else:
        return None

def get_article(url):
    """
    Get Articles from the Url
    """
    
    res = requests.get(url)
    soup = BeautifulSoup(res.content,features="lxml")
    
    row = {}
    try:
        row['title'] = soup.find('h1',{'class':'sp-ttl'}).text.strip()
        row['link'] = url 
        pubDate = soup.find('span',{'class':'pst-by_lnk'}).text
        row['pubDate'] = extract_date_from_string(pubDate)
        try:
            row['description'] = '\n'.join([p.text.strip() for p in  soup.find('div',{'class':'story__content'}).find_all('p')]).strip()
        except:
            row['description'] = '\n'.join([p.text.strip() for p in  soup.find('div',{'class':'sp-cn ins_storybody'}).find_all('p')]).strip()
    except Exception as e:
        # print(url)
        # print(e)
        pass
    return row


def get_articles_frm_page(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content,features='lxml')
    articles = []
    try:
        articles = soup.find('div',{'class':'lisingNews'}).find_all('div',{'class':'news_Itm'})
    except Exception as e:
        print(e)
    rows = []
    for article in articles:
        try:
            link = article.a.attrs['href']            
            # date = parse(article.find('span',{'class':'posted-by'}).text.split('|')[1]).replace(tzinfo=None)
            title = article.a.text.strip()     
            row = get_article(link)
            date = row['pubDate']

            if date > today:
                rows.append(row)
            elif date == today:
                if title not in titles:
                    rows.append(row)
            else:
                
                # print("no article_links found at :",url)
                
                return rows, True
        except:
            pass
                
                     
    if len(rows) > 0:
        return rows, False
    return rows, True

    

base_url = 'https://www.ndtv.com/latest'
final_list= [] 
page_no = 1
while True:
    page_url = base_url + f'/page-{page_no}'
    pg_articles,last_page = get_articles_frm_page(page_url)
    if last_page:
        break
    final_list.extend(pg_articles)
    print('Crawling page::',page_no)
    page_no +=1


# print(final_list)
# final_list = list(set(final_list))

df = pd.DataFrame(final_list)
df['DateFetched'] = datetime.now()
df['source']  = source
print(df)

df.to_csv('News_Articles.csv')














