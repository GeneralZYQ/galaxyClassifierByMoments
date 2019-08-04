#batch processing and detecting objects
import os
import time

foldernames = ['combinesFITS', 'DKsFITS', 'edgesFITS', 'mergesFITS', 'ellipticsFITS','cwSpiralsFITS','acwSpiralFITS']

cou = 1 # Just for counting how many files has been processed # elliptics 55
startedInfolder = 'acwSpiralFITS'
shouldCheckFolder = True
countIndex = 0
shouldCheckIndex = True
startIndex = 550

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

	path = "/Volumes/DISK1/MTObjects/%s" % foldername 
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

		pngname = rawfilename + '.' + 'png'

		command = "python mto.py %s -verbosity 0 -out %s -par_out %s" % (fullPath, pngname, csvname)
		os.system(command)

		#os.system('python mto.py gray1f.fits -verbosity 2 -out out1.png -par_out pout1.csv')

		cou = cou + 1
		if cou % 50 == 0:
			print ("==================The number is %d in time %s ===========================" % (cou, time.time()))
		if cou > 100:
			break

