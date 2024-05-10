# Imports
import requests
import json

baseurl  = "https://rickandmortyapi.com/api/"
endpoint = "character"

def main_request(baseurl , endpoint, x):
    response = requests.get(baseurl+endpoint+ f"/?page={x}")
    return response

response = main_request(baseurl , endpoint, 1)
# print(response)

# To get the json response

# print(response.json())
# print(type(response.json()))

####---- Convert python dictionary to JSON Format String onject using json.dumps()

# print(json.dumps(response.json() , indent=4))

###--------------------------------------



### To get keys
# print(response.json().keys())

# Access specific key

# print(response.json()['info'])

def get_pages(response):
    pages = response.json()['info']['pages']
    return pages

# print(get_pages(response=response))

# # Paginationto completed


# # Create a function returns all the name and number of episodes from that pages
def parse_page(response):
     data_list = []
     for item in response.json()['results']:
        data = {}
        name = item['name']
        episodes = item['episode']
        data['name'] = name
        data['episode'] = episodes
        data_list.append(data)

     return data_list
    

# parse_page(response=response)


# # execute the parse page function for all 42 pages 

main_list = []

for index,page_no in enumerate(range(1, int(get_pages(response))+1), start=1):
    print('Scraping page::',index)
    response = main_request(baseurl , endpoint, page_no)
    # <parse page>
    data_list = parse_page(response)
    main_list.extend(data_list)

# print(main_list)

import pandas as pd
df = pd.DataFrame(main_list)
# print(df)

df.to_csv('results.csv')

