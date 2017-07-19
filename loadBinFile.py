#


import numpy as np
import os
import matplotlib.pyplot as plt

# data directory
input = os.getcwd() + "/eval/eval.bin" # either "/eval/eval.bin" or "data/data.bin"
imageSize = 128 #16 or 32
labelSize = 1
imageDepth = 3
debugEncodedImage = True


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

def showImageWithData(data, offset):
    eachColorSize = imageSize * imageSize
    offset = labelSize + (labelSize + eachColorSize * 3) * offset

    rgb = []
    for i in range(267):
        color = eachColorSize * i
        rgbData = data[offset + color : offset + color + eachColorSize]
        rgb.append(rgbData)
    showImage(rgb[0], rgb[1], rgb[2])
for i in range(267):
    data = np.fromfile(input, dtype='u1') # Construct an array from data in a text or binary file. u는 unicode를 의미
    showImageWithData(data, i)
