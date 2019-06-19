#this is the python file to detect all the objects and calculate the moments.
import os
import time
from TestTree import *
import csv

prePath = '/Volumes/DISK1/galaxyClassifierByMoments'

files= os.listdir(prePath)

for filename in files:
	if '.csv' not in filename:
		continue

	print (filename)

	fullPath = prePath + '/' + filename
	#use the algorithm to detect the central object. 
	rootNode = None
	existNodes = []
	with open(fullPath, mode='r') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			
			if (int(row['x_end']) - int(row['x_start'])) > 1022 or (int(row['y_end']) - int(row['y_start'])) > 1022:
				continue
			area = int(row['area'])
			greyLevel = float(row['greylevel'])


			newNode = TestNode(int(row['x_start']), int(row['x_end']), int(row['y_start']), int(row['y_end']))
			newNode.area = area
			newNode.graylevel = greyLevel
			existNodes.append(newNode)



			if (rootNode is None) or (newNode.area > rootNode.area):#and abs(((int(row['x_end']) - int(row['x_start'])) / 2.0) - 512) < 200 and abs(((int(row['y_end']) - int(row['y_start'])) / 2.0) - 512.0) < 200:

				if rootNode is None:
					rootNode = newNode
				else:
					rootNode = newNode

				# print (abs(((int(row['y_end']) - int(row['y_start'])) / 2.0)))
				# print (abs(((int(row['x_end']) - int(row['x_start'])) / 2.0)))
				# print (area)
				# print ("----")

	# if rootNode is not None:
	# 	print ("The startx endx starty and endy are %d, %d, %d , %d" % (rootNode.xstart, rootNode.ystart, rootNode.xend, rootNode.yend))
	
	# #Construct the tree.
	if rootNode is None:
		print ("no fittable root node")
		break
	testingTree = TestTree(name='filename', root=rootNode)
	print (len(existNodes))
	for node in existNodes:

		if node.isSameNode(rootNode):
			continue

		testingTree.insertNode(node)

   
	print (testingTree.root.yend)
	print (testingTree.root.children[0].yend)
	break
	# #calculate the moment to generate a bar.
	# getBar = testingTree.calculateBar()
	# # print (getBar)
	# csv_columns = ['delta','ratio']
	# csv_file = filename.split('.')[0] + '_bar.csv'
	# with open(csv_file, 'a') as csvfile:
	# 	writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
	# 	writer.writeheader()
	# 	for data in getBar:
	# 		writer.writerow(data)
	#save the bar to a individual file