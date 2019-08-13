#batch processing and detecting objects
import os
import time
import pandas as pd

foldernames = ['combinesFITS', 'DKsFITS', 'edgesFITS', 'mergesFITS', 'ellipticsFITS','cwSpiralsFITS','acwSpiralFITS']

cou = 1 # Just for counting how many files has been processed # elliptics 55
startedInfolder = 'cwSpiralsFITS'
shouldCheckFolder = True
countIndex = 0
shouldCheckIndex = False
startIndex = 550

namesDF = pd.read_csv("selfLabelledGalaxies.csv")
namesSet = set(namesDF['name'])


for foldername in foldernames:

	print (foldername)
	cou = 1
	if shouldCheckFolder and foldername != startedInfolder:
		print (foldername)
		continue

	if shouldCheckFolder and foldername == startedInfolder:
		shouldCheckFolder = False
		print ("Starting at Folder %s" % startedInfolder)
	

	#/Volumes/DISK1/MTObjects/mergesFITS 

	path = "/Volumes/DISK2/galaxyZooDataSource/%s" % foldername 
	files= os.listdir(path)

	for filename in files:

		if '.fits' not in filename:
			continue

		if shouldCheckIndex and countIndex < startIndex:
			countIndex = countIndex + 1
			# print (countIndex)
			continue
		else:
			if shouldCheckIndex and countIndex >= startIndex:
				shouldCheckIndex = False
				print ('start here! %d' % countIndex)


		fullPath = path + '/' + filename

		rawfilename = filename.split('.')[0]
		csvname = rawfilename + '.' + 'csv'
		print (csvname)

		filenameNum = int(rawfilename)
		if filenameNum not in namesSet:
			continue

		pngname = rawfilename + '.' + 'png'

		command = "python mto.py %s -verbosity 0 -out %s -par_out %s" % (fullPath, pngname, csvname)
		os.system(command)

		#os.system('python mto.py gray1f.fits -verbosity 2 -out out1.png -par_out pout1.csv')

		cou = cou + 1
		if cou % 50 == 0:
			print ("==================The number is %d in time %s ===========================" % (cou, time.time()))
		if cou > 120:
			print ("upper")
			break

