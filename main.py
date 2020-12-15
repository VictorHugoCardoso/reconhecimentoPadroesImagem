import PIL
from PIL import Image, ImageFilter
import numpy as np
import cv2 as cv
import csv

def next_index_in_neighbourhood(x, y, direction):
    dx, dy = dir_to_coord(direction)
    next_x = x + dx
    next_y = y + dy
    return next_x, next_y

def dir_to_coord(direction):
    if direction == 0:
        dx = 0
        dy = 1
    if direction == 1:
        dx = -1
        dy = 1
    if direction == 2:
        dx = -1
        dy = 0
    if direction == 3:
        dx = -1
        dy = -1
    if direction == 4:
        dx = 0
        dy = -1
    if direction == 5:
        dx = 1
        dy = -1
    if direction == 6:
        dx = 1
        dy = 0
    if direction == 7:
        dx = 1
        dy = 1

    return dx, dy


def trace_boundary(image):
  connectivity = 8
  background = 0

  M, N = image.shape
  previous_directions = [] 
  start_search_directions = [] 
  boundary_positions = [] 

  found_object = False

  # localiza o pixel mais à cima e à esquerda
  for x in range(M):
    for y in range(N):
      if not (image[x, y] == background):
        p0 = [x, y]
        found_object = True
        break
    if found_object:
      break

  boundary_positions.append(p0)
  previous_directions.append(7)
  start_search_directions.append(np.mod((previous_directions[0] - 6), 8))

  n = 0 # numPixels

  while True:
    # acaba o algoritmo quando chega no pixel inicial
    if n > 2:
      if ((boundary_positions[n-1] == boundary_positions[0]) and
              (boundary_positions[n] == boundary_positions[1])):
        break

    search_neighbourhood = True 
    loc_counter = 0

    x, y = boundary_positions[n] # (x,y) do pixel atual do contorno
                                 

    # procura (x,y) vizinho
    while search_neighbourhood:

      # procura o próximo pixel conectado
      direction = np.mod(start_search_directions[n] - loc_counter, connectivity)
      next_x, next_y = next_index_in_neighbourhood(x, y, direction)

      if next_x < 0 or next_x >= M or next_y < 0 or next_y >= N:
        search_neighbourhood = True
        loc_counter += 1
        continue

      # Checa se encontrou pixel
      if not (image[next_x, next_y] == background):
        # Se sim, termina de procurar nessa vizinhança
        search_neighbourhood = False
      else:
        # Se não, continua a procurar nessa vizinhança
        loc_counter += 1

    # atualiza a lista de direções e a lista de limite
    previous_directions.append(direction)
    boundary_positions.append([next_x, next_y])


    if np.mod(direction, 2):
        #par
        start_search_directions.append(np.mod(direction - 6, 8))
    else:
        #impar
        start_search_directions.append(np.mod(direction - 7, 8))

    n += 1

  chain_code = previous_directions[1:-1]

  return chain_code, boundary_positions, p0, n

def toCannyDetect(img):
    tempImage = img.convert('L').point(lambda x: 0 if x < 128 else 255, 'L')
    return tempImage.filter(ImageFilter.FIND_EDGES) 


def showImg(img):
    cv.imshow('image', img)
    cv.waitKey(5000)
    cv.destroyAllWindows()

def writeCSV(folder, vector):
    with open(folder+"informacao.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(vector)

# recortar as folhas
def cutLeafs(folder, nome):
    
    img = cv.imread(folder+nome+'.png')
    copy = img.copy()
    imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imgray, 200, 255, 0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    nFolhas = 0

    for i in range(1,len(contours)): 
        if(cv.contourArea(contours[i]) > 100.0): # tava pegando algumas áreas ridiculas
            nFolhas += 1
            '''
            print(i, cv.contourArea(contours[i]))

            # faz um bound box do contorno identificado
            x,y,w,h = cv.boundingRect(contours[i])
            ROI = img[y:y+h, x:x+w]
            cv.imwrite(folder+nome+'-{}.png'.format(nFolhas), ROI)

            drawing = np.zeros(img.shape)
            cv.drawContours(drawing, contours, i, (255, 255, 255), 1, 8, hierarchy)
            ROIGray = drawing[y:y+h, x:x+w]
            cv.imwrite(folder+nome+'-{}-P.png'.format(nFolhas), ROIGray)

            cv.rectangle(copy,(x,y),(x+w,y+h),(0,0,255),2)
            cv.imwrite(folder+nome+'ident'+'.png',copy)
            '''

    print('\nNúmero de contornos: ',  len(contours))
    print('Número de folhas identificadas: ', nFolhas)
    return nFolhas

def eachLeaf(folder, nome, nFolhas):
    cabecalho = [['fonte','folha','perimetro','freeman']] # cabecalho csv

    for n in range(1,nFolhas+1): 
        thresh = cv.imread(folder+nome+'-{}-P.png'.format(n), cv.IMREAD_GRAYSCALE)
        height, width = thresh.shape

        image = thresh.copy()
        
        chain_code, boundary, firstPoint, perimetro = trace_boundary(image)
        print(chain_code)
        #print(boundary)
        print('firstPoint: ', firstPoint)
        print('perimetro: ', perimetro)


        info = [nome, 'folha{}'.format(n), perimetro, chain_code]
        cabecalho.append(info)

        break
    
    return cabecalho

def main():
    folder = 'imagens/dangerzone/'
    nome = 'Teste02' # arquivo
    
    nFolhas = cutLeafs(folder, nome)
    infoCSV = eachLeaf(folder, nome, nFolhas)
    writeCSV(folder, infoCSV)

main()

 