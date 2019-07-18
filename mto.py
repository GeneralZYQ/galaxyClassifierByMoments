import mtolib.main as mto
import numpy as np
import numpy.ctypeslib as npct
import ctypes as ct
from PIL import Image
import pandas as pd 

"""Example program - using original settings"""

# Get the input image and parameters
image, params = mto.setup()


# Pre-process the image
processed_image = mto.preprocess_image(image, params, n=2)

# # Build a max tree
mt = mto.build_max_tree(processed_image, params)

nodes = npct.as_array(ct.cast(mt.nodes, ct.POINTER(ct.c_int32)), (image.size, 2))
print ("in main")
# print (nodes)

# # Filter the tree and find objects
id_map, sig_ancs = mto.filter_tree(mt, processed_image, params)
print ("filtered")

# # # # Relabel objects for clearer visualisation
id_map = mto.relabel_segments(id_map, shuffle_labels=False) 
print ("relabbled")

# # # Generate output files
mto.generate_image(image, id_map, params)
mto.generate_parameters(image, id_map, sig_ancs, params)
print ("parameters generated")

df = pd.read_csv(params.par_out)
print (list(df.columns.values))

assumeXstart = 0
assumeXend = 0
assumeYstart = 0
assumeYend = 0
assumeArea = 0

detected = False

for index, row in df.iterrows():
	# print (row['x_start'] - row['x_end'])
	width = row['x_end'] - row['x_start']
	height = row['y_end'] - row['y_start']
	if (width > 200) and (height > 200) and width != 1023 and height != 1023:
		print ("treat as galaxy")
		if detected:
			currentCenterX = (assumeXstart + assumeXend) / 2.0
			currentCenterY = (assumeYstart + assumeYend) / 2.0
			newCenterX = (row['x_end'] + row['x_start']) / 2.0
			newCenterY = (row['y_end'] + row['y_start']) / 2.0
			if (pow(currentCenterX , 2) + pow(currentCenterY, 2)) > (pow(newCenterX, 2) + pow(newCenterY ,2)) :
				assumeXstart = row['x_start']
				assumeXend = row['x_end']
				assumeYstart = row['y_start']
				assumeYend = row['y_end']
				assumeArea = row['area']
		else:
			assumeXstart = row['x_start']
			assumeXend = row['x_end']
			assumeYstart = row['y_start']
			assumeYend = row['y_end']
			assumeArea = row['area']
			detected = True
	if index > 300:
		break

print ("the startX is %d, startY is %d, endX is %d, endY is %d , the area is %d, the detected is %d" % (assumeXstart, assumeYstart, assumeXend, assumeYend, assumeArea, detected))


iIndex = 0
for node in nodes:
	if node[1] == assumeArea:
		print (iIndex)
		print (node)
		break
	iIndex = iIndex + 1

print ("the iIndex is %d" % iIndex)
count = 0
currentIndex = 0
for node in nodes:
	if node[0] == iIndex:
		count = count + 1
		rown = int(currentIndex / 1024)
		coln = int(currentIndex % 1024)
		print ("The density is %d" % processed_image[rown, coln])
	currentIndex = currentIndex + 1

print ("The first children number is %d" % count)
# delta = processed_image[]
# in here we calculate the object we would like , then we can use the nodes to calculate the local spectrum


# # get image and parames from here
# mto.generate_moments_based_on_image(params)