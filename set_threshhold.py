import cv2
import numpy as np
import matplotlib.pyplot as plt

def nothing(x):
    pass

cv2.namedWindow('threshold')
cv2.createTrackbar('H', 'threshold', 0, 255, nothing)
cv2.createTrackbar('S', 'threshold', 0, 255, nothing)
cv2.createTrackbar('V', 'threshold', 0, 255, nothing)


cap = cv2.VideoCapture(0)
W_View_size = 320  # 320  #640
H_View_size = 240

cap.set(3, W_View_size)
cap.set(4, H_View_size)

while True:
    ret, img_color = cap.read()
    img_color = cv2.cvtColor(img_color, cv2.COLOR_BGR2HSV)  # HSV로 변환
    h, v, c = img_color.shape
    h = int(h * 0.8)  # 발 안보이게 하려고 하단에 짤랐음
    img_color = img_color[:h]  # 발 안보이게 하려고 하단에 짤랐음

    if ret:
        # v_ = img_color[:, :, 2]
        # v_ = (v_ - np.mean(v_)) / np.std(v_)
        #
        # h_ = img_color[:, :, 0]
        # h_ = (h_ - np.mean(h_)) / np.std(h_)
        #
        # img_color[:, :, 2] = v_
        # img_color[:, :, 0] = h_

        cv2.imshow('or', img_color)

        # img_binary = cv2.cvtColor(img_color, cv2.COLOR_HSV2BGR)
        # img_binary = cv2.cvtColor(img_binary, cv2.COLOR_BGR2GRAY)
        low_h = cv2.getTrackbarPos('H', 'threshold')
        low_s = cv2.getTrackbarPos('S', 'threshold')
        low_v = cv2.getTrackbarPos('V', 'threshold')
        '''여기 마지막 인자에 따라 밝게 어둡게..'''
        tem_img = np.copy(img_color)
        tem_img[tem_img[:, :, 0] > low_h] = 179
        tem_img[tem_img[:, :, 1] > low_s] = 255
        tem_img[tem_img[:, :, 2] > low_v] = 255


        # ret,img_binary = cv2.threshold(img_binary, low_h, 255, cv2.THRESH_BINARY_INV)


        # img_binary[img_binary!=255] = 0
        # img_binary = cv2.Canny(img_binary, 50, 200, apertureSize=5)
        cv2.imshow('threshold', tem_img)

        img_result = cv2.bitwise_and(img_color, img_color, mask=img_color)
        cv2.imshow('Result', img_color)


        if cv2.waitKey(1)&0xFF == 27:
            break

plt.show()
cv2.destroyAllWindows()