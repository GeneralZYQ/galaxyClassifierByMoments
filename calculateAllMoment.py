#this is a file used to calculate the moments in a object.
#I will save all the moments in a dict, {[NodeIndex : moment]}

import csv
import numpy as np
import pandas as pd
from numpy import genfromtxt
import os 
from CalMoments import MPQ, MiuPQ, ItaIJ, calculateM1
import math
import time


from mtolib.io_mto import make_parser
import mtolib.main as mto
from ctypes import c_float, c_double
from mtolib import _ctype_classes as ct
import numpy.ctypeslib as npct
import ctypes as ctp

import collections

from PIL import Image

params = make_parser().parse_args()
params.d_type = c_double
ct.init_classes(params.d_type)


count = 0 


path = "/Volumes/DISK1/processed/SpiralsCSV"
files= os.listdir(path)

for fileName in files:

	calculatedMoment1s = {}
	if '_nodes.csv' in fileName:
		nodesFullPath = path + '/' + fileName
		firstPar = fileName.split('_')[0]
		rangefullPath = path + '/' + firstPar + '_range.csv'
		processedImagefullPath = path + '/' + firstPar + '_processedImage.csv'

		nodeData = genfromtxt(nodesFullPath, delimiter=',')
		rangeData = genfromtxt(rangefullPath, delimiter=',')
		processedImageData = genfromtxt(processedImagefullPath, delimiter=',')

		rangeXes = [x % 1024 for x in rangeData]
		rangeYes = [int(math.floor(x / 1024)) for x in rangeData]

		rangeYes = [int(x) for x in rangeYes]

		print ((max(rangeYes) - min(rangeYes)))
		print ((max(rangeXes) - min(rangeXes)))


		crocantImage = np.zeros(((max(rangeYes) - min(rangeYes)+1), int(1+max(rangeXes) - min(rangeXes))))
		# print (crocantImage.shape)

		minX = min(rangeXes)
		minY = int(min(rangeYes))
		for x in rangeData:
			XC = int(x % 1024)
			YC = int(math.floor(x / 1024))
			XCinNew = int(x % 1024 - minX)
			YCinNew = int(math.floor(x / 1024)) - minY

			crocantImage[YCinNew][XCinNew] = processedImageData[XC][YC]





		# crocantImage = np.ndarray((6,6), buffer=np.array([[0.0,0.0,0.0,0.0,0.0,0.0], 
  #   	                                               [0.0,1.0,1.0,1.0,1.0,0.0], 
  #   	                                               [0.0,1.0,2.0,2.0,1.0,0.0], 
  #   	                                               [0.0,4.0,4.0,1.0,1.0,0.0], 
  #   	                                               [0.0,0.0,1.0,0.0,0.0,0.0],
  #   	                                               [0.0,0.0,0.0,0.0,0.0,0.0]]), dtype=int)






		mt = mto.build_max_tree(crocantImage, params)
		# MTnodes = npct.as_array(ctp.cast(mt.nodes, ctp.POINTER(ctp.c_int32)), (crocantImage.size, 2))
		# mtMoments = npct.as_array(ctp.cast(mt.moments, ctp.POINTER(ctp.c_float)), (crocantImage.size, 9))
		# print (mt.moments)
		# MTNODEINDEXESnodes = npct.as_array(ctp.cast(mt.nodeIndexes, ctp.POINTER(ctp.c_int32)), (crocantImage.size, 2))



		# shapes = [crocantImage.shape[1], crocantImage.shape[0]]
		# ravaledCroissant = crocantImage.ravel()

		# maxtreename = firstPar+'_croissant_mtnodes.csv'
		# shapesname = firstPar + '_croissant_shape.csv'
		# reveledimageName = firstPar + '_croissant_image.csv'

		# np.savetxt(maxtreename, MTnodes, delimiter=",", fmt='%i')#all the nodes

		# np.savetxt(shapesname, shapes, delimiter=",", fmt='%i')

		# np.savetxt(reveledimageName, ravaledCroissant, delimiter=",", fmt='%.03f')

	

		# with open(reveledimageName, 'w') as myfile:
		# 	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
		# 	wr.writerow(ravaledCroissant)




		# index = 0

		# indecesDict = {}
		# M1Dict = {}

		# for mtnoden in MTnodes:

			
		# 	if (mtnoden[1] > 1) and (mtnoden[0] != -3): #this is a node or leave  

		# 		print ('my have %d ns! \n' % mtnoden[1])

		# 		Nindeces = [index]
		# 		j = 0
		# 		for mtnodej in MTnodes:

		# 			if mtnodej[0] == -3:
		# 				j = j + 1
		# 				continue
		# 			# print ("this is the index i am serachig ! %d \n" % index)


		# 			if mtnodej[0] == index:
		# 				Nindeces.append(j)
		# 			else:
		# 				parent = MTnodes[mtnodej[0]]
						
		# 				while True:
		# 					if parent[0] == -3:
		# 						break
		# 					elif parent[0] == index:
		# 						# print ("find one !")
		# 						Nindeces.append(j)
		# 						break
		# 					else:
		# 						parent = MTnodes[parent[0]]

		# 			j = j + 1

		# 		print ("find %d !\n" % len(Nindeces))
		# 		indecesDict.update({index : Nindeces})
		# 		m1 = calculateM1(Nindeces, ravaledCroissant)
		# 		print ("the index is %d and m1 is %f" % (index, m1))
		# 		M1Dict.update({index : m1})
		# 		#in here you can calculate the moments.

		# 	index = index+1


		# RatioMDict = {}

		# for keytext in M1Dict.keys():
		# 	node = MTnodes[keytext]
		# 	parent = MTnodes[node[0]]
		# 	if parent[0] == -3: #this is the root
		# 		continue
		# 	else:
				
		# 		# print ("the midict m1 now is %f" % M1Dict[keytext])
		# 		# print ("the parent m1 is %f" % M1Dict[node[0]])

		# 		delta = M1Dict[keytext] - M1Dict[node[0]]
		# 		ratio = len(indecesDict[keytext]) / len(ravaledCroissant)
		# 		RatioMDict.update({ratio:delta})


		# od = collections.OrderedDict(sorted(RatioMDict.items()))
		# print (od.keys())
		# print (od.values())

		# resultname = firstPar + '_m1.csv'
		# with open(resultname, 'w') as myfile:
		# 	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
		# 	wr.writerow(od.keys())
		# 	wr.writerow(od.values())


		count = count + 1
		if count % 50 == 0:
			print ("this is %d and %s =============" % (count, time.time()))
		if count > 0:
			break
			


				

