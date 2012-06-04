from bs4 import BeautifulSoup
from urllib2 import urlopen
t = BeautifulSoup(urlopen("http://physics.nist.gov/PhysRefData/IonEnergy/tblNew.html")).findAll("table")[1]
t = [ [column.text for column in row.findAll("td")] for row in t.findAll("tr") ][2:-1]
t = [item for item in t if item[0] != '']
dexa0 = lambda array: [item.replace(u'\xa0', '') for item in array]
t = map(dexa0, t)
