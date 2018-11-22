import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import time
import os
import paho.mqtt.client as mqttClient

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
    else:
        print("Connection failed")

def photo():
    if cv2.VideoCapture(0).isOpened() == 0:
        client.publish("python/test", "Camera not functioning")
        return -1
    else:
        camera = cv2.VideoCapture(0)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
        ret, frame = camera.read()
        savingBase = "image"
        fileName = "camera " + str(time.ctime()) + ".jpg"
        cv2.imwrite(fileName, frame)
        camera.release()
        return fileName

def filter(image):
    blue = green = red = 0
    color = [[0 for i in range(3)] for j in range(4)]
    startX = 47
    startY = 81
    # row_length = [47, 190, 366, 475, 829, 959, 1091, 1226]
    # column_length = [92, 247, 391, 500, 646, 772]
    positionX = [[165, 339, 515, 684, 851, 1018],
                 [158, 333, 509, 683, 854, 1020],
                 [150, 325, 505, 681, 851, 1019],
                 [145, 322, 500, 673, 848, 1017]]
    positionY = [[157, 157, 159, 166, 178, 186],
                 [322, 326, 329, 336, 341, 349],
                 [504, 509, 514, 514, 520, 522],
                 [684, 687, 692, 695, 695, 691]]
    square_length = 10
    for i in range(4):
        j = i + 1
        r = j % 6
        c = math.floor(j / 6)
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

def mvkit(sample, time, start):
    for i in range(4):
        sample[i] = time * i + 16
    print(sample)
    return sample

def analysis(color, sample, detec, interval):
    for i in range(4):
        if color[i][0] < 255 and color[i][1] < 200 and color[i][2] < 150 and detec[i] == 0:
            timeInterval = interval - sample[i]
            print(timeInterval)
            detec[i] = ((timeInterval * 100) ** (-17.8126)) * 7.1825 * (10 ** 57)
            detec[i] = round(detec[i], 2)
    
    client.publish("python/test", "send")
    for i in range(4):
        client.publish("python/test", detec[i])
                
    return detec

Connected = False   #global variable for the state of the connection
 
broker_address= "m14.cloudmqtt.com"  #Broker address
port = 17476                         #Broker port
user = "fxrzavwa"                #Connection username
password = "YJvtjXgFgxKP"            #Connection password
 
client = mqttClient.Client("Python")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.connect(broker_address, port=port)          #connect to broker
 
client.loop_start()        #start the loop

while Connected != True:    #Wait for connection
    time.sleep(0.1)

client.publish("python/test", "connected")

startTime = int(time.time())
endTime = int(time.time())
interval = endTime - startTime
previousTime = endTime - 10
sample_value = [0 for i in range(4)]
sample_value = mvkit(sample_value, 1, startTime)
detec_value = [0 for i in range(4)]
i = 0
k = 0
n = 0
while True:
    if interval % 30 == 0 and endTime - previousTime > 5:
        print("write %d" %(k))
        print(interval)
        savingBase = "image"
        fileName = photo()
        if fileName != -1:
            image_bgr = cv2.imread(fileName)
            # fileName = "../image/camera Fri Oct 19 17:21:56 2018.jpg"
            # image_bgr = cv2.imread(fileName)
            image_rgb = image_bgr[:, :, ::-1]
            # plt.imshow(image_rgb)
            # plt.show()
            # r, g, b = image_rgb[20, 300]
            # print("位置(20, 300)處的像素 -> 红:%d, 綠:%d, 藍:%d" %(r,g,b))
            
            color_value = filter(image_rgb)
            
            if k > 0:
                detec_value = analysis(color_value, sample_value, detec_value, interval)

            colorFile = open("color_value_ver1.txt", "a")
            colorFile.write("Sample %d  %s\n\n" %(k, str(time.ctime())))
            k = k + 1
            for j in range(4):
                # print("value[%d] = " %j, color_value[j], detec_value[j])
                colorFile.write("color_value[%2d] = %s, detec_value[%2d] = %s\n" 
                                %(j, color_value[j], j, detec_value[j]))
            colorFile.write("\n\n")
            colorFile.close()
        previousTime = endTime
    endTime = int(time.time())
    interval = endTime - startTime



# code's location: Desktop/課外專業/iGEM國際基因工程競賽/DryLab/MV-kit/影像辨識

# Tue Sep  4 08_19_58 2018
# Tue Sep  4 10_39_58 2018
