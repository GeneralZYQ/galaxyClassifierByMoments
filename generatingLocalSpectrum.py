#this is used to generate useful local spectrum
import pandas as pd
import os
import time
import csv



path = "/Volumes/DISK1/CReadCSV/SpiralsZooSpectrumwithabc"
files= os.listdir(path)
featuresCount = 20.0;
featuresIntervals = []


for x in range(0,int(featuresCount)):
	a = float(x) / featuresCount
	featuresIntervals.append(a)

# print(featuresIntervals);


count = 0
for filename in files:
	if '.csv' in filename:
		print(filename)
		# if count < 209:
		# 	count = count + 1
		# 	continue
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
			currentMinIndex = -1
			for i in range(0, r1.shape[0]):
				ratio = data.iloc[0, i]
				if abs(ratio - interval) <= currentMin:
					currentMin = abs(ratio - interval)
					currentMinIndex = i

			if currentMinIndex >= 0:
				features.append(data.iloc[1, currentMinIndex])
			else:
				features.append(0)


		print ('---')
		print(count)
		print (features)

		with open(finalName, 'wb') as myfile:
			wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
			wr.writerow(features)

	print ("the end tieme is %s" % time.time())

