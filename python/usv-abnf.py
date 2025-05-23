
data = """
# Fisher's Iris data set

The Iris flower data set or Fisher's Iris data set is a multivariate data set 
used and made famous by the British statistician and biologist Ronald Fisher 
in his 1936 paper The use of multiple measurements in taxonomic problems as an 
example of linear discriminant analysis.

---


Dataset orderSepal lengthSepal widthPetal lengthPetal widthSpecies
15.13.51.40.2I. setosa
24.93.01.40.2I. setosa

1505.93.05.11.8I. virginica
"""


sdata = """# Fisher's Iris data set


This is the data
Dataset orderSepal lengthSepal widthPetal lengthPetal widthSpecies
15.13.51.40.2I. setosa
24.93.01.40.2I. setosa
1505.93.05.11.8I. virginica

"""
from usv import USVReader
from pprint import pprint



thing = USVReader(sdata)
pprint(thing.data)
pprint(thing.groups)
thing.groups[0].records.append([1,2,3])
pprint(thing.data)

print(str(thing))
print(str(thing.groups[0].to_csv()))
