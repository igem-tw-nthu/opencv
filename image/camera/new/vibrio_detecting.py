import cv2  #poencv
import numpy as np  #img
import os
import matplotlib.pyplot as plt     #show the image
import time

def photo():    #read and capturedimage through camera and save it in "os.path.join(img_saving_base,filename)"
    img_saving_base = "../image/camera"     #the address of the saved image
    camera = cv2.VideoCapture(0)    #open the webcam
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
    ret, frame = camera.read()      #read the captured the image
    filename = "real.jpg"    #the name of the saved image
    cv2.imwrite(os.path.join(img_saving_base, filename), frame)      #save the captured image
    camera.release()    #close the webcam

    #plt.imshow(frame)
    #plt.show()

def distance(img):

    # img size
    h, w, ch = img.shape    #the dimension of the input image

    # hsv img
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  #convert the BGR image to the HSV inage

    # detect led's color
    lower_led = np.array([0,70,30])    #the lowest boundary of the needed color
    upper_led = np.array([20,210,110])  #the highest boundary of the needed color
    mask = cv2.inRange(img_hsv, lower_led, upper_led)   #the filtered value of the image
    img_result1 = cv2.bitwise_and(img_hsv, img_hsv, mask=mask)   #filter the image to remain the needed part of color
    lower_led = np.array([150,70,30])    #the lowest boundary of the needed color
    upper_led = np.array([180,210,110])  #the highest boundary of the needed color
    mask = cv2.inRange(img_hsv, lower_led, upper_led)   #the filtered value of the image
    img_result2 = cv2.bitwise_and(img_hsv, img_hsv, mask=mask)   #filter the image to remain the needed part of color
    img_result = cv2.bitwise_or(img_result1, img_result2)

    # erosion and dilation
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(4,7))

    #plt.imshow(kernel)
    #plt.show()

    img_dilate = cv2.dilate(img_result, kernel, iterations = 1)   #dilate the filetered part (unknown)

    #plt.imshow(img_dilate)
    #plt.show();

    # change to binary (0 or 255)
    th, img_binary = cv2.threshold(img_dilate[:,:,0], 1, 255, cv2.THRESH_BINARY)

    # hough circle
    circles = cv2.HoughCircles(img_binary, cv2.HOUGH_GRADIENT, 3, 10, param1=40,param2=25,minRadius=5,maxRadius=10)
    #find the shape of circle in the image and return the parameter of circles including x, y, and radius

    print(circles[0, 0, 0])     #circles[a, b, c]
    print(circles[0, 0, 1])     #a: (unknown)
    print(circles[0, 1, 0])     #b: the undex of the circle
    print(circles[0, 1, 1])     #c: 0 is x, 1 is y, 2 is radius

    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
    
    print(circles[0, 0, 0])
    print(circles[0, 0, 1])
    print(circles[0, 1, 0])
    print(circles[0, 1, 1])

    led_distance = np.sqrt(np.square(circles[0,0,0] - circles[0,1,0]) + np.square(circles[0,0,1] - circles[0,1,1]))
    #calculate the distance between two circles
    print(led_distance)

    #plt.imshow(img) #show the image
    #plt.show()

    # cv2.imshow('img', img)  #something wrong to close this kind of picture
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    filename = "detected_" + str(int(time.time())) +".jpg"  #the name of the processed image
    img_saving_base = "../image/process"
    cv2.imwrite(os.path.join(img_saving_base, filename), img)  #save the processed image

startTime = int(time.time())
print(startTime)
while True:
    endTime = int(time.time())
    print(endTime)
    if (endTime - startTime) % 10 == 0:
        #photo()
        filename = "../image/camera/real.jpg" #"../image/camera/real.jpg""detected_vibrio.jpg" "camera.jpg"
        img = cv2.imread(filename)  #open and read the image
        distance(img)   #process the image


