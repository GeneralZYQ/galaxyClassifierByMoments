#this is the a file used to draw local spectrums

import csv
import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import os
from operator import add


path = "/Volumes/DISK1/spectrums/spiral_50_spectrum"
files= os.listdir(path)
filesCount = len(files)

totalValues = []
for x in xrange(1,51):
	totalValues.append(0.0)

for filename in files:
	fullPath = path + "/" + filename
	df = pd.read_csv(fullPath, header=None)
	datas = df.iloc[0].tolist()
	totalValues = list(map(add, totalValues, datas))
	

# avaerage = totalValues / float(filesCount)


averageValues = [x / float(filesCount) for x in totalValues]
print (averageValues)

xAxis = []

for x in xrange(1, 51):
	xAxis.append(x / 50.0)

plt.plot(xAxis, averageValues, '-r', label='delta of indensity')
plt.title('Local Spectrum of Spirals')
plt.xlabel('Ratio of Area', color='#1C2833')
plt.ylabel('Delta of Indensity', color='#1C2833')
plt.legend(loc='upper left')
plt.grid()
plt.show()



# df1 = pd.read_csv('/Volumes/DISK1/spectrums/elliptic_50_spectrum/587727177913532487_50_spectrum.csv', header=None)

# print(len (df1.iloc[0].tolist()))



# print(len(xAxis))

# plt.plot(xAxis, df1.iloc[0].tolist())
# plt.show()