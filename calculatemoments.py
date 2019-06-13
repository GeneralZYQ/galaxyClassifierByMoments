#This is used to calculate the moments of each jpeg
import pandas as pd
import Image


#Firstly read coordinates 
csv_file = 'moments.csv'
names = ['name', 'hu1', 'hu2', 'hu3', 'hu4', 'hu5', 'hu6', 'hu7'];
df = pd.read_csv(csv_file)

folderNames = ['a', 'b']

#Secondly find the image to calculate
for x in xrange(0,df.shape[0]):
	print(df.iloc[x][3])

	for foldername in folderNames:
		fileNames = os.listdir(foldername)
		for filename in fileNames:
			if '.jpeg' not in filename:
				continue
			preffix = filename.split('.')[0]
			if int(preffix) == int(df.iloc[x][3]):
				#calculate use the crop method https://www.cnblogs.com/way_testlife/archive/2011/04/17/2019013.html

#Thirdly add the result to the dataframe

