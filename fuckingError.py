#this is a file used to avoid the fucking errors!

import csv
import os
import numpy as np
from numpy import genfromtxt

path = "/Volumes/DISK1/croissant_elliptics"
files= os.listdir(path)

for file in files:
	if "_image.csv" in file:
		shapeFullPath = path + '/' + file
		shapeData = genfromtxt(shapeFullPath, delimiter=',')
		print (shapeFullPath)
		truecroissantImage = []
		with open(shapeFullPath, 'r') as myfile:
			reader = csv.reader(myfile)
			for row in reader:
				# print (type(row[0]))
				for x in range(0,len(row)):
					truecroissantImage.append(float(row[x]))
			np.savetxt(file, truecroissantImage, delimiter=",", fmt='%.03f')

		

		