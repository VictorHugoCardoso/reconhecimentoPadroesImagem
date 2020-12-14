import PIL
from PIL import Image, ImageFilter
import numpy as np
import cv2 as cv
import csv

def toCannyDetect(img):
    tempImage = img.convert('L').point(lambda x: 0 if x < 128 else 255, 'L')
    return tempImage.filter(ImageFilter.FIND_EDGES) 

# numpy.arctan2(dY, dX)
def slope(x1, y1, x2, y2):
    return (y2-y1)/(x2-x1)

folder = 'imagens/dangerzone/'
nome = 'Teste02' # arquivo

img = cv.imread(folder+nome+'.png')
copy = img.copy()
imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 200, 255, 0)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

nfolhas = 0 
intelFolhas = [['fonte','folha','perimetro']] # cabecalho csv


# função pra recortar as folhas
for i in range(1,len(contours)): 
    if(cv.contourArea(contours[i]) > 100.0): # tava pegando algumas áreas ridiculas
        nfolhas += 1
        '''
        print(i, cv.contourArea(contours[i]))

        # faz um bound box do contorno identificado
        x,y,w,h = cv.boundingRect(contours[i])
        ROI = img[y:y+h, x:x+w]
        cv.imwrite(folder+nome+'-{}.png'.format(nfolhas), ROI)

        drawing = np.zeros(img.shape)
        cv.drawContours(drawing, contours, i, (255, 255, 255), 1, 8, hierarchy)
        ROIGray = drawing[y:y+h, x:x+w]
        cv.imwrite(folder+nome+'-{}-P.png'.format(nfolhas), ROIGray)

        cv.rectangle(copy,(x,y),(x+w,y+h),(0,0,255),2)
        cv.imwrite(folder+nome+'ident'+'.png',copy)
        
        '''



j=0
k=0
perimetro=0

#aqui mapeia o freeman
for n in range(1,nfolhas+1): 
    thresh = cv.imread(folder+nome+'-{}-P.png'.format(n), cv.IMREAD_GRAYSCALE)
    height, width = thresh.shape

    image = thresh.copy()

    # descobre o ponto mais a esquerda superior
    for j in range(thresh.shape[0]):
        for k in range(thresh.shape[1]):
            if (thresh[j][k] == 255):
                start_point = (j, k)
                print(start_point)
                perimetro = perimetro+1
                break
        else:
            continue
        break

    intel = [nome, 'folha{}'.format(n), perimetro]
    intelFolhas.append(intel)

    break

print('\nNúmero de contornos: ',  len(contours))
print('Número de folhas identificadas: ', nfolhas)


with open(folder+"informacao.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(intelFolhas)


'''
cv.imshow('image', img)
cv.waitKey(5000)
cv.destroyAllWindows()
'''
