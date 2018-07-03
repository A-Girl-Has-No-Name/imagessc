import numpy.matlib 
import numpy as np 
import random
import image_slicer
from image_slicer import join
from itertools import product
import skimage.measure
from skimage import color
import scipy
#from skimage import viewer
from skimage import io
from skimage import exposure
#import pylab
import scipy.signal
from PIL import Image, ImageDraw


#image = Image.open("temp.jpg") #Открываем изображение. 
dim = input("Enter matrix dim: ")
dim = int (dim)
print (dim)

tiles = image_slicer.slice('star.png', 9, save = False)

lst = []

i = 0
for tile in tiles:
       if (i<12) : 
              lst.append((i, tile))
              i+=1

print("firstlist: ")
print (lst)
print("\n\n\n")


sk = np.random.randint(500, size=dim)
sk = np.float_(sk)
print ("sk = ")
print (sk) 




def encryption(x, sk, dim):
       print (type(dim))
       D = np.random.randint(500, size=(dim, dim))
       H = np.random.randint(-100, 100, size=(dim, dim))
       H = np.float_(H)
       D = np.float_(D)
       x = np.float_(x)
       D[0][0] = x
       for i in range(1,dim):
              D[i][0] = 0.
       for i in range(0,dim):
              H[i][0] = sk[i]     
       H = np.asmatrix(H)
       D = np.asmatrix(D)
       H1 = np.linalg.inv(H) 
       M = np.matmul(H,D)
       M = np.matmul(M, H1)
       return M

def decryption (M,sk):
       res = np.matmul(M,sk)
       res = np.squeeze(np.asarray(res))
       res[0] = res[0]/sk[0]
       res[1] = res[1]/sk[1]
       if ( abs(res[0]-res[1])>0.01 ) :
              print ("error")
       return int(round(res[0]))



def brightness (image, factor):
       draw = ImageDraw.Draw(image) 
       width = image.size[0] 
       height = image.size[1]        
       pix = image.load() 

       
       for i in range(width):
              for j in range(height):
                     a = pix[i, j][0] + factor
                     b = pix[i, j][1] + factor
                     c = pix[i, j][2] + factor
                     if (a < 0):
                            a = 0
                     if (b < 0):
                            b = 0
                     if (c < 0):
                            c = 0
                     if (a > 255):
                            a = 255
                     if (b > 255):
                            b = 255
                     if (c > 255):
                            c = 255
                     draw.point((i, j), (a, b, c))
       del draw


def negativ (image):
       draw = ImageDraw.Draw(image) 
       width = image.size[0] 
       height = image.size[1]        
       pix = image.load() 

       for i in range(width):
              for j in range(height):
                     a = pix[i, j][0]
                     b = pix[i, j][1]
                     c = pix[i, j][2]
                     draw.point((i, j), (255 - a, 255 - b, 255 - c))
                     draw.point((i, j), (a, b, c))
       del draw

def noise (image):
       draw = ImageDraw.Draw(image) 
       width = image.size[0] 
       height = image.size[1]        
       pix = image.load() 
       for i in range(width):
              for j in range(height):
                     rand = random.randint(-factor, factor)
                     a = pix[i, j][0] + rand
                     b = pix[i, j][1] + rand
                     c = pix[i, j][2] + rand
                     if (a < 0):
                            a = 0
                     if (b < 0):
                            b = 0
                     if (c < 0):
                            c = 0
                     if (a > 255):
                            a = 255
                     if (b > 255):
                            b = 255
                     if (c > 255):
                            c = 255
                     draw.point((i, j), (a, b, c))
       del draw


def blackwhite (image):
       draw = ImageDraw.Draw(image) 
       width = image.size[0] 
       height = image.size[1]        
       pix = image.load() 

       for i in range(width):
              for j in range(height):
                     a = pix[i, j][0]
                     b = pix[i, j][1]
                     c = pix[i, j][2]
                     S = a + b + c
                     if (S > (((255 + factor) // 2) * 3)):
                            a, b, c = 255, 255, 255
                     else:
                            a, b, c = 0, 0, 0
                     draw.point((i, j), (a, b, c))
       del draw 




def swaptiles (lst, M, N):     
       for i in range(len(lst)):
              if np.allclose(lst[i][0], M):
                     a = i 
                     for j in range(len(lst)):
                            if np.allclose(lst[j][0], N):
                                   b = j
                                   tile1 = lst[i][1]
                                   tile2 = lst[j][1]
                                   img1 = tile1.image
                                   brightness (img1, 100)
                                   img2 = tile2.image
                                   tile1.image = img2
                                   tile2.image = img1
                                   #pix = numpy.array(tile2.image)
                                   #print ("array from image:    \n")
                                   #print (pix) 
                                   return  lst  




def bypixels (lst): 
       factor = int(input('increase brightness on...?:'))    
       for i in range(len(lst)):
              tile1 = lst[i][1]
              img1 = tile1.image
              brightness(img1, factor)
       return  lst                                     
                     
                
newlst = []
check = 0

for th in lst:
       MA = encryption(th[0], sk, dim)
       #print (MA)
       if (check == 2):
               M = MA
       if (check == 1):
               N = MA         
       newlst.append((MA, th[1]))
       check +=1


print("cypheredlist: ")
print (newlst)
print("\n\n\n")

'''
print("M: ")
print (M)
print("\n\n\n")
print("N: ")
print (N)
print("\n\n\n")
'''

finallst = bypixels(newlst)
#swappedlst = swaptiles (newlst1, M, N)


#tiles1 = [None] * len(swappedlst)
#for i in range(len(swappedlst)):
#       tiles1[i] = swappedlst[i][1]

tiles2 = [None] * len(finallst)
for i in range(len(finallst)):
       tiles2[i] = finallst[i][1]


'''
image = join(tiles1)
image.save("starswapped.png")
image.show()
'''
image = join(tiles2)
image.save("starchanged.png")
image.show()

#img = io.imread('star1.png') 
