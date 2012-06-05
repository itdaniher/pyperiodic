from bs4 import BeautifulSoup
from urllib2 import urlopen
import itertools

# select the first table from the NIST "Ground levels and ionization energies for the neutral atoms" datasite
t = BeautifulSoup(urlopen("http://physics.nist.gov/PhysRefData/IonEnergy/tblNew.html")).findAll("table")[1]

# go from HTML to list of lists
t = [ [column.text for column in row.findAll("td")] for row in t.findAll("tr") ][2:-1]

# discard empty rows
t = [item for item in t if item[0] != '']

# replace unicode char \xa0 with empty string
dexa0 = lambda array: [item.replace(u'\xa0', '') for item in array]
t = map(dexa0, t)

# manual fixes for formatting errors in original HTML parsing
del t[0][10]
t[90] = [u'91', u'Pa', u'Protactinium', u'[Rn]', u'5f2', u'(3H4)', u'6d', u'7s2', u'(4,3/2)11/2', u'5.89  ', u'Sugar (1974)']
t[91] = [u'92', u'U', u'Uranium', u'[Rn]', u'5f3', u'(4Io9/2)', u'6d', u'7s2', u'(9/2,3/2)o6', u'6.1939', u'(1997), (2001)']
t[92] = [u'93', u'Np', u'Neptunium', u'[Rn]', u'5f4', u'(5I4)', u'6d', u'7s2', u'(4,3/2)11/2', u'6.2657', u'(1979), (1994), (1997)']

# bit of hacking to put electron configuration information in an array as the key of a dictionary at the end of the list
def configurationRearranger(row):
	row.append({row[1]:row[3:8]})
	del row[3:8]
	del row[5]
	return row

t = [configurationRearranger(row) for row in t]

electrons = reduce(lambda a,b: a.update(b) or a, [item[-1] for item in t], {})

flatten = lambda l: list(itertools.chain(*[[x] if type(x) in [str, unicode] else x for x in l]))

for key in electrons.keys():
	def unstuff():
		electrons[key] = [ item for item in electrons[key] if item != '' ]
		electrons[key][0] = electrons[key][0].strip('[]')
		if electrons[key][0] in electrons.keys():
			electrons[key][0] = electrons[electrons[key][0]]
			electrons[key] = flatten(electrons[key])
			unstuff()
	unstuff()
	try:
		int(electrons[key][-1][-1])
	except ValueError:
		electrons[key][-1] = electrons[key][-1]+'1'

