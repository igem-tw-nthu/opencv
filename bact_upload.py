# coding=utf-8
import os
import cv2
import requests
import json
import string
import time
from datetime import datetime
import matplotlib.pyplot as plt
# import paho.mqtt.client as mqttClient

def upload_img(img, cnt):

    img_str = cv2.imencode('.jpg', img)[1].tostring()
    name = 'item.jpg'

    files = {}
    files['item'] = (name, img_str)

    print(url)

    try:
        init_time = datetime.now()

        r = requests.post(url, files=files)
        print('upload success')

        response = json.loads(r.text)

        if response['status']['code'] == 0:
            results = response['result']
            anaFile = open("analysis.txt", "a")
            anaFile.write("%s" %(response))
            anaFile.close()
            # print(response)

            for n in range(len(results)):
                print('------------------------------------')
                print('item : %s' %(results[str(n+1)]))

            print('')
        else:
            print('Can not find object.')

        print('total time : {}'.format((datetime.now()-init_time).total_seconds()))
        print('')
        return response

    except :
        print("can't upload image to server")

def position(init):

    pos = [[0 for i in range (3)] for j in range (49)]

    for i in range(48):
        pos[i+1][0] = init['result'][str(i+1)]['x']
        pos[i+1][1] = init['result'][str(i+1)]['y']
        pos[i+1][2] = init['result'][str(i+1)]['id']
    print(pos)
    print('')
    for i in range(2, 49):
        pos[0] = pos[i]
        j = i - 1
        while pos[j][1] > pos[0][1]:
            pos[j+1] = pos[j]
            j = j - 1
        pos[j+1] = pos[0]
    print(pos)
    print('')
    for i in range(6):
        for j in range(0+8*i+2, 8+8*i+1):
            pos[0] = pos[j]
            k = j - 1
            while pos[k][0] > pos[0][0]:
                pos[k+1] = pos[k]
                if k == 0+8*i+1:
                    k = 0
                else:
                    k = k - 1
            if k == 0:
                pos[0+8*i+1] = pos[0]
            else:
                pos[k+1] = pos[0]
    print(pos)
    print('')
    for i in range(48):
        pos[i] = pos[i+1]
    print(pos)
    print('')
    return pos

def mvkit(sample, time, start):
    
    for i in range(4):
        sample[i] = start + time * (i + 1) + 3
    return sample

def analysis(color, location, detec):

    resFile = open("result.txt", "a")
    write = 0

    for i in range(48):
        # print (color['result'][str(location[i][2])]['class'])
        if color['result'][str(location[i][2])]['class'] == 'purple':
            if write == 0:
                resFile.write("Sample %d  %s\n\n" %(times, str(time.ctime())))
            write = 1
            if detec[i] == 0:
                timeInterval = int(time.time()) - sample_value[i]
                if timeInterval != 0:
                    detec[i] = ((timeInterval * 60) ** (-17.8126)) * 7.1825 * (10 ** 57)
                resFile.write("color[%2d] = %s, detec_value[%2d] = %s, time[%2d] = %s\n" %(i, color['result'][str(location[i][2])]['class'], i, detec[i], i, timeInterval))
                # value = "Important"
                # client.publish("python/test", value)
            # client.publish("python", detec[i])
                
    resFile.close()

# Connected = False   #global variable for the state of the connection
# broker_address= "m14.cloudmqtt.com"  #Broker address
# port = 17476                         #Broker port
# user = "fxrzavwa"                #Connection username
# password = "YJvtjXgFgxKP"            #Connection password
# client = mqttClient.Client("Python")               #create new instance
# client.username_pw_set(user, password=password)    #set username and password
# client.on_connect= on_connect                      #attach function to callback
# client.connect(broker_address, port=port)          #connect to broker
# client.loop_start()        #start the loop

startTime = int(time.time())
endTime = int(time.time())
previousTime = endTime - 10
times = 0

sample_value = [startTime for i in range(48)]
sample_value = mvkit(sample_value, 0, startTime)
detec_value = [0 for i in range(48)]

if __name__ == "__main__":
    
    url = "http://210.61.209.194:8000/recog"

    ## Start Camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)

    count = 0

    while(1):

        if (endTime - startTime) % 20 == 0 and endTime - previousTime > 5:
            # ret, frame = cap.read()
            # savingBase = "../image"
            # fileName = "camera " + str(time.ctime()) + ".jpg"
            # cv2.imwrite(os.path.join(savingBase, fileName), frame)
            # image_bgr = cv2.imread(os.path.join(savingBase, fileName))
            # image_rgb = image_bgr[:, :, ::-1]
            # plt.imshow(image_rgb)
            # plt.show()

            fileName = "Real/Version_2/opencv-/newPos.png"
            frame = cv2.imread(fileName)
            frame = frame[:, :, ::-1]
            plt.imshow(frame)
            plt.show()

            #& 0xFF == ord('t')
            analysis_result = upload_img(frame,count)
            justify_result = position(analysis_result)
            times = times + 1
            analysis(analysis_result, justify_result, detec_value)

            previousTime = endTime
        endTime = int(time.time())
    
    cap.release()
    cv2.destroyAllWindows()