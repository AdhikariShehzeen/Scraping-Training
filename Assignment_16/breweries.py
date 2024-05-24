import requests
import json
import pandas as pd


url = 'https://www.brewersassociation.org/wp-content/themes/ba2019/json-store/breweries/breweries.json?nocache=1716465936929'
res = requests.get(url)
data = res.json()
print(len(data))
data_list =[]
for i,d in enumerate(data):
    print(i)
    dict = {}
    dict['Name'] = d.get('Name')
    dict['url'] = d['attributes'].get('url') 
    dict["Phone"] = d.get("Phone") 
    dict["Membership"] = d.get("Membership_Record_Item__c")
    dict["Membership_Date"] = d.get("Membership_Record_Paid_Through_Date__c")  
    dict["Membership_Status"] = d.get("Membership_Record_Status__c")  
    dict["BillingAddress"] = d.get("BillingAddress") 
    data_list.append(dict)

df = pd.DataFrame(data_list)
df.to_csv('data.csv')

    

