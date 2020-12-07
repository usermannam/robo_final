import time
import math

class Stage:
    def __init__(self, global_var, message):
        self.gv = global_var
        self.mg = message
        self.p_ = 0
        self.c = False

    # 교차점 매트릭스, 화면 채우는 선 포인트(시작, 끝) 리스트, 원래 선 포인트(시작, 끝) 리스트, 선 기울기 리스트, 선 절편 리스트
    def stage(self, top, bottom, left, right, w_, h_):
        # 직진
        if self.gv.step == 1:
            print(top, bottom, left, right)
            # 끝에 다다르면
            if top[1] is None and h_ is not None:
                if h_ > self.gv.v_c:
                    print("11111")
                    if left[0] is None or right[0] is None:
                        self.forward()
                    else:
                        if abs(left[0] - right[0]) <= self.gv.e_:
                            self.forward()
                        elif left[0] > right[0]:
                            self.left_turn()
                        else:
                            self.right_turn()

                    self.c = True

            elif self.c and top[1] is None and bottom[1] is None and left[0] is None and right[0] is None:
                print("22222")
                while True:
                    self.up_head()
                    if self.mg.get_up():
                        break
                self.c = False
                self.gv.task_step = 2
                self.gv.step = 2

            else:
                print("33333")
                if bottom[1] is not None and top[1] is not None:
                    # 하단 위치 맞는지
                    if bottom[1] - self.gv.e_ <= self.gv.h_c and self.gv.h_c <= bottom[1] + self.gv.e_:
                        dy = (top[1] - bottom[1])
                        dx = (top[0] - bottom[0])
                        if dx != 0:
                            angle = math.atan(dy / dx) * (180.0 / math.pi)
                        else:
                            angle = 180

                        if dx < 0:
                            angle += 180
                        angle -= 180

                        if angle <= 10:
                            self.forward()
                        elif angle > 0:
                            self.left_turn()
                        else:
                            self.right_turn()

                    else:
                        if bottom[1] < self.gv.h_c:
                            if bottom[1] <= self.gv.h_c and self.gv.h_c <= top[1]:
                                self.forward()
                            else:
                                self.left_turn()

                        else:
                            if top[1] <= self.gv.h_c and self.gv.h_c <= bottom[1]:
                                self.forward()
                            else:
                                self.right_turn()
                else:
                    if w_ - self.gv.e_ <= self.gv.h_c and self.gv.h_c <= w_ + self.gv.e_:
                        self.forward()
                    elif w_ <= self.gv.h_c:
                        self.left_turn()
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

            elif w_ is not None:
                if w_ - self.gv.e_ <= self.gv.h_c and self.gv.h_c <= w_ + self.gv.e_:
                    self.gv.step = 1
                    t_flag = False

            if t_flag:
                if self.gv.L_R_flag:
                    self.left_turn()
                    pass
                else:
                    self.right_turn()
                    pass
        
        # 라인복귀
        # elif self.gv.step == 3:



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