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
    positionX = [[100, 248, 397, 546, 787, 927, 1063, 1190],
                 [100, 242, 392, 539, 789, 929, 1069, 1195],
                 [97, 242, 392, 541, 791, 929, 1069, 1197],
                 [100, 244, 395, 537, 787, 931, 1067, 1197],
                 [108, 248, 395, 543, 789, 929, 1065, 1194],
                 [116, 257, 401, 546, 789, 925, 1061, 1188]]
    positionY = [[128, 128, 131, 128, 135, 141, 148, 154],
                 [273, 273, 271, 273, 284, 286, 290, 292],
                 [422, 417, 415, 417, 428, 424, 433, 435],
                 [562, 566, 566, 568, 570, 573, 573, 571],
                 [709, 711, 713, 711, 721, 715, 711, 709],
                 [853, 859, 862, 862, 864, 853, 847, 840]]
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
    if (endTime - startTime) % 300 == 0:
        fileName = photo()
        # fileName = "Real/Version_2/opencv-/test_pos.jpg"
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
        colorFile.write("Sample %d  %s\n\n" %(k, str(time.ctime())))
        k = k + 1
        for j in range(48):
            # print("value[%d] = " %j, color_value[j], detec_value[j])
            colorFile.write("color_value[%2d] = %s, sample_value[%2d] = %s\n" %(j, color_value[j], j, sample_value[j]))
        colorFile.write("\n\n")
        colorFile.close()



# code's location: Desktop/課外專業/iGEM國際基因工程競賽/DryLab/MV-kit/影像辨識

# Tue Sep  4 08_19_58 2018
# Tue Sep  4 10_39_58 2018

