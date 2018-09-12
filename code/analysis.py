import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import time

def photo():
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
    ret, frame = camera.read()
    fileName = "camera " + str(time.ctime()) + ".jpg"
    cv2.imwrite(fileName, frame)
    camera.release()
    return fileName

def filter(image):
    blue = green = red = 0
    color = [[0 for i in range(3)] for j in range(48)]
    startX = 47
    startY = 81
    # row_length = [47, 190, 366, 475, 829, 959, 1091, 1226]
    # column_length = [92, 247, 391, 500, 646, 772]
    positionX = [[74, 231, 377, 520, 742, 890, 1025, 1155],
                 [74, 229, 377, 526, 752, 896, 1034, 1172],
                 [76, 229, 380, 526, 753, 898, 1038, 1172],
                 [90, 233, 382, 530, 759, 902, 1044, 1177],
                 [97, 242, 388, 530, 768, 906, 1045, 1179],
                 [102, 250, 395, 535, 768, 909, 1045, 1174]]
    positionY = [[88, 131, 129, 122, 56, 63, 65, 74],
                 [224, 271, 271, 269, 210, 203, 210, 214],
                 [372, 422, 417, 415, 357, 350, 352, 352],
                 [517, 566, 564, 564, 503, 495, 495, 493],
                 [661, 706, 709, 706, 651, 644, 635, 627],
                 [806, 846, 855, 846, 791, 782, 767, 759]]
    square_length = 20
    for i in range(48):
        r = i % 8
        c = math.floor(i / 8)
        centerX = positionX[c][r]
        centerY = positionY[c][r]
        for j in range(square_length * square_length):
            # print(i)
            # print(math.floor(centerX - square_length / 2 + j % square_length))
            # print(math.floor(centerY - square_length / 2 + j / square_length))
            b, g, r = image[math.floor(centerY - square_length / 2 + j % square_length), 
                            math.floor(centerX - square_length / 2 + j / square_length)]
            blue += b
            green += g
            red += r
        blue /= square_length * square_length
        green /= square_length * square_length
        red /= square_length * square_length
        color[i][:] = [blue, green, red]
        blue = green = red = 0
    return color

def mvkit(sample, i):
    #########################################
    # give the sample in fish farm to mvkit #
    #########################################
    sample[i] = int(time.time())
    return sample

def analysis(color, sample, detec):
    anaFile = open("ana_value.txt", "a")
    for i in range(48):
        if color[i][0] < 110 and color[i][1] < 90 and color[i][2] < 90:
            if detec[i] == 0:
                detec[i] = int(time.time()) - sample[i]
            # print("color_value[%d] = " %i, color[i], detec[i])
                anaFile.write("color_value[%2d] = %s, detec_value[%2d] = %s\n" %(i, color[i], i, detec[i]))
            if detec[i] < 21600:
                a = 1
                ##########################
                # send dangerous message #
                ##########################
            elif detec[i] < 86400:
                a = 1
                #########################
                # send original message #
                #########################
            else:
                a = 1
                ############################
                # need not to send message #
                ############################
    anaFile.close()
    return detec

startTime = int(time.time())
sample_value = [startTime for i in range(48)]
detec_value = [0 for i in range(48)]
i = 0
k = 0
while True:
    endTime = int(time.time())
    if (endTime - startTime) % 1200 == 0:
        fileName = photo()
        # fileName = "Real/Version_2/opencv-/newlens2.png"
        image_bgr = cv2.imread(fileName)
        image_rgb = image_bgr[:, :, ::-1]
        # plt.imshow(image_rgb)
        # plt.show()
        # r, g, b = image_rgb[20, 300]
        # print("位置(20, 300)處的像素 -> 红:%d, 綠:%d, 藍:%d" %(r,g,b))
        
        color_value = filter(image_rgb)
        
        # if (endTime - startTime) % 3600 == 0:
        #     sample_value = mvkit(sample_value, i)
        #     i = i + 1
        
        detec_value = analysis(color_value, sample_value, detec_value)

        colorFile = open("color_value.txt", "a")
        colorFile.write("Sample %d\n\n" %(k))
        k = k + 1
        for j in range(48):
            # print("value[%d] = " %j, color_value[j], detec_value[j])
            colorFile.write("color_value[%2d] = %s, sample_value[%2d] = %s\n" %(j, color_value[j], j, sample_value[j]))
        colorFile.write("\n\n")
        colorFile.close()



# code's location: Desktop/課外專業/iGEM國際基因工程競賽/DryLab/MV-kit/影像辨識

# Tue Sep  4 08_19_58 2018
# Tue Sep  4 10_39_58 2018

