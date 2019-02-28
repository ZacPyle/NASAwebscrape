import requests
from bs4 import BeautifulSoup

page = requests.get("http://dataquestio.github.io/web-scraping-pages/ids_and_classes.html")
soup = BeautifulSoup(page.content, 'html.parser')

'''
outer_text = soup.find_all('p', class_ = 'outer-text')

for i in range(len(outer_text)):
    print( outer_text[i].get_text() )
    print( ' ' )
'''

divp = soup.select('div p')
print(divp[1].get_text())
