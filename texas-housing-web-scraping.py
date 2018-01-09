# author: Daniel Marrama

# This script uses har.com to scrape data including 
# lot size, built sqft. and stories of houses listed
# It will prompt a search where the user will type in an address
# and the program with retrieve the data for them

import bs4 as bs
import urllib.request

# Search har.com for the desired house and extract the URL from the page
def search_for_home():
    search = 'http://www.har.com/search/dosearch?for_sale=1&quicksearch='
    address_list = input('Please type street number, street name and town/city in Texas for the home you want information on (do not type "Texas" or "TX" at the end): ').split(' ')
    address_string = '+'.join(address_list)
    search_url = search + address_string
    sauce = urllib.request.urlopen(search_url)
    soup = bs.BeautifulSoup(sauce, 'lxml')
    

    for script in soup.find_all('script'):
        if '"ID":' in str(script.get_text()):
            ID = str(script.get_text()).split(',')[4].split('"')[3]
            WADDR = str(script.get_text()).split(',')[-6].split('"')[3]
            return str('http://www.har.com/' + WADDR + '/homevalue_' + ID)

    for a in soup.find_all('a', href=True):
        if '/sale_' in a['href']:
            return a['href']
            break

# Use the url from the search function to extract the built size, lot size and
# number of stories data. Some pages do not have the number of stories so there
# is an exception for that programmed in.
def housing_information(url):
    sauce = urllib.request.urlopen(url)
    soup = bs.BeautifulSoup(sauce, 'lxml')
    
    for div in soup.find_all('div', class_='features_cols'):
        print('\n'.join(s for s in str(div.text).split('\n') if 'built' in s.lower()))
        print('\n'.join(s for s in str(div.text).split('\n') if 'lot' in s.lower()))
    
    if soup.find(text='Stories:'):
        print('Number of stories: ', soup.find(text='Stories:').parent.find_next_sibling().text.split(' ')[0])
    else:
        print('Number of stories is not available.')

url = search_for_home()
housing_information(url)

