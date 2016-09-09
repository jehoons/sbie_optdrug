from bs4 import BeautifulSoup
import re

html_file = 'ATM.html'

f = open(html_file)
tt = f.read()

pp = BeautifulSoup(tt, "html.parser")

data = pp.find_all('div', attrs={'class': 'ng-binding'})

#data = pp.find_all('div', attrs={'id': 'annotatedTable_wrapper'})

#d2 = data.find_all('div', attrs={'class': 'ng-binding'})

print data
