import random

import numpy as np
import cv2
import matplotlib.pyplot as plt

class Img:
    def __init__(self, gv, stage, cap):
        self.gv = gv
        self.st = stage
        self.cap = cap
        self.size_x = self.gv.size_x
        self.size_y = self.gv.size_y
        self.init_ = True

    def nothing(self, x):
        pass

    # 마우스 이벤트 콜백함수 정의
    def mouse_callback(self, event, x, y, flags, param):
        print("마우스 이벤트 발생, x:", x, " y:", y)  # 이벤트 발생한 마우스 위치 출력

    # 이미지 전처리
    def img_process(self):
        cv2.namedWindow('threshold')
        cv2.createTrackbar('H', 'threshold', 0, 255, self.nothing)
        cv2.createTrackbar('S', 'threshold', 0, 255, self.nothing)
        cv2.createTrackbar('V', 'threshold', 0, 255, self.nothing)
        cv2.setMouseCallback('threshold', self.mouse_callback)
        # 영상 읽기
        while True:
            # 넘어짐 신호 있으면 아무것도 수행 X
            if self.gv.crush:
                continue
            ret, frame = self.cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # HSV로 변환
            h, v, c = frame.shape
            h = int(h * self.gv.roi)  # 발 안보이게 하려고 하단에 짤랐음
            # frame = frame[h-self.gv.m_:h]  # 발 안보이게 하려고 하단에 짤랐음

            # 이미지 읽기
            if ret:
                # 임계값 적용한 이미지
                img_binary = None

                gray = frame[:, :, 1]
                thr = 128
                gray[gray>=thr] = 255
                gray[gray<thr] = 0

                kernel = np.ones((3, 3), np.int8)
                gray = cv2.erode(gray, kernel, iterations=2)
                gray = cv2.dilate(gray, kernel, iterations=2)

                height, width = gray.shape
                t1, t2, b1, b2, l1, l2, r1, r2 = self.return_pixel(gray)
                if t1 is not None:
                    cv2.circle(gray, t1, 10, 80, 5)
                if t2 is not None:
                    cv2.circle(gray, t2, 10, 100, 5)
                if b1 is not None:
                    cv2.circle(gray, b1, 10, 120, 5)
                if b2 is not None:
                    cv2.circle(gray, b2, 10, 140, 5)
                if l1 is not None:
                    cv2.circle(gray, l1, 10, 160, 5)
                if l2 is not None:
                    cv2.circle(gray, l2, 10, 180, 5)
                if r1 is not None:
                    cv2.circle(gray, r1, 10, 200, 5)
                if r2 is not None:
                    cv2.circle(gray, r2, 10, 220, 5)

                cv2.imshow('gv', gray)
                cv2.imshow('threshold', gray)

                # gray = gray[110:165, 110:231]
                # height, width = gray.shape
                #
                # w_c, h_c = self.sum_pixel(gray)
                #
                # top = [i for i, g in enumerate(gray[0]) if g == 255]
                # bottom = [i for i, g in enumerate(gray[-1]) if g == 255]
                # left = [i for i, g in enumerate(gray[:, 0]) if g == 255]
                # right = [i for i, g in enumerate(gray[:, -1]) if g == 255]
                #
                # top_coordinate = [0, None if len(top) == 0 else top[len(top)//2]]
                # bottom_coordinate = [height-1, None if len(bottom) == 0 else bottom[len(bottom) // 2]]
                # left_coordinate = [None if len(left) == 0 else left[len(left) // 2], 0]
                # right_coordinate = [None if len(right) == 0 else right[len(right) // 2], width-1]
                #
                #
                # cv2.imshow('gv', gray)
                # cv2.imshow('threshold', gray)
                #
                k = cv2.waitKey(1)
                # esc 키 종료
                if k == 27:
                    break
                # try:
                #     self.st.stage(top_coordinate, bottom_coordinate, left_coordinate, right_coordinate, w_c, h_c)
                # except:
                #     input()
                # if self.gv.task_step != 1:
                #     break
            else:
                print("error")
                break

    def sum_pixel(self, img):
        a0 = np.sum(img, axis=0)    # 가로
        a1 = np.sum(img, axis=1)    # 세로

        a0 = np.where(a0 > 0)[0]
        a1 = np.where(a1 > 0)[0]

        a0 = None if len(a0) == 0 else a0[len(a0) // 2]
        a1 = None if len(a1) == 0 else a1[len(a1) // 2]

        return a0, a1

    def return_pixel(self, img):
        a0 = np.sum(img, axis=0)  # 가로
        a1 = np.sum(img, axis=1)  # 세로

        a0 = np.where(a0 > 0)[0]
        a1 = np.where(a1 > 0)[0]

        # a0[0] a0[-1]        # left, right
        # a1[0] a1[-1]        # top, bottom
        top = [i for i, g in enumerate(img[a1[0]]) if g == 255]
        bottom = [i for i, g in enumerate(img[a1[-1]]) if g == 255]
        left = [i for i, g in enumerate(img[:, a0[0]]) if g == 255]
        right = [i for i, g in enumerate(img[:, a0[-1]]) if g == 255]

        top_ = None if len(top) == 0 else (top[0], top[-1])
        bottom_ = None if len(bottom) == 0 else (bottom[0], bottom[-1])
        left_ = None if len(left) == 0 else (left[0], left[-1])
        right_ = None if len(right) == 0 else (right[0], right[-1])

        t1, t2 = (None, None) if top_ is None else ((top_[0], a1[0]), (top_[1], a1[0]))
        b1, b2 = (None, None) if bottom_ is None else ((bottom_[0], a1[-1]), (bottom_[1], a1[-1]))
        l1, l2 = (None, None) if left_ is None else ((a0[0], left_[0]), (a0[0], left_[1]))
        r1, r2 = (None, None) if right_ is None else ((a0[-1], right_[0]), (a0[-1], right_[1]))
        return t1, t2, b1, b2, l1, l2, r1, r2








