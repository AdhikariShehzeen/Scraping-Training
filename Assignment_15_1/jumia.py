import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
from lxml import etree  
import pandas as pd

page_no = 1
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
# url = f'https://www.jumia.co.ke/mlp-black-friday/phones-tablets/?{page_no}'
base_url = 'https://www.jumia.co.ke/mlp-jumia-official-stores/'
def get_section_url():
    res = requests.get(base_url)
    print(res)
    soup = BeautifulSoup(res.text,'lxml')
    section_urls = soup.find_all('a',{'class':'-db -pvs -phxl -hov-bg-gy05'})
    section_urls = [urljoin(base_url,a.attrs['href'].replace('#catalog-listing',''))for a in section_urls]
    # print(len(section_urls))
    # print(section_urls)
    if len(section_urls) == 0:
        print('No section url found')
    return section_urls
def get_product(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'lxml')
    product = {}
    name = soup.find('h1',{'class':'-fs20 -pts -pbxs'}).text.strip()  
    price = soup.find('span',{'class':'-b -ubpt -tal -fs24 -prxs'}).text.strip()
    try:
        image_url = soup.find('img',{'class':'-fw -fh'}).attrs['data-src'] 
    except:
        image_url = 'Not Available'

    try:
        desc = ''.join(li.text for li in soup.find('div',{'class':'markup -pam'}).ul.find_all('li'))
    except:
        desc = 'Not Available'
    try:
        size = ' | '.join(label.text for label in soup.find('div',{'class':'-phxs'}).find_all('label',{'class':'vl'}))
    except:
        size = 'Not Available'
    try:
        dom = etree.HTML(str(soup))
        brand = dom.xpath("//div[contains(text(), 'Brand')]/a")[0].text
    except:
        brand = 'Not Available'
    try:
        rating = soup.find('div',{'class':'-df -i-ctr -pbs'}).find('div',{'class':'stars _m _al'}).text 
    except:
        rating = 'Not Available'
    
    try:
        review = ' | '.join(p.text for p in soup.find('div',{'class':'cola -phm -df -d-co'}).find_all('p',{'class':'-pvs'}))
    except:
        review = 'Not Available'
    
    product['name'] = name
    product['price'] = price
    product['image_url'] = image_url
    product['description'] = desc
    product['size'] = size
    product['brand'] = brand
    product['rating'] = rating
    product['review'] = review
    # print('returning')
    return product



def get_product_list(url):
    # print('in get product')
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'lxml')
    articles = []
    try:
        articles = soup.find_all('article',{'class':'prd _fb col c-prd'})
    except Exception as e:
        print(e)
    product_list = []
    for article in articles:
        link = urljoin(base_url,article.find('a',{'class':'core'}).attrs['href'])
        product = get_product(link)
        if product:
             product_list.append(product)

    return product_list

def pagination(url):
    final_list = []
    for i in range(1,4):
        print('page::',i)
        page_url = url+f'?page={i}#catalog-listing'
        product_list = get_product_list(page_url)
        final_list.append(product_list)
    return product_list

            




section_urls = get_section_url()
product_details = []
for section_url in section_urls:
    print('url::::::::::::::::::::::::', section_url )
    product_details.extend(pagination(section_url))
    
print(len(product_details))

dataframe = pd.DataFrame(product_details)
dataframe.to_csv('products.csv')