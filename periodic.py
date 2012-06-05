from bs4 import BeautifulSoup
from urllib2 import urlopen
import itertools
from collections import OrderedDict

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
t[90] = [u'91', u'Pa', u'Protactinium', u'[Rn]', u'5f2', u'6d1', u'7s2', u'',  u'(4,3/2)11/2', u'5.89  ', u'Sugar (1974)']
t[91] = [u'92', u'U', u'Uranium', u'[Rn]', u'5f3', u'6d1', u'7s2', u'', u'(9/2,3/2)o6', u'6.1939', u'(1997), (2001)']
t[92] = [u'93', u'Np', u'Neptunium', u'[Rn]', u'5f4', u'6d1', u'7s2', u'', u'(4,3/2)11/2', u'6.2657', u'(1979), (1994), (1997)']
t[102] = [u'103', u'Lr', u'Lawrencium', u'[Rn]', u'5f14', u'', u'7s2', u'7p', u'2Po1/2?', u'4.9? ', u'Eliav et al. (1995)']
t[103] = [u'104', u'Rf', u'Rutherfordium', u'[Rn]', u'5f14', u'6d2', u'7s2', u'', u'3F2?', u'6.0? ', u'Eliav et al. (1995)']

# bit of hacking to put electron configuration information in an array as the key of a dictionary at the end of the list
def configurationRearranger(row):
	row.append({row[1]:row[3:8]})
	del row[3:8]
	del row[5]
	return row

t = [configurationRearranger(row) for row in t]

# turn a list of dictionaries into a dictionary
superdict = lambda l: reduce(lambda a,b: a.update(b) or a, l, OrderedDict())

electrons = superdict([item[-1] for item in t])

# turn an uneven list of lists into a list without decomposing strings
flatten = lambda l: list(itertools.chain(*[[x] if type(x) in [str, unicode] else x for x in l]))

for key in electrons.keys():
	def unstuff():
		""" recursive function to replace element notation for electron orbital configurations with the configuration, explicitly """
		# remove empty values
		electrons[key] = [ item for item in electrons[key] if item != '' ]
		# strip brackets from first values
		electrons[key][0] = electrons[key][0].strip('[]')
		# see if first value is the name of an element in 'electrons'
		if electrons[key][0] in electrons.keys():
			# if so, replace with the electron configuration of that element
			electrons[key][0] = electrons[electrons[key][0]]
			# flatten
			electrons[key] = flatten(electrons[key])
			# repeat
			unstuff()
	unstuff()
	# default formatting assumes that if no number listed, it's '1' - not good practice
	dontAssume = lambda l: [x+'1' if x[-1] in ['s', 'p', 'd', 'f'] else x for x in l]
	electrons[key] = dontAssume(electrons[key])

for key in electrons.keys():
	# replace list of strings with an ordered dictionary
	electrons[key] = OrderedDict([(orbital[0:-1],int(orbital[-1])) for orbital in electrons[key]])
