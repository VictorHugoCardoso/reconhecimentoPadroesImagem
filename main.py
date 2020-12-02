import PIL
from PIL import Image, ImageFilter
import numpy as np
import cv2 as cv

def toCannyDetect(img):
    tempImage = img.convert('L').point(lambda x: 0 if x < 128 else 255, 'L')
    return tempImage.filter(ImageFilter.FIND_EDGES) 

'''
def dilateCross(ar,x):
    for n in range(x): 
        for i in range(ar.shape[0]):
            for j in range(ar.shape[1]):
                if (ar[i, j] == 255):
                    if ((i>0) and (ar[i-1, j]==0)):
                        ar[i-1,j] = 2 #cima
                    
                    if ((j>0) and (ar[i, j-1]==0)):
                        ar[i,j-1] = 2 #esquerda
                    
                    if ((i+1<ar.shape[0]) and (ar[i+1, j]==0)):
                        ar[i+1, j] = 2 #baixo

                    if ((j+1<ar.shape[1]) and (ar[i, j+1]==0)):
                        ar[i, j+1] = 2 #direita

        for i in range(ar.shape[0]):
            for j in range(ar.shape[1]):
                if (ar[i, j] == 2):
                    ar[i, j] = 255
        print(n,'...')

    print('Dilated:\n',ar)
    finalImage = Image.fromarray(np.uint8(ar))
    finalImage.save('imagens/geradas/dilatedCross.png')
    #finalImage.show()
'''

folder = 'imagens/dangerzone/'
nome = 'Teste02'

img = cv.imread(folder+nome+'.png')
copy = img.copy()
imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 200, 255, 0)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

nfolhas = 0 
for i in range(1,len(contours)): 
    if(cv.contourArea(contours[i]) > 100.0): # tava pegando algumas áreas ridiculas
        nfolhas += 1
        print(i, cv.contourArea(contours[i]))

        x,y,w,h = cv.boundingRect(contours[i])
        ROI = img[y:y+h, x:x+w]
        cv.imwrite(folder+nome+'_ROI_{}.png'.format(nfolhas), ROI)

        cv.rectangle(copy,(x,y),(x+w,y+h),(0,0,255),2)
        cv.imwrite(folder+nome+'ident'+'.png',copy)
        

print('\nNúmero de contornos: ',  len(contours))
print('Número de folhas identificadas: ', nfolhas)

'''
cv.imshow('image', img)
cv.waitKey(5000)
cv.destroyAllWindows()
'''


'''
img = Image.open('imagens/' + caminho_img)


print("Formato:", img.format)
print("Size:", img.size)
print("Mode:", img.mode)

grayImg = toCannyDetect(img)
grayImg.show()

nparray = np.array(grayImg)
print('Array:\n',nparray)
finalImage = Image.fromarray(np.uint8(nparray))
'''
