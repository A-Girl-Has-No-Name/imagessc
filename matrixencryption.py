import numpy.matlib 
import numpy as np 
import random
import copy
import image_slicer
from image_slicer import join
from itertools import product
import skimage.measure
from skimage import color
import scipy
from skimage import io
from skimage import exposure
import scipy.signal
from PIL import Image, ImageDraw


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


def swaptiles (lst, M, N):     #swap tiles with numbers coded as M and N
       lst1 = copy.deepcopy(lst)
       for i in range(len(lst1)):
              if np.allclose(lst1[i][0], M):
                     for j in range(len(lst1)):
                            if np.allclose(lst1[j][0], N):
                                   tile1 = lst1[i][1]
                                   tile2 = lst1[j][1]
                                   img1 = tile1.image
                                   img2 = tile2.image
                                   tile1.image = img2
                                   tile2.image = img1
                                   return  lst1  

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

                
def bynumber (lst, P):            #do something if the number of the  tile is N; brightness increase as example
       factor = int(input('increase brightness on...?:'))    
       for i in range(len(lst)):
              if np.allclose(lst[i][0], P):
                     tile1 = lst[i][1]
                     img1 = tile1.image
                     brightness(img1, factor)
                     return  lst                                     
                                           

newlst = []
check = 0

for th in lst:                #create a new list with numbers encrypted. The 1st and 2nd are marked as N and M
       MA = encryption(th[0], sk, dim)
       if (check == 2):
               M = MA
       if (check == 1):
               N = MA   
       if (check == 6):
               P = MA       
       newlst.append((MA, th[1]))
       check +=1

swappedlst = swaptiles (newlst, M, N)
finlst = bynumber(newlst, P)

tiles1 = [None] * len(swappedlst)
for i in range(len(swappedlst)):
       tiles1[i] = swappedlst[i][1]


image = join(tiles1)
image.save("swapped.png")
image.show()

tiles2 = [None] * len(finlst)
for i in range(len(finlst)):
       tiles2[i] = finlst[i][1]

image = join(tiles2)
image.save("onepiece.png")
image.show()
