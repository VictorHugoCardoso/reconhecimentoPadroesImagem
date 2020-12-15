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

  n = 0 # Counter for boundary pixels

  while True:
    # Check convergence criteria. We terminate the algorithm when we are back
    # at the starting point.
    if n > 2:
      if ((boundary_positions[n-1] == boundary_positions[0]) and
              (boundary_positions[n] == boundary_positions[1])):
        break

    search_neighbourhood = True # This variable indicates whether to continue
                                # to search the local neighbourhood for an
                                # object pixel
    loc_counter = 0 # This variable keeps track of how many local neighbourhood
                    # pixels we have searched.
    x, y = boundary_positions[n] # We get the (x,y)-coordinates of our current
                                 # position on the boundary.

    # Then, we search the neighbourhood of (x,y) for an object pixel.
    while search_neighbourhood:

      # Find the next pixel in the neighbourhood of (x,y) to check (we search
      # in a clockwise direction in the local neighbourhood also)
      direction = np.mod(start_search_directions[n] - loc_counter, connectivity)
      next_x, next_y = next_index_in_neighbourhood(x, y, direction)

      # If we go beyond the image frame, we skip it, and continue the search
      # from the next pixel in the neighbourhood.
      if next_x < 0 or next_x >= M or next_y < 0 or next_y >= N:
        search_neighbourhood = True
        loc_counter += 1
        continue

      # Check if we encountered an object pixel
      if not (image[next_x, next_y] == background):
        # Found one: terminate the search in this neighbourhood
        search_neighbourhood = False
      else:
        # Did not find one: continue the search in this neighbourhood
        loc_counter += 1
        #search_neighbourhood = True

    # We append the direction we used to find the object pixel to the chain
    # code, and also update the list of boundary positions
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
        print(boundary)
        print(firstPoint)
        print(perimetro)


        info = [nome, 'folha{}'.format(n), perimetro, chain_code]
        cabecalho.append(info)

        break
    
    return info

def main():
    folder = 'imagens/dangerzone/'
    nome = 'Teste02' # arquivo

    nFolhas = cutLeafs(folder, nome)
    infoCSV = eachLeaf(folder, nome, nFolhas)
    writeCSV(folder, infoCSV)

main()



#newX, newY = next_index_in_neighbourhood(start_point[0],start_point[1], 8)




