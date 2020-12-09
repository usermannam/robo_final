import cv2
import numpy as np
import matplotlib.pyplot as plt

def nothing(x):
    pass

cv2.namedWindow('threshold')
cv2.createTrackbar('HD', 'threshold', 0, 360, nothing)
cv2.createTrackbar('HU', 'threshold', 0, 360, nothing)
cv2.createTrackbar('S', 'threshold', 0, 255, nothing)
# cv2.createTrackbar('V', 'threshold', 0, 255, nothing)


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

        # cv2.imshow('or', img_color)

        # img_binary = cv2.cvtColor(img_color, cv2.COLOR_HSV2BGR)
        # img_binary = cv2.cvtColor(img_binary, cv2.COLOR_BGR2GRAY)
        low_hd = cv2.getTrackbarPos('HD', 'threshold')
        low_hu = cv2.getTrackbarPos('HU', 'threshold')
        low_s = cv2.getTrackbarPos('S', 'threshold')
        # low_v = cv2.getTrackbarPos('V', 'threshold')
        '''여기 마지막 인자에 따라 밝게 어둡게..'''
        temh_img = np.copy(img_color[:, :, 0])
        tems_img = np.copy(img_color[:, :, 1])
        temv_img = np.copy(img_color[:, :, 2])

        temh_img[np.logical_and(temh_img[:, :] > low_hd, temh_img[:, :] <= low_hu)] = 255
        temh_img[temh_img[:, :] < 255] = 0
        # print(temh_img)
        tems_img[tems_img[:, :] >= low_s] = 255
        tems_img[tems_img[:, :] < low_s] = 0
        # tem_img[tem_img[:, :, 2] > low_v] = 255
        # tem_img[tem_img[:, :, 2] < low_v] = 0
        temv_img[:, :] = 0


        # ret,img_binary = cv2.threshold(img_binary, low_h, 255, cv2.THRESH_BINARY_INV)

        cv2.imshow('H', temh_img)
        cv2.imshow('S', tems_img)
        cv2.imshow('V', temv_img)
        # img_binary[img_binary!=255] = 0
        # img_binary = cv2.Canny(img_binary, 50, 200, apertureSize=5)
        cv2.imshow('threshold', img_color)

        # img_result = cv2.bitwise_and(img_color, img_color, mask=img_color)
        # cv2.imshow('Result', img_color)


        if cv2.waitKey(1)&0xFF == 27:
            break

plt.show()
cv2.destroyAllWindows()