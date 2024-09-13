from urllib.request import urlopen, Request
import json

API_URL = "https://api.dineoncampus.com/v1/sites/todays_menu?site_id=64872d0f351d53058416c3d5"
HDR = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

response = urlopen(Request(API_URL, headers=HDR))
data_json = json.loads(response.read())
#print(data_json)
location = data_json['locations'][0]['name']
meal_periods = data_json['locations'][0]['periods'][0]['name']
items = data_json['locations'][0]['periods'][0]['stations'][0]['items']
for item in items:
    print(f"  - Name: {item['name']}, Calories: {item['calories']}, Portion: {item['portion']}")




print(f"Location: {location}")
print(f"Meal Period: {meal_periods}")
print("Menu:")



