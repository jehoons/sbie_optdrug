from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


html_file = "ATM.html" # PhantomJS로 만든 해당 WebPage(http://oncokb.org/#/gene/ATM)의 html파일

f = open(html_file)
tt = f.read()

pp = BeautifulSoup(tt, "lxml")

data = pp.find_all('div', attrs={'id':'annotatedTable_wrapper'}) # pp 내용중에서 div tag 이면서 id = 'annotatedTable_wrapper'인 element들을 list로 가져온다.

d2 = data.find_all('div', attrs={'class':'ng-binding'}) # data 내용중에서 class = 'ng-binding'인 element들을 list로 가져온다.

print(d2)