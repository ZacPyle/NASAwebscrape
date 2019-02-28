import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import pandas as pd
import xlsxwriter
import datetime
import pprint
import numpy as np


######### DEFINED FUNCTIONS ##########

def SBIRList(address):
    #this function will go through the page and grab all the state info urls from the NASA url
    
    page = requests.get(address)
    if page.status_code != 200:
        print('Issue retrieving state lists')
    
    soup = BeautifulSoup(page.content, 'html.parser')
    #Now we should have all the content on that page
    
    #Now search through your soup to find the section that has the state list, grab that, get the hyperlink
    SelList = soup.find('ul', class_ = 'selectionList')
    State = SelList.find_all('a')
    for atag in State:
        if atag.get_text() == 'State List':
            target = atag['href']
    
    return target





def CAcomp(address):
    #this function will get the companies in CA from the state url that was input
    
    page = requests.get(address)
    if page.status_code != 200:
        print('Issue retrieving CA companies')
    
    soup = BeautifulSoup(page.content, 'html.parser')
    #now we have the raw content of the state listings page
    
    accordion = soup.find(id = 'accordion')
    states = accordion.find_all('li')
    cali = states[2]
    #now we have pulled all the info for california companies from the states info list
    
    #we'll get lists of company names, city the company is in, and the project they're working on
    company_name = [name.get_text() for name in cali.select('.awardDetails h4')]
    company_project = [project.get_text() for project in cali.select('.awardDetails a')]
    
    awards = cali.select('.awardDetails')
    company_city = []
    for award in awards:
        basic_info = award.find_all('p')
        company_city.append(basic_info[1].get_text())
    
    return company_name, company_project, company_city







######## GLOBAL VARIABLES ###########




url = 'https://sbir.gsfc.nasa.gov/prg_sched_anncmnt'
base_url = 'https://sbir.gsfc.nasa.gov/'


######### SCRAPING THE INFORMATION ##############

#get the raw html and parse it from main webpage
page = requests.get(url)

if page.status_code != 200:
    print('Issue retrieving base url')
    quit()

print('NASA data successfully retrieved')

#parse the raw html
soup = BeautifulSoup(page.content, 'html.parser')


#makes a list of all the table rows that were found with the tr tag
rows = soup.find_all('tr')

#initialize an array that will be filled with my links
links = []

#use for loop because find_all() only works on single elements, not lists
for row in rows:
    
    #find all the attribute tags in each element of your list of rows
    atags = [items for items in row.find_all('a')]
    title = atags[0].get_text()
    
    if ('SBIR' in title) and ('2019' not in title) and ('Proposal' not in title):
        # We only want to pull the data from SBIR from 2018 and earlier; no proposals
        
        #the last a tag has the url we want
        aref_tags = atags[-1]
        href_tags = aref_tags['href']
        
        destination = base_url + href_tags
        links.append(destination)
        #now we have an array of hyperlinks for all the SBIR sections


year_links = [base_url + SBIRList(link) for link in links]
print('SBIR information for each year successfully retrieved')


company = []
project = []
city = []

# Make a counter and max length to keep track of scraping progress
count = 1
limit = len(year_links)




for year in year_links:
    #get the information for CA companies from each year's SBIR list
    
    comp, proj, cit = CAcomp(year)
    company.extend(comp)
    project.extend(proj)
    city.extend(cit)
    
    print('Obtained information on CA companies for SBIR listing: {}/{}'.format(count, limit))
    
    count += 1



# Now hash it and return it to a list to get rid of all duplicates
triple = list(zip(company, project, city))
CompanyList = list(set(triple))



############  Make a .txt of it #########

# Save the date so you can know the last time it was updated
date = str(datetime.date.today())

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('NASA_Small_Business.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write(0, 0, 'This sheet is up to date as of: ')
worksheet.write(0, 1, date)


# Start from the first cell. Rows and columns are zero indexed.
row = 3
col = 0

# Iterate over the data and write it out row by row.
for co, pj, ci in (CompanyList):
    worksheet.write(row, col,     co)
    worksheet.write(row, col + 1, pj)
    worksheet.write(row, col + 2, ci)
    row += 1




workbook.close()



