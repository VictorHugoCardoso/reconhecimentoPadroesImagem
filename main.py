import PIL
from PIL import Image
import numpy as np

caminho_img = 'example.png'
img = Image.open('imagens/' + caminho_img).convert('L').point(lambda x: 0 if x < 128 else 255, 'L')

print("Formato:", img.format)
print("Size:", img.size)
print("Mode:", img.mode)

nparray = np.array(img)

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

def erodeCross(ar,x):
    for n in range(x):   
        for i in range(ar.shape[0]):
            for j in range(ar.shape[1]):
                if (ar[i, j] == 0):
                    if ((i>0) and (ar[i-1, j]==255)):
                        ar[i-1,j] = 2 #cima
                    
                    if ((j>0) and (ar[i, j-1]==255)):
                        ar[i,j-1] = 2 #esquerda
                    
                    if ((i+1<ar.shape[0]) and (ar[i+1, j]==255)):
                        ar[i+1, j] = 2 #baixo

                    if ((j+1<ar.shape[1]) and (ar[i, j+1]==255)):
                        ar[i, j+1] = 2 #direita

        for i in range(ar.shape[0]):
            for j in range(ar.shape[1]):
                if (ar[i, j] == 2):
                    ar[i, j] = 0

        print(n,'...')
    print('Eroded:\n',ar)
    finalImage = Image.fromarray(np.uint8(ar))
    finalImage.save('imagens/geradas/eroded.png')
    #finalImage.show()


dilateCross(nparray, 2)  # n