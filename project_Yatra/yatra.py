import requests
import pandas as pd
from datetime import datetime, timedelta
import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Training"]
collection = db["yatra"]

def get_data():
   api_url = f'https://flight.yatra.com/lowest-fare-service/seodom/get-fare?origin=BOM&destination=DEL&from={from_date}&to={to_date}&tripType=O&airlines=all&_i=417636858974&src=srp'
   res = requests.get(api_url, headers=headers)
   data = res.json().get('day')
   return data


def get_flight_details(from_date, to_date, data):

   from_date = datetime.strptime(from_date, '%d-%m-%Y').date()
   to_date = datetime.strptime(to_date, '%d-%m-%Y').date()
   date_list = [(from_date + timedelta(days=x)).strftime('%Y-%m-%d') for x in range((to_date - from_date).days + 1)]
   flight_data = []
   for date in date_list:
      print('Fetching Flights for date::', date)    
      af_data = data[date]["af"]
      

      # Iterate through the airlines in 'af' data

      for airline, details in af_data.items():
         if 'tf' in details and 'ow' in details:
            for flight in details['ow']:
                  flight_info = {
                     'flight_name': flight.get('an', ''),
                     'flight_code': flight.get('ac', '') + '-' + str(flight.get('fl', '')),
                     'departure': flight.get('dac', ''),
                     'dep_datetime': flight.get('ddt', ''),
                     'arrival': flight.get('aac', ''),
                     'arr_datetime': flight.get('adt', ''),
                     'cabin': flight.get('cabin', ''),
                     'total_fare': 'Rs.'+ str(details.get('tf', ''))
                  }
                  flight_data.append(flight_info)

   return flight_data





#--------------------------------------MAIN-----------------------------------------------------------

headers = {'Cookie': '_abck=04326FE708A482FD048D2F79C131434B~-1~YAAQrl3SFzHlxbmPAQAACd7zwwuxY3gSAPaDPzSeVyAHPF6ozgW/jdUHXbognx0egvu992MAzi5hk3SGr+WEmFa6ghT8QlbzptZhby9glWNnL6iW6yHOqT8U1zOcYWUzrzIVOhkgwglbu+y2CiuRVBg6TAPtAeRddzLIFR7rHQSFtqlBavBHEn9xUG4azIdBWtCUd6Fol+QQMx6/aa6VeaZ4jySAWi5LE//xkEoIB+chpWAjeOQglX2cRE0+5Y3/VTVubsiw42rNnXLg7BbAkmih6AJDPrxaG1j+lSuIxoXHFiP9DOqn17LxNAIXlq3/HRemgnPVPTF4n2cR5McvQMa/iV5AIJS+1MBDD83QaovU/XEwHZ/SeE1Wj8zX~-1~-1~-1; bm_sz=88A14F45154DE624D0E8F7AD919EA890~YAAQrl3SFzLlxbmPAQAACd7zwxfVl958ejxCD/z0GGfIEFLn6RbqM7RoJHPff7go8esNcTCghsRyqerOpkIbvnDYgV1zdJx02huHeZt9gIomP/S6KdX2ID/wpNFJTv2b1sPTUaw/b4gy70W2ZeHc8ZqPV2nKR8EELqx+vPxVvQojS42N+iQtrLVoPPLsNsJjNp83UQ3zEBH0MSwn+ZiluggjQDJTvXXfVL+H2oSgESi63FmBfIDSWXkn3s8FB5rFdjaLsFuGW92WW8XZHP1oiOelvn3M6a8tY3gjpkPZJTwIu+hKsqQEsVhyMVETEeHRADxphP/Gt94fpI0WygbpD/O2uWLB2AGUS+TWNMk=~3556933~3163703',
            'Connection': 'keep-alive',
            'Accept': '*/*', 
            'Accept-Encoding': 'gzip, deflate, br', 
           'User-Agent': 'PostmanRuntime/7.29.2',
            'Host': 'flight.yatra.com'}

base_url = 'https://www.yatra.com/flight-schedule/mumbai-to-delhi-flights.html'
from_date = '01-06-2024' #you have to change dates according to your preferance
to_date = '31-07-2024'
data = get_data()
flight_details = get_flight_details(from_date,to_date, data)

df = pd.DataFrame(flight_details)
df.to_excel('flights.xlsx', index=False)

for flight_info in flight_details:
    collection.insert_one(flight_info)






# print(type(from_date))
