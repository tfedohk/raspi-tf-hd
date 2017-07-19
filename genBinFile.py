import PIL
# Python Image Library. PIL 프로젝트는 2009년 11월을 마지막으로 1.1.7버전을 Release하고 더이상 업데이트가 진행되지 않고 있습니다.
# 하지만 여전히 많은 사람들이 PIL을 사용하고 있습니다. PIL이 그만큼 완벽한 라이브러리이며 굉장히 많은곳에서 쓰이고 있다는 증거입니다.
from PIL import Image
import numpy as np
import os
import matplotlib.pyplot as plt

# data directory
input = os.getcwd() + "/eval" #either "/eval" or "/data". if doing training, then use "/data"
output = os.getcwd() + "/eval/eval.bin" #ethier "/eval/eval.bin" or "/data/data.bin".
imageSize = 16 # 이 수치를 줄이면 좀 더 해상도가 높아짐
imageDepth = 3
debugEncodedImage = False

# show given image on the window for debug
def showImage(r, g, b):
    temp = []
    for i in range(len(r)):
        temp.append(r[i])
        temp.append(g[i])
        temp.append(b[i])
    show = np.array(temp).reshape(imageSize, imageSize, imageDepth)
    plt.imshow(show, interpolation='nearest')
    plt.show()

# convert to binary bitmap given image and write to law output file
def writeBinaray(outputFile, imagePath, label): # 바이너리 파일에 이미지 경로와 라벨값을 붙인다?
    img = Image.open(imagePath)# 이미지를 연다.
    img = img.resize((imageSize, imageSize), PIL.Image.ANTIALIAS)#  ANTIALIAS는 부드럽지만 조금은 연하지만, 포토샵의 손으로 문지른 효과처럼 약간은 번짐이 보이는 이미지.
    img = (np.array(img))

# flatten : 납작하게 만들다.
# flatten메서드는 디폴트로 행방향으로 납작하게 한다. 옵션으로 F를 주면 열방향으로 납작하게 만든 결과를 낸다.
# >>> a = np.array([[1,2], [3,4]])
# >>> a.flatten()
# array([1, 2, 3, 4])
# >>> a.flatten('F')
# array([1, 3, 2, 4])
    r = img[:,:,0].flatten() # 32 * 32 사이즈(예시 사이즈)에 해당하는 영역 중 Red값에 대해 flatten연산을 수행한다. 즉 전체 이미지 사이즈 중 예를 들면 32*32사이즈 부분들씩 뭉개지게 된다.
    g = img[:,:,1].flatten()
    b = img[:,:,2].flatten()
    label = [label]

    out = np.array(list(label) + list(r) + list(g) + list(b), np.uint8)
    outputFile.write(out.tobytes())

    # if you want to show the encoded image. set up 'debugEncodedImage' flag
    if debugEncodedImage:
        showImage(r, g, b)

subDirs = os.listdir(input) #input폴더 내의 sub directory 목록이 저장된다. subDirs는 배열일까?
numberOfClasses = len(input)

try:
    os.remove(output)
except OSError:
    pass

# 기본적으로 open 메서드는 해당 디렉토리에 파일이 없으면 새로 생성시킨다. 파일 객체 = open(파일 이름, 파일 열기 모드).
# a는 추가모드로서 파일의 마지막에 새로운 내용을 추가 시킬 때 사용한다. b플래그는 바이너리 파일을 의미하는데, 파이너리 파일은 플랫폼에 의존적이지 않다는 특징이 있다.
outputFile = open(output, "ab") # output 바이너리 파일(즉, eval.bin파일 혹은 data.bin파일)을 만들고 이 파일 끝에 append한다. 쓰기 전용.
label = -1
totalImageCount = 0
labelMap = []

for subDir in subDirs:#현재 디렉토리에 있는 하위 디렉토리를 하나씩
    subDirPath = os.path.join(input, subDir) #현재 디렉토리에서 하위 디렉토리까지의 전체 경로를 만들고

    # filter not directory
    if not os.path.isdir(subDirPath): #만든 경로가 디렉토리가 아니면 이번 loop는 빠져나가고 다음 loop로 진행한다.
        # continue는 바로 다음 순번의 loop를 돌도록 하게 합니다.
        # http://plaboratory.org/archives/927 여기에 자세한 설명이 있음.
        continue

    imageFileList = os.listdir(subDirPath) #os.listdir은 해당 경로(path)에 존재하는 디렉토리뿐만 아니라 파일들의 리스트를 반환합니다. 아, 그래서 바로 위의 조건문에서 디렉토리인지 아닌지를 검사한 것이구나.
    # 이렇게 하면 전체 이미지 목록이 리스트 형태로 만들어진다.
    # os.listdir의 리턴형은 무엇일까? list다.
    # This method returns a list containing the names of the entries.
    label += 1

    print("writing %3d images, %s" % (len(imageFileList), subDirPath))
    totalImageCount += len(imageFileList)
    labelMap.append([label, subDir])
    # 이 부분이 혹시 라벨링하는 부분인가? 라벨은 순차적으로 0, 1, 2, ...로 붙여지는 숫자인 것으로 보인다. subDir은 하위 디렉토리 이름이다.
    # 즉, 라벨과 하위 디렉토리 이름 배열의 형태로 labelMap에 저장되어 출력된다. 

    for imageFile in imageFileList: # 이미지 파일들의 리스트에서 이미지 파일 하나하나를 꺼내서
        imagePath = os.path.join(subDirPath, imageFile) # 각각의 이미지 파일과 현재 디렉토리~하위 디렉토리까지의 경로 정보를 붙여서 현재 디렉토리~이미지 파일까지의 경로를 만든다.
        writeBinaray(outputFile, imagePath, label) #eval.bin파일 혹은 data.bin파일 하나에 이미지의 경로와 라벨값을 붙인다.

outputFile.close()
print("Total image count: ", totalImageCount)
print("Succeed, Generate the Binary file")
print("You can find the binary file : ", output)
print("Label MAP: ", labelMap)

