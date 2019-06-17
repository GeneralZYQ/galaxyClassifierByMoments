#This is a class used to test
#With these two classes, you can build the max tree by using the objects detected by mto.py
class TestTree:
	"""docstring for ClassName"""
	def __init__(self, name, root):
		self.name = name
		self.root = root

	def insertNode(self,node):
		inserted = False

		if self.root.containsNode(node): 
			#There are three types 
			#1. father contains the new node but the new node contains none of the children of the father.
			#Then the new node act as a new child of the fater.
			#2. The father contains the new node and the new node contains one of the children .
			#Then insert the new node between father and the child.
			#3. To the final child contains the new node .
			# Then the new node is a child of the final child

			inserted = True

			queue = []
			queue.append(self.root)#
			canBreak = False
			i = 0
			NewNodeNotBelongToAnyOne = True
			while len(queue):
				i = i+ 1
				print (i)

				father = queue.pop(0)
				NewcontiansOne = False
				
				beContainedChild = None

				for x in range(0,len(father.children)):
					queue.append(father.children[x])

				for x in range(0,len(father.children)):
					if node.containsNode(father.children[x]):
						print ('new node contain old ones')
						NewcontiansOne = True
						beContainedChild = father.children[x]

					if father.children[x].containsNode(node):
						if i == 1:
							print ("The child xstart %d, xend %d, ystart %d, yend %d" % (father.children[x].xstart, father.children[x].xend, father.children[x].ystart, father.children[x].yend))
							print ("The node xstart %d, xend %d, ystart %d, yend %d" % (node.xstart, node.xend, node.ystart, node.yend))
						NewNodeNotBelongToAnyOne = False


					if len(father.children[x].children) <= 0 and father.children[x].containsNode(node):#case 3
						father.children[x].children.append(node)
						canBreak = True
						print ("case3")
						break

				if NewNodeNotBelongToAnyOne and not NewcontiansOne: # case 1
					father.children.append(node)
					print ("case1")
					break
				elif NewcontiansOne and beContainedChild:#case 2
					father.children.remove(beContainedChild)
					father.children.append(node)
					node.children.append(beContainedChild)
					print ("case2")
					break

				if canBreak:
					break




		if not inserted:
			print ("not belongs to this tree")

		return inserted


	def breadth_travel(self): 
		if self.root == None:
			return

		print (self.name)
		queue = []
		queue.append(self.root)
		while len(queue):
			node = queue.pop(0)
			print ("and %s" % (node.name))
			for x in range(0,len(node.children)):
				queue.append(node.children[x])



class TestNode:
	"""docstring for Node"""
	def __init__(self, xstart, xend, ystart,yend):
		
		self.xstart = xstart
		self.xend = xend
		self.ystart = ystart
		self.yend = yend
		self.father = None
		self.children = []
		self.name = ''

	def containsNode(self,node):
		if self.xstart <= node.xstart and self.xend >= node.xend and self.ystart <= node.ystart and self.yend >= node.yend:
			return True
		else:
			return False
			

		
