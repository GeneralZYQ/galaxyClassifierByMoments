import mtolib.main as mto
import numpy as np
import numpy.ctypeslib as npct
import ctypes as ct
from PIL import Image
import pandas as pd 
import csv
from PIL import Image

"""Example program - using original settings"""

# Get the input image and parameters
image, params = mto.setup()
# print (image)

# Pre-process the image
processed_image = mto.preprocess_image(image, params, n=2)
# print (processed_image)


# # # Build a max tree
mt = mto.build_max_tree(processed_image, params)

# nodes = npct.as_array(ct.cast(mt.nodes, ct.POINTER(ct.c_int32)), (image.size, 2))#
# # print (nodes)

# np.set_printoptions(suppress=True)
# np.set_printoptions(precision=3)


# # Filter the tree and find objects
id_map, sig_ancs = mto.filter_tree(mt, processed_image, params)
# print ("filtered")

# # # # # # Relabel objects for clearer visualisation
id_map = mto.relabel_segments(id_map, shuffle_labels=False) 
# print ("relabbled")
# print (id_map.shape)

# # # # # Generate output files
# mto.generate_image(image, id_map, params)
# mto.generate_parameters(image, id_map, sig_ancs, params)

object_ids = id_map.ravel()
sorted_ids = object_ids.argsort()
id_set = list(set(object_ids))
# # print ("the length is %d" % len(id_set))
right_indices = np.searchsorted(object_ids, id_set, side='right', sorter=sorted_ids)
left_indices = np.searchsorted(object_ids, id_set, side='left', sorter=sorted_ids)

# for n in range(len(id_set)):
# 	pixel_indices = np.unravel_index(sorted_ids[left_indices[n]:right_indices[n]], processed_image.shape)
# 	# print (pixel_indices)
# 	crooImage = np.ones(processed_image.shape)
# 	allXes = pixel_indices[1]
# 	allYes = pixel_indices[0]
	# # print (len(allXes))

	# print ("the min x is %d" % min(pixel_indices[1]))
	# print ("the max x is %d" % max(pixel_indices[1]))

	# print ("the min y is %d" % min(pixel_indices[0]))
	# print ("the max y is %d" % max(pixel_indices[0]))

	# for x in range(len(allXes)):
	# 	crooImage[allYes[x]][allXes[x]] = 30

	# print (crooImage)
		
	
	# if n == 6:
	# 	imagename = "im" + ("%d" % n) + '.png'
	# 	mto.generate_image(image, crooImage, params)
		

	# filename = "file" + ("%d" % n) + '.csv'

	# np.savetxt(filename, crooImage, delimiter=",")

	# print (n)


assumeXstart = 0
assumeXend = 0
assumeYstart = 0
assumeYend = 0
assumeArea = 0
assumeYs = []
assumeXs = []

for n in range(len(id_set)):
	pixel_indices = np.unravel_index(sorted_ids[left_indices[n]:right_indices[n]], processed_image.shape)

	width = np.amax(pixel_indices[1]) - np.amin(pixel_indices[1])
	height = np.amax(pixel_indices[0]) - np.amin(pixel_indices[0])
	
	if (width >= 180) and (height >= 180) and (width != 1023) and (height != 1023):
		currentCenterX = (assumeXstart + assumeXend) / 2.0
		currentCenterY = (assumeYstart + assumeYend) / 2.0

		newCenterX = (np.amax(pixel_indices[1]) + np.amin(pixel_indices[1])) / 2.0
		newCenterY = (np.amax(pixel_indices[0]) + np.amin(pixel_indices[0])) / 2.0
		print ("the widthh is %d and height is %d" % (width, height))

		if (pow(abs (currentCenterX - 512) , 2) + pow(abs(currentCenterY - 512) , 2)) > (pow(abs (newCenterX - 512), 2) + pow(abs(newCenterY - 512) ,2)) :
			assumeXstart = np.amin(pixel_indices[1])
			assumeXend = np.amax(pixel_indices[1])
			assumeYstart = np.amin(pixel_indices[0])
			assumeYend = np.amax(pixel_indices[0])
			assumeArea = len(pixel_indices[0])
			assumeYs = pixel_indices[0]
			assumeXs = pixel_indices[1]
			print ("The n is %d" % n)


				
# print ("the start x is %d" % assumeXstart)
# print ("hte xs length is %d" % len(assumeXs))
# print ("the ys lenght is %d " % len(assumeYs))
# print ("parameters generated")

# if len(assumeYs) > 0:

# 	preffix = params.par_out.split(".")[0]
# 	nodename = preffix + '_nodes.csv'
# 	np.savetxt(nodename, nodes, delimiter=",", fmt='%.03f') # all the nodes


# 	imageName = preffix + '_processedImage.csv'
# 	np.savetxt(imageName, processed_image, delimiter=",", fmt="%.03f") # all the processed image nodes 

# 	objectName = preffix + "_range.csv"
# 	ranges = []
# 	for x in range(0,len(assumeYs)):
# 		num = assumeXs[x] + 1024 * assumeYs[x]
# 		ranges.append(num)
# 	print ("the range lenght is %d " % len(ranges))

# 	with open(objectName, 'w') as csvFile:
# 		writer = csv.writer(csvFile)
# 		writer.writerow(ranges)
# 	csvFile.close()



