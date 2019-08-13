import mtolib.main as mto
import numpy as np
import numpy.ctypeslib as npct
import ctypes as ct
from PIL import Image
import pandas as pd 
import csv

"""Example program - using original settings"""

# Get the input image and parameters
image, params = mto.setup()


# Pre-process the image
processed_image = mto.preprocess_image(image, params, n=2)


# # Build a max tree
mt = mto.build_max_tree(processed_image, params)
nodes = npct.as_array(ct.cast(mt.nodes, ct.POINTER(ct.c_int32)), (image.size, 2))
print ("in main")

np.set_printoptions(suppress=True)
np.set_printoptions(precision=3)


# Filter the tree and find objects
id_map, sig_ancs = mto.filter_tree(mt, processed_image, params)
print ("filtered")

# # # # Relabel objects for clearer visualisation
id_map = mto.relabel_segments(id_map, shuffle_labels=False) 
print ("relabbled")

# # # Generate output files
# mto.generate_image(image, id_map, params)
# mto.generate_parameters(image, id_map, sig_ancs, params)
object_ids = id_map.ravel()
sorted_ids = object_ids.argsort()
id_set = list(set(object_ids))
# print ("the length is %d" % len(id_set))
right_indices = np.searchsorted(object_ids, id_set, side='right', sorter=sorted_ids)
left_indices = np.searchsorted(object_ids, id_set, side='left', sorter=sorted_ids)


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


				
	# p.append(np.amin(pixel_indices[1])) #start x
    # p.append(np.amax(pixel_indices[1])) #end x
    # p.append(np.amin(pixel_indices[0])) #start y
    # p.append(np.amax(pixel_indices[0])) #end y
print ("the start x is %d" % assumeXstart)
print ("hte xs length is %d" % len(assumeXs))
print ("the ys lenght is %d " % len(assumeYs))
print ("parameters generated")

if len(assumeYs) > 0:

	preffix = params.par_out.split(".")[0]
	nodename = preffix + '_nodes.csv'
	np.savetxt(nodename, nodes, delimiter=",", fmt='%.03f') # all the nodes


	imageName = preffix + '_processedImage.csv'
	np.savetxt(imageName, processed_image, delimiter=",", fmt="%.03f") # all the processed image nodes 

	objectName = preffix + "_range.csv"
	ranges = []
	for x in range(0,len(assumeYs)):
		num = assumeXs[x] + 1024 * assumeYs[x]
		ranges.append(num)
	print ("the range lenght is %d " % len(ranges))

	with open(objectName, 'w') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerow(ranges)
	csvFile.close()



# df = pd.read_csv(params.par_out)



# detected = False

# for index, row in df.iterrows():
# 	# print (row['x_start'] - row['x_end'])
# 	width = row['x_end'] - row['x_start']
# 	height = row['y_end'] - row['y_start']
# 	if (width > 200) and (height > 200) and width != 1023 and height != 1023:
# 		print ("treat as galaxy")
# 		if detected:
# 			currentCenterX = (assumeXstart + assumeXend) / 2.0
# 			currentCenterY = (assumeYstart + assumeYend) / 2.0
# 			newCenterX = (row['x_end'] + row['x_start']) / 2.0
# 			newCenterY = (row['y_end'] + row['y_start']) / 2.0
# 			if (pow(currentCenterX , 2) + pow(currentCenterY, 2)) > (pow(newCenterX, 2) + pow(newCenterY ,2)) :
# 				assumeXstart = row['x_start']
# 				assumeXend = row['x_end']
# 				assumeYstart = row['y_start']
# 				assumeYend = row['y_end']
# 				assumeArea = row['area']
# 		else:
# 			assumeXstart = row['x_start']
# 			assumeXend = row['x_end']
# 			assumeYstart = row['y_start']
# 			assumeYend = row['y_end']
# 			assumeArea = row['area']
# 			detected = True
# 	if index > 300:
# 		break

# print ("the startX is %d, startY is %d, endX is %d, endY is %d , the area is %d, the detected is %d" % (assumeXstart, assumeYstart, assumeXend, assumeYend, assumeArea, detected))


# iIndex = 1024 * assumeYstart + assumeXstart


# print ("the iIndex is %d" % iIndex)
# #The assume index is 'iIndex'
# #The assume area is 'assumeArea'

# if iIndex > 0 and iIndex < (1024 * 1024):
# 	if assumeArea > 0:
		
		# preffix = params.par_out.split(".")[0]
		# imageName = preffix + '_processedImage.csv'
		# np.savetxt(imageName, processed_image, delimiter=",", fmt="%.03f")


# 		nodes = np.insert(nodes, 0, [iIndex, assumeArea])
# 		nodes = nodes.reshape(1024*1024+1, 2)
# 		print (nodes[0])
# 		nodename = preffix + '_nodes.csv'
# 		np.savetxt(nodename, nodes, delimiter=",", fmt='%.03f')
# 	else:
# 		print ("skip!");




# ratios = []
# deltas = []
# i = 0

# for node in nodes:
#     #node is the current node
#     parent = node[0]
#     area = node[1]

#     contains = False
#     parentNodeParent = parent
#     parentNode = []

#     if parent == iIndex: #directly
#         contains = True
#         parentNode = nodes[parent] #parentNode is the father of current node
#     else:

#         while True:
#             parentNode = nodes[parentNodeParent]
#             parentNodeParent = parentNode[0]
#             if parentNodeParent == iIndex:
#                 contains = True
#                 break
#             if parentNodeParent == -3:
#                 break

#     if contains: #the node belongs to the galaxy
#         if area > 1: #this is a node but not a pixel
#             ratio = float(area / assumeArea)
#             print ('---------')
#             print (ratio)
#             currentIndex = i
#             parentIndex = parent

#             rown = int(currentIndex / 6)
#             coln = int(currentIndex % 6)

#             rowp = int(parentIndex / 6)
#             colp = int(parentIndex % 6)

#             delta = self.image[rown,coln] - self.image[rowp,colp]
#             print (delta)
#             ratios.append(ratio)
#             deltas.append(delta)


#     i = i + 1

# # get image and parames from here
# mto.generate_moments_based_on_image(params)