import cv2
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

startTime = int(time.time())
while True:
    endTime = int(time.time())
    if (endTime - startTime) % 100 == 0:
        fileName = photo()
        # fileName = "Real/Version_2/opencv-/newlens2.png"
        image_bgr = cv2.imread(fileName)
        image_rgb = image_bgr[:, :, ::-1]
        plt.imshow(image_rgb)
        plt.show()
