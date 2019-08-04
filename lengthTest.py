#this is used to test length
from numpy import genfromtxt
my_data = genfromtxt('587727223561781463_range.csv', delimiter=',')
my_data1 = genfromtxt('587727223561781463_nodes.csv', delimiter=',')

print (type(my_data1[0][0]))

coutn = 0
for x in my_data:
	ind = int(x)
	if my_data1[ind][1] != 1:
		coutn = coutn + 1

print (coutn)