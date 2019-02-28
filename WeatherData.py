import requests
from bs4 import BeautifulSoup
import pandas as pd

page = requests.get('https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168')

soup = BeautifulSoup(page.content, 'html.parser')

seven_day = soup.find(id = 'seven-day-forecast')


'''
forecast_items = seven_day.find_all(class_ = "tombstone-container")
tonight = forecast_items[2]

#extract name of forecast item, short description, and temp low

period = tonight.find(class_ = 'period-name').get_text()
short_desc = tonight.find(class_ = 'short-desc').get_text()
temp_low = tonight.find(class_ = 'temp temp-low').get_text()
img = tonight.find('img')
desc = img['title']

print(desc)
'''


period_tags = seven_day.select(".tombstone-container .period-name")

periods = [pt.get_text() for pt in period_tags]
short_descs = [sd.get_text() for sd in seven_day.select('.tombstone-container .short-desc')]
temps = [t.get_text() for t in seven_day.select('.tombstone-container .temp')]
descs = [d['title'] for d in seven_day.select('.tombstone-container img')]


weather = pd.DataFrame({
    'period': periods,
    'short_desc': short_descs,
    'temp': temps,
    'descs': descs
    })

temp_nums = weather['temp'].str.extract("(?P<temp_num>\d+)", expand = False)
weather['temp_num'] = temp_nums.astype('int')

is_night = weather["temp"].str.contains("Low")
weather["is_night"] = is_night

rainy = weather['short_desc'].str.contains("Showers")
print(weather[rainy])

