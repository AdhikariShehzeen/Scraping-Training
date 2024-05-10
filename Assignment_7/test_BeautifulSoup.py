import requests
from bs4 import BeautifulSoup
import pandas as pd

def product_details(res):
    soup = BeautifulSoup(res.text,'lxml')
    # print(soup)
    products = soup.find_all('div',{'class':'product-wrapper card-body'})
    # print(len(products))
    product_list = []
    for product in products:
        product_dict = {}
        product_dict['product_name'] = product.find('a',{'class':'title'}).attrs['title']
        product_dict['procuct_price'] = product.find('h4',{'class':'price'}).text.strip()
        product_dict['rating'] = product.find('div',{'class':'ratings'}).find_all('p')[1].attrs['data-rating']
        product_dict['reviews'] = product.find('div',{'class':'ratings'}).find_all('p')[0].text.strip()
        product_dict['product_link'] = 'https://webscraper.io'+ product.find('a',{'class':'title'}).attrs['href']
        product_list.append(product_dict)
    if len(product_list) > 0:
        return product_list, False
    
    return product_list, True

base_url = 'https://webscraper.io/test-sites/e-commerce/static/computers/tablets'
final_list = []
page_no = 1
while True:
    page_url = base_url + f'?page={page_no}'
    
    res = requests.get(page_url)
    product_list,last_page = product_details(res)
    if last_page:
        break
    final_list.extend(product_list)
    print('Crawling page::',page_no)
    page_no +=1

    
final_list = list(set(final_list))
# print(final_list)
df = pd.DataFrame(final_list)
# print(df)

df.to_excel('Test_products.xlsx', index=False)




