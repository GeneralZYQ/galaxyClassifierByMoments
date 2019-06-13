#batch processing and detecting objects
import os

foldernames = ['acwSpiralFITS', 'combinesFITS', 'cwSpiralsFITS', 'DKsFITS', 'edgesFITS', 'ellipticsFITS', 'mergesFITS']

for foldername in foldernames:

	#/Volumes/DISK1/MTObjects/mergesFITS 

	path = "/Volumes/DISK1/MTObjects/%s" % foldername 
	files= os.listdir(path)

	for filename in files:

		if 'fits' not in filename:
			continue

		fullPath = path + '/' + filename

		rawfilename = filename.split('.')[0]
		csvname = rawfilename + '.' + 'csv'
		print (csvname)

		#os.system('python mto.py gray1f.fits -verbosity 2 -out out1.png -par_out pout1.csv')
