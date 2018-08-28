import cv2
import numpy as np
import os

def photo():    #透過相機讀取影像並存入 "os.path.join(img_saving_base,filename)" 路徑中
    img_saving_base = "/home/ell/ee2405/emlab5/img"
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    filename = "img.jpg"
    cv2.imwrite(os.path.join(img_saving_base,filename), frame)
    camera.release()


def distance(img):

    # img size
    h, w, ch = img.shape

    # hsv img
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # detect led's color
    lower_led = np.array([10,0,200])
    upper_led = np.array([50,10,255])
    mask = cv2.inRange(img_hsv, lower_led, upper_led)
    img_result = cv2.bitwise_and(img_hsv, img_hsv, mask=mask)

    # erosion and dilation
    img_result = cv2.dilate(img_result, None, iterations = 4)

    # change to binary (0 or 255)
    th, img_binary = cv2.threshold(img_result[:,:,0], 1, 255, cv2.THRESH_BINARY)

    # hough circle
    circles = cv2.HoughCircles(img_binary, cv2.HOUGH_GRADIENT, 3, 20, param1=50,param2=30,minRadius=0,maxRadius=30)
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)

    led_distance = np.sqrt(np.square(circles[0,0,0] - circles[0,1,0]) + np.square(circles[0,0,1] - circles[0,1,1]))
    print(led_distance)

    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    filename = "ans_" + str(int(led_distance)) +".jpg"
    cv2.imwrite(filename, img)

#photo()
img_saving_base = r"C:\Users\張傳佳\Desktop\課外專業\iGEM國際基因工程競賽\DryLab\MV-kit\影像辨識"
filename = "img_before.jpg"
img = cv2.imread(filename)
distance(img)