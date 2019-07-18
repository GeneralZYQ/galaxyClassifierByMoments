"""Build a maxtree from a numpy array."""

import ctypes as ct
import numpy.ctypeslib as npct
import numpy as np

from mtolib import _ctype_classes as mt_class
import matplotlib.pyplot as plt


class MaxTree:
    """A container class for the C maxtree"""
    def __init__(self, image, verbosity):
        self.image = image
        self.verbosity = verbosity

        self.nodes = None
        self.node_attributes = None
        self.root = None

        self.mt = None

    def flood(self):
        raise NotImplementedError

    def free_objects(self):
        raise NotImplementedError

    def ctypes_maxtree(self, params):
        # Create image object
        img_pointer = self.image.ravel().ctypes.data_as(ct.POINTER(params.d_type))

        return mt_class.MtData(root=self.root,
                               nodes=self.nodes,
                               node_attributes=self.node_attributes,
                               img=mt_class.Image(img_pointer, *self.image.shape, self.image.size),
                               verbosity_level = self.verbosity)


class OriginalMaxTree(MaxTree):
    def __init__(self, image, verbosity, params):
        # Sets up CTypes to interact with C code; Sets up maxtree

        MaxTree.__init__(self, image, verbosity)

        # Get access to the compiled C maxtree library
        if params.d_type == ct.c_double:
            self.mt_lib = ct.CDLL('mtolib/lib/maxtree_double.so')
        else:
            self.mt_lib = ct.CDLL('mtolib/lib/maxtree.so')


        # Create image object
        img_pointer = image.ravel().ctypes.data_as(ct.POINTER(params.d_type))

        c_img = mt_class.Image(img_pointer, image.shape[0], image.shape[1], image.size)
        # print (image.ravel())

        # Create empty mt object
        self.mt = mt_class.MtData()

        # Set argument types for init function; Initialise max tree.
        self.mt_lib.mt_init.argtypes = (ct.POINTER(mt_class.MtData), ct.POINTER(mt_class.Image))

        self.mt_lib.mt_init(ct.byref(self.mt), ct.byref(c_img))

        # Set verbosity
        self.mt_lib.mt_set_verbosity_level.argtypes = (ct.POINTER(mt_class.MtData),
                                                  ct.c_int)
        self.mt_lib.mt_set_verbosity_level(ct.byref(self.mt), verbosity)

    def flood(self):
        # Call the C function to flood the maxtree

        # C flood function takes a pointer to an MtData (mt_data in C) object
        self.mt_lib.mt_flood.argtypes = [ct.POINTER(mt_class.MtData)]
        self.mt_lib.mt_flood(ct.byref(self.mt))

        # Get a 2D numpy array of the MtNode data
        nodes = npct.as_array(ct.cast(self.mt.nodes, ct.POINTER(ct.c_int32)), (self.mt.img.size, 2))
        
        # node_attributes = npct.as_array(ct.cast(self.mt.node_attributes, ct.POINTER(ct.c_double)),
        #                                (self.mt.img.size, 2))

        # print (nodes)

        ####
        ##The following piece of code can be used as the method to make local spectrum

        # assumeObjectStartIndex = 7
        # assumeObjectArea = 13
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

        #     if parent == assumeObjectStartIndex: #directly
        #         contains = True
        #         parentNode = nodes[parent] #parentNode is the father of current node
        #     else:

        #         while True:
        #             parentNode = nodes[parentNodeParent]
        #             parentNodeParent = parentNode[0]
        #             if parentNodeParent == assumeObjectStartIndex:
        #                 contains = True
        #                 break
        #             if parentNodeParent == -3:
        #                 break

        #     if contains: #the node belongs to the galaxy
        #         if area > 1: #this is a node but not a pixel
        #             ratio = float(area / assumeObjectArea)
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

        # ratios.append(1.0)
        # deltas.append(0.0)


        ### The code piece ends here.
        
        # ratios = [0.16, 0.33, 1.0]
        # deltas = [2, 1, 0]
        # plt.figure(figsize=(8,4))
        # plt.plot(ratios,deltas,"r--",linewidth=1)
        # plt.xlabel("ratio") 
        # plt.ylabel("delta")
        # plt.title("Local Spectrum")
        # plt.show()

                    







        self.root = self.mt.root
        self.nodes = self.mt.nodes
        self.node_attributes = self.mt.node_attributes

    def free_objects(self):
        # Free the memory used by the max tree
        self.mt_lib.mt_free.argtypes = [ct.POINTER(mt_class.MtData)]
        self.mt_lib.mt_free(ct.byref(self.mt))

    def ctypes_maxtree(self):
        return self.mt
