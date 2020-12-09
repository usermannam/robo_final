import time
import math

class Stage:
    def __init__(self, global_var, message):
        self.gv = global_var
        self.mg = message
        self.p_ = 0
        self.c = False
        self.deflag = False

    # 교차점 매트릭스, 화면 채우는 선 포인트(시작, 끝) 리스트, 원래 선 포인트(시작, 끝) 리스트, 선 기울기 리스트, 선 절편 리스트
    def stage(self, top, bottom, left, right, w_, h_):
        # 직진
        if self.gv.step == 1:
            print(top, bottom, left, right)
            # 끝에 다다르면
            if top[1] is None and h_ is not None:
                if h_ > self.gv.v_c:
                    print("111111")
                    if self.deflag:
                        print("앞으로")
                    else:
                        self.forward()
                    # if left[0] is None or right[0] is None:
                    #     if self.deflag:
                    #         print("앞으로")
                    #     else:
                    #         self.forward()
                    # else:
                    #     if abs(left[0] - right[0]) <= self.gv.e_:
                    #         if self.deflag:
                    #             print("앞으로")
                    #         else:
                    #             self.forward()
                    #     elif left[0] > right[0]:
                    #         if self.deflag:
                    #             print("왼쪽")
                    #         else:
                    #             self.left_turn()
                    #     else:
                    #         if self.deflag:
                    #             print("오른쪽")
                    #         else:
                    #             self.right_turn()

                    self.c = True

            elif self.c and top[1] is None and bottom[1] is None and left[0] is None and right[0] is None:
                if self.deflag:
                    print("22222")
                else:
                    while True:
                        self.up_head()
                        if self.mg.get_up():
                            break
                    self.c = False
                    self.gv.task_step = 2
                    self.gv.step = 2

            else:
                print("33333")
                if w_ - self.gv.e_ <= self.gv.h_c and self.gv.h_c <= w_ + self.gv.e_:
                    if self.deflag:
                        print('그래프 앞으로')
                    else:
                        self.forward()
                elif w_ <= self.gv.h_c:
                    if self.deflag:
                        print('그래프 왼쪽')
                    else:
                        self.left_turn()
                else:
                    if self.deflag:
                        print('그래프 오른쪽')
                    else:
                        self.right_turn()

        # 턴
        elif self.gv.step == 2:
            t_flag = True
            if bottom[1] is not None and top[1] is not None:
                b, t = bottom[1], top[1]
                if bottom[1] > top[1]:
                    b, t = top[1], bottom[1]

                if b - self.gv.e_ <= self.gv.h_c and self.gv.h_c <= t + self.gv.e_:
                    self.gv.step = 1
                    t_flag = False

            # elif w_ is not None and h_ is not None:
            #     if h_ > self.gv.v_c:
            #         if w_ - self.gv.e_ <= self.gv.h_c and self.gv.h_c <= w_ + self.gv.e_:
            #             self.gv.step = 1
            #             t_flag = False

            if t_flag:
                if self.gv.L_R_flag:
                    self.left_turn()
                    pass
                else:
                    self.right_turn()
                    pass

    # 라인 복귀 함수 (중간 부분쯤에서 직선 따라가기)
    def return_line2(self, a0, img):
        h, w = img.shape
        w = w//2
        if a0 - self.gv.e_ <= w and w <= a0 + self.gv.e_:
            if self.deflag:
                print('그래프 앞으로')
            else:
                self.forward()
        elif a0 <= w:
            if self.deflag:
                print('그래프 왼쪽')
            else:
                self.left_turn()
        else:
            if self.deflag:
                print('그래프 오른쪽')
            else:
                self.right_turn()

    # 라인 복귀 함수
    def return_line(self, cx, cy, h, w, head_check=False):
        f = True
        dy = (cy - h)
        dx = (cx - w//2)
        angle = 90
        if dx != 0:
            angle = math.atan(dy / dx) * (180.0 / math.pi)
        if angle < 0:
            angle += 180
        angle -= 90

        if cy > h // 4 * 3:
            self.head_control()
            f = False

        if not head_check:
            if f:
                if -20 <= angle <= 20:
                    # print('앞으로')
                    self.forward()
                elif angle < 0:
                    # print('왼쪽')
                    self.left_turn()
                else:
                    # print('오른쪽')
                    self.right_turn()
        

    def head_control(self):
        if self.gv.head_count == 1:
            while True:
                self.head1()
                if self.mg.get_head1():
                    break
            self.gv.head_count = 2
            print("1 Stage")

        elif self.gv.head_count == 2:
            while True:
                self.head2()
                if self.mg.get_head2():
                    break
            self.gv.head_count = 3
            print("2 Stage")

        elif self.gv.head_count == 3:
            while True:
                self.head3()
                if self.mg.get_head3():
                    break
            self.gv.head_count = 4
            print("3 Stage")

        elif self.gv.head_count == 4:
            while True:
                self.head4()
                if self.mg.get_head4():
                    break
            self.gv.head_count = 5
            print("4 Stage")
            print("Mission Complete!")

    def forward(self):
        self.p_ = 0
        self.mg.TX_append(self.gv.Forward)

    def left_turn_f(self):
        self.mg.TX_append(self.gv.Left_turn)

    def right_turn_f(self):
        self.mg.TX_append(self.gv.Right_turn)

    def left_turn(self):
        self.p_ = 1
        self.mg.TX_append(self.gv.Left_onturn)

    def right_turn(self):
        self.p_ = 2
        self.mg.TX_append(self.gv.Right_onturn)

    def up_head(self):
        self.mg.TX_append(self.gv.up_head)

    def down_head(self):
        self.mg.TX_append(self.gv.down_head)

    def head1(self):
        self.mg.TX_append(self.gv.head1)

    def head2(self):
        self.mg.TX_append(self.gv.head2)

    def head3(self):
        self.mg.TX_append(self.gv.head3)

    def head4(self):
        self.mg.TX_append(self.gv.head4)