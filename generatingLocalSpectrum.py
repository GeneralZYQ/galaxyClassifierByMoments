#this is used to generate useful local spectrum
import pandas as pd
import os
import time
import csv



path = "/Volumes/DISK1/CReadCSV/EllipticsPatternSpectrum"
files= os.listdir(path)
featuresCount = 20;
featuresIntervals = []

epsilon = 0.001;

for x in range(0,featuresCount):
	a = float(x) / 20.0
	featuresIntervals.append(a)


count = 0
for filename in files:
	if '.csv' in filename:
		print(filename)
		rawFileName = filename.split('_')[0]
		finalName = rawFileName + '_%d_spectrum.csv' % featuresCount
		fullPath = path + '/' + filename
		data = pd.read_csv(fullPath, header=None, index_col=False)

		count = count + 1
		r1 = data.iloc[0]
		r2 = data.iloc[1]
		print (r1.shape[0])

		print ("the start tieme is %s" % time.time())

		features = []
		
		for interval in featuresIntervals:
			currentMin = 1
			currentMinIndex = 20000
			for i in range(0, r1.shape[0]):
				ratio = data.iloc[0, i]
				if abs(ratio - interval) <= currentMin:
					currentMin = abs(ratio - interval)
					currentMinIndex = i

			features.append(data.iloc[1, currentMinIndex])


		print ('---')
		print (len(features))
		print (features)

		with open(finalName, 'wb') as myfile:
			wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
			wr.writerow(features)

	print ("the end tieme is %s" % time.time())

