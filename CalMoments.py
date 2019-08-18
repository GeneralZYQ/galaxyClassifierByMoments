#this is the file I am trying to calculate the M1 of Hu.

def MPQ(pixels, p, q, img, imageWidth, imageHeight):
	Mqp = 0.0

	for value in pixels:
		xc = value % imageWidth
		yc = value / imageWidth

		mid = pow(xc, p) * pow(yc, q) * img[value]
		Mqp = Mqp + mid

	return Mqp

def MiuPQ(pixels, p, q, img, imageWidth, imageHeight):
	
	M10 = MPQ(pixels, 1, 0, img)
	M01 = MPQ(pixels, 0, 1, img)
	M00 = MPQ(pixels, 0, 0, img)

	Xcentral = M10 / M00
	Ycentral = M01 / M00

	miupq = 0.0

	for value in pixels:
		xc = value % imageWidth
		yc = value / imageWidth

		miupq = miupq +  pow(xc - Xcentral, p) * pow(yc - Ycentral, q) * img[value]

	return miupq

def ItaIJ(pixels, i, j, img, imageWidth, imageHeight):
	miuij = MiuPQ(pixels, i, j, img, imageWidth)
	miu00 = MiuPQ(pixels, 0,0, img, imageHeight)

	itaij = miuij / pow(miu00, (1 + (i + j) / 2))
	return itaij

def calculateM1(pixels, img):
	return ItaIJ(pixels, 0, 2, img, imageWidth, imageHeight) + ItaIJ(pixels, 2, 0, img, imageWidth, imageHeight)

def calculateM2(pixels, img):
	return pow(ItaIJ(pixels, 2, 0, img, imageWidth, imageHeight) - ItaIJ(pixels, 0, 2, img, imageWidth, imageHeight), 2) + 4 * pow(ItaIJ(pixels, 1, 1, img, imageWidth, imageHeight), 2)

def calculateM3(pixels, img):
	return pow(ItaIJ(pixels, 3, 0, img, imageWidth, imageHeight) - 3 * ItaIJ(pixels, 1, 2, img, imageWidth, imageHeight), 2) + pow(3 * ItaIJ(pixels, 2, 1, img, imageWidth, imageHeight) - ItaIJ(pixels, 0, 3, img, imageWidth, imageHeight), 2)

def calculateM4(pixels, img):
	return pow(ItaIJ(pixels, 3, 0, img, imageWidth, imageHeight) + ItaIJ(pixels, 1, 2, img, imageWidth, imageHeight), 2) + pow(3 * ItaIJ(pixels, 2, 1, img, imageWidth, imageHeight) + ItaIJ(pixels, 0, 3, img, imageWidth, imageHeight), 2) 

def calculateM5(pixels, img):
	# return (ItaIJ(pixels, 3, 0, img, imageWidth, imageHeight) - 3 * ItaIJ(pixels, 1, 2, img, imageWidth, imageHeight)) * (ItaIJ(pixels, 3, 0, img, imageWidth, imageHeight) + ItaIJ(pixels, 1, 2, img, imageWidth, imageHeight)) * (pow((ItaIJ(pixels, 3, 0, img, imageWidth, imageHeight) + ItaIJ(pixels, 1, 2, img, imageWidth, imageHeight)), 2) - 3 * pow(ItaIJ((pixels, 2, 1, img, imageWidth, imageHeight), 2))) + (3 * ItaIJ(pixels, 2, 1, img, imageWidth, imageHeight) - ItaIJ(pixels, 0, 3, img, imageWidth, imageHeight)) * (ItaIJ(pixels, 2, 1, img, imageWidth, imageHeight) + ItaIJ(pixels, 0, 3, img, imageWidth, imageHeight)) * (3 * pow(ItaIJ(pixels, 3, 0 ,img, imageWidth, imageHeight) + ItaIJ(pixels, 1,2, img, imageWidth, imageHeight), 2)) - pow((ItaIJ(pixels, 2, 1, img, imageWidth, imageHeight) + ItaIJ(pixels, 0, 3, img, imageWidth, imageHeight)), 2))
	return 0.0;

def calculateM6(pixels, img):
	firstpart = ItaIJ(pixels, 2, 0, img, imageWidth, imageHeight) - ItaIJ(pixels, 0, 2, img, imageWidth, imageHeight)
	secondpart = pow(ItaIJ(pixels, 3, 0, img, imageWidth, imageHeight) + ItaIJ(pixels, 1, 2, img, imageWidth, imageHeight), 2)
	thirdpart = pow(ItaIJ(pixels, 2, 1, img, imageWidth, imageHeight) + ItaIJ(pixels, 0, 3, img, imageWidth, imageHeight), 2)

	fourthpart = ItaIJ(pixels, 1,1, img, imageWidth, imageHeight)
	fifthpart = ItaIJ(pixels, 3, 0, img, imageWidth, imageHeight) + ItaIJ(pixels, 1, 2, img, imageWidth, imageHeight) 
	sexthpart = ItaIJ(pixels, 2, 1, img, imageWidth, imageHeight) + ItaIJ(pixels, 0, 3, img, imageWidth, imageHeight) 

	return firstpart * (secondpart - thirdpart) + 4 * fourthpart * fifthpart * sexthpart

def calculateM7(pixels, img):
	firstparth = 3 * ItaIJ(pixels, 2, 1, img, imageWidth, imageHeight) - ItaIJ(pixels, 0, 3, img, imageWidth, imageHeight) 
	secondpart = ItaIJ(pixels, 1, 2, img, imageWidth, imageHeight) + ItaIJ(pixels, 3, 0, img, imageWidth, imageHeight)
	thirdpart = pow(secondpart, 2)
	fourthpart = 3 * pow(ItaIJ(pixels, 2, 1, img, imageWidth, imageHeight) + ItaIJ(pixels, 0, 3, img, imageWidth, imageHeight) , 2)

	fifthpart = ItaIJ(pixels, 3, 0, img, imageWidth, imageHeight) - 3 * ItaIJ(pixels, 1, 2, img, imageWidth, imageHeight)
	sexthpart = ItaIJ(pixels, 2, 1, img, imageWidth, imageHeight) + ItaIJ(pixels, 0, 3, img, imageWidth, imageHeight)
	senventhpart = 3 * pow(secondpart, 2)
	eighthpart = pow(sexthpart, 2)

	return firstparth * secondpart * (thirdpart - fourthpart) - fifthpart * sexthpart * (senventhpart - eighthpart)





