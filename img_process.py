import random

import numpy as np
import cv2
import math
import matplotlib.pyplot as plt

class Img:
    def __init__(self, gv, stage, cap):
        self.gv = gv
        self.st = stage
        self.cap = cap
        self.size_x = self.gv.size_x
        self.size_y = self.gv.size_y
        self.init_ = True
        self.head_term = 0
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
                hue = np.copy(frame[:, :, 0])
                hue[np.logical_and(hue[:, :] > self.gv.thresh_d, hue[:, :] <= self.gv.thresh_u)] = 255
                hue[hue[:, :] < 255] = 0

                gray = np.copy(frame[:, :, 1])
                gray[gray >= self.gv.thresh] = 255
                gray[gray < self.gv.thresh] = 0
                gray = hue & gray

                if self.gv.step == 3:
                    kernel = np.ones((3, 3), np.int8)
                    gray = cv2.erode(gray, kernel, iterations=1)
                    gray = cv2.dilate(gray, kernel, iterations=2)
                    # gray = gray[:]
                    if self.gv.head_count == 0:
                        gray = gray[110:165, 110:231]

                    height, width = gray.shape
                    cx, cy, left_line, right_line = self.hough_line(gray)
                    if cx is not None:
                        cv2.circle(gray, (cx, cy), 20, 200, 5)

                        if self.gv.head_count != self.gv.phead_count:
                            self.head_term = self.head_term + 1
                            if self.head_term >= 10:
                                self.gv.phead_count = self.gv.head_count
                                self.st.return_line(cx, cy, height-1, width)
                                self.head_term = 0

                        # elif self.gv.head_count == 3:
                        #     l_img = self.getline_img(left_line, right_line, gray)


                        elif self.gv.head_count == 0:
                            self.st.forward()

                        else:
                            self.st.return_line(cx, cy, height - 1, width)
                    elif self.gv.head_count == 0:
                        print("REAL_COMPLETE!!")
                        self.st.down_head()

                    cv2.imshow('df', gray)
                    k = cv2.waitKey(1)
                    # esc 키 종료
                    if k == 27:
                        break
                    continue

                kernel = np.ones((3, 3), np.int8)
                gray = cv2.erode(gray, kernel, iterations=2)
                gray = cv2.dilate(gray, kernel, iterations=2)
                gray = gray[110:165, 110:231]

                height, width = gray.shape

                w_c, h_c = self.sum_pixel(gray)

                top = [i for i, g in enumerate(gray[0]) if g == 255]
                bottom = [i for i, g in enumerate(gray[-1]) if g == 255]
                left = [i for i, g in enumerate(gray[:, 0]) if g == 255]
                right = [i for i, g in enumerate(gray[:, -1]) if g == 255]

                top_coordinate = [0, None if len(top) == 0 else top[len(top)//2]]
                bottom_coordinate = [height-1, None if len(bottom) == 0 else bottom[len(bottom) // 2]]
                left_coordinate = [None if len(left) == 0 else left[len(left) // 2], 0]
                right_coordinate = [None if len(right) == 0 else right[len(right) // 2], width-1]

                cv2.imshow('gv', gray)
                cv2.imshow('threshold', gray)

                k = cv2.waitKey(1)
                # esc 키 종료
                if k == 27:
                    break
                try:
                    self.st.stage(top_coordinate, bottom_coordinate, left_coordinate, right_coordinate, w_c, h_c)
                except:
                    input()
                if self.gv.task_step != 1:
                    break
            else:
                print("error")
                break

    def sum_pixel(self, img):
        a0 = np.sum(img, axis=0)    # 가로
        a1 = np.sum(img, axis=1)    # 세로

        a0 = np.where(a0 > 0)[0]
        a1 = np.where(a1 > 0)[0]
        # a0 = np.where(a0 >= np.max(a0))[0]
        # a1 = np.where(a1 >= np.max(a1))[0]

        a0 = None if len(a0) == 0 else a0[len(a0) // 2]
        a1 = None if len(a1) == 0 else a1[len(a1) // 2]

        return a0, a1
    
    # 라인 이미지만 남기기
    def getline_img(self, left_line, right_line, img):
        line_img = np.copy(img)
        line_img[:, :] = 0
        if self.gv.L_R_flag:
            cv2.line(line_img, (left_line[0], left_line[1]), (left_line[2], left_line[3]), 200, 3)
        else:
            cv2.line(line_img, (right_line[0], right_line[1]), (right_line[2], right_line[3]), 200, 3)

        return line_img


    # 허프라인을 이용하여 교차점 찾기 위한 함수
    def hough_line(self, img):
        gause_img = cv2.GaussianBlur(img, (5, 5), 0)
        median_img = cv2.medianBlur(gause_img, 5)
        canny = cv2.Canny(median_img, 5000, 1500, apertureSize = 5, L2gradient = True)
        cv2.imshow('canny', canny)
        '''확률적 허프라인'''
        lines = cv2.HoughLinesP(canny, 0.8, np.pi / 180, 20, minLineLength=10, maxLineGap=100)

        if lines is not None:
            angle_list = np.array([], dtype=np.int64) # 기울기 리스트

            for i in lines:
                cv2.line(img, (i[0][0], i[0][1]), (i[0][2], i[0][3]), 127, 2)
                # 기울기 계산
                dy = (i[0][3] - i[0][1])
                dx = (i[0][2] - i[0][0])
                if dx != 0:
                    angle = math.atan(dy / dx) * (180.0 / math.pi)
                else:
                    angle = 90

                if angle < 0:
                    angle += 180

                angle_list = np.append(angle_list, angle)

            line_p = []
            pass_index = []
            for i, angle in enumerate(angle_list):
                p_flag = False
                for pa in pass_index:
                    if i in pa:
                        p_flag = True
                        break
                if p_flag:
                    continue
                low = angle - self.gv.s_group
                high = angle + self.gv.s_group

                p_i = np.where(
                    np.logical_and(angle - self.gv.s_group <= angle_list, angle_list <= angle + self.gv.s_group))
                if low < 0 or high > 180:
                    if low < 0:
                        low = 180 + low
                    elif high > 180:
                        high %= 180
                    p_i = np.where(np.logical_or(angle_list <= high, low <= angle_list))

                pass_index.append(list(p_i)[0])

                x = lines[i][0]
                points = self.long_line(x[0], x[1], x[2], x[3], img) # 기울기와 절편 구하기
                cv2.line(img, (points[0], points[1]), (points[2], points[3]), 200, 3)
                line_p.append((points, i))

            cx_list, cy_list = [], []
            line1_list, line2_list = [], []
            coner_flag = False
            # 교차점 찾아보자
            if len(line_p) >= 2:
                for i, p1 in enumerate(line_p):
                    i1 = p1[1]
                    p1 = p1[0]
                    for p2 in line_p[i+1:]:
                        i2 = p2[1]
                        p2 = p2[0]
                        cx, cy = self.get_crosspt(p1[0], p1[1], p1[2], p1[3], p2[0], p2[1], p2[2], p2[3])
                        if cx is None:
                            continue
                        else:
                            s1 = self.cross_slope(cx, cy, lines[i1][0])
                            s2 = self.cross_slope(cx, cy, lines[i2][0])
                            if s1 < self.gv.sb and s2 < self.gv.sb:
                                continue
                            else:
                                cx_list.append(cx)
                                cy_list.append(cy)
                                line1_list.append(lines[i1][0])
                                line2_list.append(lines[i2][0])
                                coner_flag = True

            if coner_flag:
                if len(cx_list) > 1:
                    min_y, index = cy_list[0], 0
                    for i, y in cy_list:
                        if min_y < y:
                            min_y = y
                            index = i
                    cx_list, cy_list = cx_list[index], cy_list[index]
                    line1_list, line2_list = line1_list[index], line2_list[index]
                else:
                    cx_list, cy_list = cx_list[0], cy_list[0]
                    line1_list, line2_list = line1_list[0], line2_list[0]

                left_line, right_line = self.r_l_line(line1_list, line2_list)
                return int(cx_list), int(cy_list), left_line, right_line

            else:
                return None, None, None, None

        return None, None, None, None

    # 왼쪽선 오른쪽선 구분
    def r_l_line(self, l1, l2):
        l1_c = (l1[0] + l1[2])//2
        l2_c = (l2[0] + l2[2])//2

        left_line, right_line = l1, l2
        if l1_c > l2_c:
            left_line, right_line = l2, l1

        return left_line, right_line

    # 교차점에서 하단 점의 기울기:
    def cross_slope(self, cx, cy, line):
        x, y = (line[0]+line[2])//2, (line[1]+line[3])//2

        # 기울기 계산
        dy = (y - cy)
        dx = (x - cx)
        if dx != 0:
            angle = math.atan(dy / dx) * (180.0 / math.pi)
        else:
            angle = 90
        if angle < 0:
            angle += 180
        if cy < y:
            angle = -angle

        return angle

    # 코너점 검출
    def get_crosspt(self, x11, y11, x12, y12, x21, y21, x22, y22):
        if x12 == x11 or x22 == x21:
            if x12 == x11:
                cx = x12
                m2 = (y22 - y21) / (x22 - x21)
                cy = m2 * (cx - x21) + y21
                return cx, cy
            if x22 == x21:
                cx = x22
                m1 = (y12 - y11) / (x12 - x11)
                cy = m1 * (cx - x11) + y11
                return cx, cy

        m1 = (y12 - y11) / (x12 - x11)
        m2 = (y22 - y21) / (x22 - x21)

        if m1 == m2:
            return None, None

        cx = (x11 * m1 - y11 - x21 * m2 + y21) / (m1 - m2)
        cy = m1 * (cx - x11) + y11

        return cx, cy
    
    # 대표선 추출
    def long_line(self, x1, y1, x2, y2, img):
        h, w = img.shape
        m, b = None, None
        x1_, y1_, x2_, y2_= 0, 0, w-1, h-1
        if x2 != x1:
            m = (y2 - y1)/(x2 - x1)
            b = y1 - (m * x1)
            # 가로
            if m <= h/w:
                y1_ = m*x1_ + b
                y2_ = m*x2_ + b
            # 세로
            else:
                x1_ = (y1_ - b) / m
                x2_ = (y2_ - b) / m

        else:
            x1_, x2_ = x1, x2

        result = (int(x1_), int(y1_), int(x2_), int(y2_))
        return result