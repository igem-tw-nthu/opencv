import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import time
import RPi.GPIO as GPIO

channel = 18

def photo():
    # GPIO.output(channel, GPIO.HIGH)
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
    ret, frame = camera.read()
    fileName = "camera" + str(time.ctime()) + ".jpg"
    cv2.imwrite(fileName, frame)
    camera.release()
    # GPIO.output(channel, GPIO.LOW)
    # GPIO.cleanup()
    return fileName

def filter(image):
    blue = green = red = 0
    color = [[0 for i in range(3)] for j in range(96)]
    startX = 156
    startY = 109
    row_length = 125
    column_length = 122
    square_length = 18
    for i in range(24):
        r = i % 4
        c = math.floor(i / 4)
        centerX = startX + row_length * r
        centerY = startY + column_length * c
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
    anaFile = open("ana_value.txt", "w")
    for i in range(24):
        if color[i][0] < 100 and color[i][1] < 50 and color[i][2] < 50:
            if detec[i] == 0:
                detec[i] = int(time.time()) - sample[i]
            # print("color_value[%d] = " %i, color[i], detec[i])
            anaFile.write("color_value[%2d] = %s, detec_value[%2d] = %s\n" %(i, color[i], i, detec[i]))
            if detec[i]< 21600:
                a = 1
                ##########################
                # send dangerous message #
                ##########################
            elif detec[i]< 86400:
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

# def led():
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setwarnings(False)
#     GPIO.setup(channel, GPIO.OUT)

startTime = int(time.time())
sample_value = [0 for i in range(24)]
detec_value = [0 for i in range(24)]
# led()
i = 0
while True:
    endTime = int(time.time())
    if (endTime - startTime) % 1200 == 0:
        fileName = photo()
        # fileName = "detected_vibrio.jpg"
        image_bgr = cv2.imread(fileName)
        image_rgb = image_bgr[:, :, ::-1]
        # plt.imshow(image_rgb)
        # plt.show()
        # r, g, b = image_rgb[20, 300]
        # print("位置(20, 300)處的像素 -> 红:%d, 綠:%d, 藍:%d" %(r,g,b))
        
        color_value = filter(image_rgb)
        
        if (endTime - startTime) % 3600 == 0:
            sample_value = mvkit(sample_value, i)
            i = i + 1
        
        detec_value = analysis(color_value, sample_value, detec_value)

        colorFile = open("color_value.txt", "w")
        for j in range(24):
            # print("value[%d] = " %j, color_value[j], detec_value[j])
            colorFile.write("color_value[%2d] = %s, sample_value[%2d] = %s\n" %(j, color_value[j], j, sample_value[j]))
        colorFile.close()



# code's location: Desktop/課外專業/iGEM國際基因工程競賽/DryLab/MV-kit/影像辨識
