import numpy as np
import imageio
from PIL import Image
from PIL import ImageDraw
import scipy
from scipy import interpolate
from scipy import misc
from scipy import spatial
from scipy import ndimage
import matplotlib.pyplot as plt
import time
import os

class Affine:
	def __init__(self, source, destination):
		if not source.shape == (3,2) or not destination.shape == (3,2) or not source.dtype == 'float64' or not destination.dtype == 'float64':
			raise ValueError('Input matrix not of correct dimensions')
		self.source = source
		self.destination = destination
		self.matrix = self.createProjectionMatrix()

	def createProjectionMatrix(self):
		B = np.array([[self.destination[0][0]], [self.destination[0][1]], [self.destination[1][0]], [self.destination[1][1]], [self.destination[2][0]], [self.destination[2][1]]])
		A = np.matrix('{} {} 1 0 0 0; 0 0 0 {} {} 1; {} {} 1 0 0 0; 0 0 0 {} {} 1; {} {} 1 0 0 0; 0 0 0 {} {} 1'.format(self.source[0][0], self.source[0][1], self.source[0][0], self.source[0][1], self.source[1][0], self.source[1][1], self.source[1][0], self.source[1][1], self.source[2][0], self.source[2][1], self.source[2][0], self.source[2][1]))
		H = np.linalg.solve(A, B)
		H = np.matrix('{} {} {}; {} {} {}; 0 0 1'.format(H[0][0], H[1][0], H[2][0], H[3][0], H[4][0], H[5][0]))
		return H
	def transform(self, sourceImage, destinationImage):
		if not isinstance(sourceImage, np.ndarray) or not isinstance(destinationImage, np.ndarray):
			raise TypeError("Affine transform type error")
		inversematrix = np.linalg.inv(self.matrix)
		img = Image.new('L', (sourceImage.shape[1],sourceImage.shape[0]), 0)
		points = (tuple(self.destination[0]), tuple(self.destination[1]), tuple(self.destination[2]))
		ImageDraw.Draw(img).polygon(points, outline=255, fill = 255)
		mask = np.array(img)
		y_co, x_co = np.where(mask == 255)
		length = len(x_co)
		xyz_co = np.array([x_co[np.arange(length)],y_co[np.arange(length)],np.ones(length)])
		coordinates = np.matmul(inversematrix,xyz_co)
		pixels = scipy.ndimage.map_coordinates(sourceImage,[coordinates[1], coordinates[0]],order=1)
		destinationImage[y_co, x_co] = pixels

class Blender:
	def __init__(self, startImage, startPoints, endImage, endPoints):
		if not isinstance(startImage, np.ndarray) or not isinstance(startPoints, np.ndarray) or not isinstance(endImage, np.ndarray) or not isinstance(endPoints, np.ndarray):
			raise TypeError("Blender transform type error")
		self.startImage = startImage
		self.startPoints = startPoints
		self.endImage = endImage
		self.endPoints = endPoints
	def getBlendedImage(self, alpha):
		triangle_vertices = (1 - alpha)*self.startPoints + (alpha)*self.endPoints
		triangle_list = spatial.Delaunay(triangle_vertices)
		tpoints= triangle_vertices[triangle_list.simplices]
		spoints = self.startPoints[triangle_list.simplices]
		epoints = self.endPoints[triangle_list.simplices]

		tempImage1 = Image.new('L', (self.startImage.shape[1],self.startImage.shape[0]),0)
		tempImage1 = np.array(tempImage1)
		tempImage2 = Image.new('L', (self.startImage.shape[1],self.startImage.shape[0]),0)
		tempImage2 = np.array(tempImage2)

		for i in range(0,len(triangle_list.simplices)):
			affine1 = Affine(spoints[i], tpoints[i])
			affine2 = Affine(epoints[i], tpoints[i])
			affine1.transform(self.startImage, tempImage1)
			affine2.transform(self.endImage, tempImage2)

		finalImage = (1 - alpha)*tempImage1 + (alpha)*tempImage2

		return np.uint8(finalImage)

	def generateMorphVideo(self, targetFolderPath, sequenceLength, includeReversed):

		if not os.path.exists(targetFolderPath):
			os.makedirs(targetFolderPath)

		Image.fromarray(self.startImage).save(targetFolderPath + "/frame001.jpg", 'JPEG')
		if (includeReversed):
			Image.fromarray(self.startImage).save(targetFolderPath + "/frame" + "{}".format(2*sequenceLength).zfill(3) + ".jpg", 'JPEG')

		increment = np.float64(1/sequenceLength)
		alpha = increment
		i=0
		for i in range(1,sequenceLength):
			tempImage = self.getBlendedImage(alpha)
			misc.toimage(tempImage, cmin=0, cmax=255).save(targetFolderPath+'/frame'+'{}'.format(i+1).zfill(3)+'.jpg')
			if (includeReversed):
				misc.toimage(tempImage, cmin=0, cmax=255).save(targetFolderPath+'/frame'+'{}'.format(2*sequenceLength - i).zfill(3)+'.jpg')
			alpha += increment


		Image.fromarray(self.endImage).save(targetFolderPath + "/frame" + "{}".format(i + 1).zfill(3) + ".jpg", 'JPEG')

		os.system("ffmpeg -framerate 5 -i "+ targetFolderPath + "/frame%03d.jpg "+ targetFolderPath + "/morph.mp4")

		return

class ColorAffine:
	def __init__(self, source, destination):
		if not source.shape == (3,2) or not destination.shape == (3,2) or not source.dtype == 'float64' or not destination.dtype == 'float64':
			raise ValueError('Input matrix not of correct dimensions')
		self.source = source
		self.destination = destination
		self.matrix = self.createProjectionMatrix()

	def createProjectionMatrix(self):
		B = np.array([[self.destination[0][0]], [self.destination[0][1]], [self.destination[1][0]], [self.destination[1][1]], [self.destination[2][0]], [self.destination[2][1]]])
		A = np.matrix('{} {} 1 0 0 0; 0 0 0 {} {} 1; {} {} 1 0 0 0; 0 0 0 {} {} 1; {} {} 1 0 0 0; 0 0 0 {} {} 1'.format(self.source[0][0], self.source[0][1], self.source[0][0], self.source[0][1], self.source[1][0], self.source[1][1], self.source[1][0], self.source[1][1], self.source[2][0], self.source[2][1], self.source[2][0], self.source[2][1]))
		H = np.linalg.solve(A, B)
		H = np.matrix('{} {} {}; {} {} {}; 0 0 1'.format(H[0][0], H[1][0], H[2][0], H[3][0], H[4][0], H[5][0]))
		return H
	def transform(self, sourceImage, destinationImage):
		if not isinstance(sourceImage, np.ndarray) or not isinstance(destinationImage, np.ndarray):
			raise TypeError("Affine transform type error")
		inversematrix = np.linalg.inv(self.matrix)
		img = Image.new('L', (sourceImage.shape[1],sourceImage.shape[0]), 0)
		points = (tuple(self.destination[0]), tuple(self.destination[1]), tuple(self.destination[2]))
		ImageDraw.Draw(img).polygon(points, outline=255, fill = 255)
		mask = np.array(img)
		y_co, x_co = np.where(mask == 255)
		length = len(x_co)
		xyz_co = np.array([x_co[np.arange(length)],y_co[np.arange(length)],np.ones(length)])
		coordinates = np.matmul(inversematrix,xyz_co)
		pixels = scipy.ndimage.map_coordinates(sourceImage[:,:,0],[coordinates[1], coordinates[0]],order=1)
		destinationImage[y_co, x_co, np.zeros(length,dtype=np.uint8)] = pixels
		pixels = scipy.ndimage.map_coordinates(sourceImage[:,:,1],[coordinates[1], coordinates[0]],order=1)
		destinationImage[y_co, x_co, np.ones(length,dtype=np.uint8)] = pixels
		pixels = scipy.ndimage.map_coordinates(sourceImage[:,:,2],[coordinates[1], coordinates[0]],order=1)
		destinationImage[y_co, x_co, np.full(length, 2, dtype=np.uint8)] = pixels

class ColorBlender:
	def __init__(self, startImage, startPoints, endImage, endPoints):
		if not isinstance(startImage, np.ndarray) or not isinstance(startPoints, np.ndarray) or not isinstance(endImage, np.ndarray) or not isinstance(endPoints, np.ndarray):
			raise TypeError("Blender transform type error")
		self.startImage = startImage
		self.startPoints = startPoints
		self.endImage = endImage
		self.endPoints = endPoints
	def getBlendedImage(self, alpha):
		triangle_vertices = (1 - alpha)*self.startPoints + (alpha)*self.endPoints
		triangle_list = spatial.Delaunay(triangle_vertices)
		tpoints= triangle_vertices[triangle_list.simplices]
		spoints = self.startPoints[triangle_list.simplices]
		epoints = self.endPoints[triangle_list.simplices]

		tempImage1 = Image.new('RGB', (self.startImage.shape[1],self.startImage.shape[0]),0)
		tempImage1 = np.array(tempImage1)
		tempImage2 = Image.new('RGB', (self.startImage.shape[1],self.startImage.shape[0]),0)
		tempImage2 = np.array(tempImage2)

		for i in range(0,len(triangle_list.simplices)):
			affine1 = ColorAffine(spoints[i], tpoints[i])
			affine2 = ColorAffine(epoints[i], tpoints[i])
			affine1.transform(self.startImage, tempImage1)
			affine2.transform(self.endImage, tempImage2)

		finalImage = (1 - alpha)*tempImage1 + (alpha)*tempImage2

		return np.uint8(finalImage)

	def generateMorphVideo(self, targetFolderPath, sequenceLength, includeReversed):

		if not os.path.exists(targetFolderPath):
			os.makedirs(targetFolderPath)

		Image.fromarray(self.startImage).save(targetFolderPath + "/frame001.jpg", 'JPEG')
		if (includeReversed):
			Image.fromarray(self.startImage).save(targetFolderPath + "/frame" + "{}".format(2*sequenceLength).zfill(3) + ".jpg", 'JPEG')

		increment = np.float64(1/sequenceLength)
		alpha = increment
		i=0
		for i in range(1,sequenceLength):
			tempImage = self.getBlendedImage(alpha)
			misc.toimage(tempImage, cmin=0, cmax=255).save(targetFolderPath+'/frame'+'{}'.format(i+1).zfill(3)+'.jpg')
			if (includeReversed):
				misc.toimage(tempImage, cmin=0, cmax=255).save(targetFolderPath+'/frame'+'{}'.format(2*sequenceLength - i).zfill(3)+'.jpg')
			alpha += increment


		Image.fromarray(self.endImage).save(targetFolderPath + "/frame" + "{}".format(i + 1).zfill(3) + ".jpg", 'JPEG')


		os.system("ffmpeg -framerate 5 -i "+ targetFolderPath + "/frame%03d.jpg "+ targetFolderPath + "/morph.mp4")

		return
#
if __name__ == "__main__":
#
# 	begin = time.time()
	start = 'Abhi_color.jpg'
	end = 'rock_color.jpg'
	sourceImage = imageio.imread(start)
	endImage = imageio.imread(end)
	startPoints = np.loadtxt('Abhi.txt')
	endPoints = np.loadtxt('rock.txt')
	Image1 = ColorBlender(np.array(sourceImage), startPoints, np.array(endImage), endPoints)
	test_image  = Image1.getBlendedImage(0.5)
	Image.fromarray(test_image).show()
    #
	# # myImage = Image1.getBlendedImage(0.5)
	# # givenImage = np.array(imageio.imread('frame021.png'))
    #
	# # print(np.mean(np.abs(givenImage-myImage)))
	# # Image.fromarray(test_image).show()
	# # print(test_image)
	# Image1.generateMorphVideo("Test", 25, True)
	# end = time.time()
	# print(end-begin)

	# start = 'Abhi_color.jpg'
	# end = 'rock_color.jpg'
	# sourceImage = ndimage.imread(start)
	# endImage = ndimage.imread(end)
	# startPoints = np.loadtxt('Abhi.txt')
	# endPoints = np.loadtxt('rock.txt')
	# Image1 = ColorBlender(np.uint8(sourceImage), startPoints, np.uint8(endImage), endPoints)
	# # test_image  = Image1.getBlendedImage(0.5)
	# # Image.fromarray(test_image).show()
	# Image1.generateMorphVideo("Test", 20, True)
	# end = time.time()
	# print(end-begin)




	# affine = Affine(source, destination)
	# print(affine.matrix.dtype)
	# im = imageio.imread('Tiger2Color.jpg')
	# print(im)
	# im = imageio.imread('Tiger2Gray.jpg')
	# print(im)
