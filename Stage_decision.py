import time
import math

class Stage:
    def __init__(self, global_var, message):
        self.gv = global_var
        self.mg = message
        self.c = False
        self.c2 = False
        self.deflag = False
        self.re_b = (self.gv.size_x - self.gv.y2) / (self.gv.y2 - self.gv.y1)

    # 교차점 매트릭스, 화면 채우는 선 포인트(시작, 끝) 리스트, 원래 선 포인트(시작, 끝) 리스트, 선 기울기 리스트, 선 절편 리스트
    def stage(self, top, bottom, left, right, w_, h_):
        # 직진 & 회전플레그 --> 나가기 단계에서는 사용 X
        if self.gv.step == 1:
            # 끝에 다다르면
            if top[1] is None and h_ is not None:
                if h_ > self.gv.v_c:
                    if self.deflag:
                        print("앞으로")
                    else:
                        self.forward()

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
                if top[1] is not None and bottom[1] is not None:
                    bottom[1] = bottom[1] - ((top[1] - bottom[1]) * self.re_b)
                    if bottom[1] - self.gv.e_ <= self.gv.h_c and self.gv.h_c <= bottom[1] + self.gv.e_:
                        b, t = bottom[1], top[1]
                        if bottom[1] > top[1]:
                            b, t = top[1], bottom[1]
                        # 제자리에 있지만 선이 중심을 가로지른다면 그냥 앞으로
                        if b <= self.gv.h_c and self.gv.h_c <= t:
                            self.forward()
                        # 제자리에 있지만 가로지르지 않는다면 각도에 따라서..
                        else:
                            dy = (top[1] - bottom[1])
                            dx = (top[0] - bottom[0])
                            angle = 0
                            if dx != 0:
                                angle = math.atan(dy / dx) * (180.0 / math.pi)

                            if -self.gv.e_a <= angle <= self.gv.e_a:
                                self.forward()
                            elif angle > 0:
                                self.left_turn()
                            else:
                                self.right_turn()

                    else:
                        b, t = bottom[1], top[1]
                        if bottom[1] > top[1]:
                            b, t = top[1], bottom[1]
                        if b <= self.gv.h_c and self.gv.h_c <= t:
                            self.forward()
                        elif b < self.gv.h_c:
                            self.left_turn()
                        else:
                            self.right_turn()

                elif w_ - self.gv.e_ <= self.gv.h_c and self.gv.h_c <= w_ + self.gv.e_:
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

        # 턴 --> 맨 처음과 나갈 때
        elif self.gv.step == 2:
            t_flag = True
            if bottom[1] is not None and top[1] is not None:
                b, t = bottom[1], top[1]
                if bottom[1] > top[1]:
                    b, t = top[1], bottom[1]

                if b - self.gv.e_ <= self.gv.h_c and self.gv.h_c <= t + self.gv.e_:
                    self.gv.step = 1
                    t_flag = False

            elif w_ is not None and h_ is not None:
                if self.gv.v_c - self.gv.e_v <= h_ and h_ <= self.gv.v_c + self.gv.e_v:
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
        
        # 나갈때
        elif self.gv.step == 4:
            if self.gv.L_R_flag and left[0] is not None and top[1] is not None:
                if left[0] >= self.gv.v_c and w_ < self.gv.h_c:
                    print("111111")
                    if self.deflag:
                        print("앞으로")
                    else:
                        self.forward()
                    self.c = True

            elif not self.gv.L_R_flag and right[0] is not None and top[1] is not None:
                if right[0] >= self.gv.v_c and w_ > self.gv.h_c:
                    print("111111")
                    if self.deflag:
                        print("앞으로")
                    else:
                        self.forward()
                    self.c = True

            # 여기서 회전을 주고 None이 아니면 위의 턴(self.gv.step == 2)로 가서 턴 돌다가 다 돌았다는 신호오면
            # 고개들어서 앞의 글자 확인하고 다시 와서 고개 숙이고 앞으로 직진하다가 앞의 직선 사라지면 거기에서 문 열기위한 동작으로 이동
            # 위의 글을 바로 밑의 코드에 적용해야함..
            if self.c and left[0] is None and right[0] is None:
                if self.gv.L_R_flag and left[0] >= self.gv.v_c:
                    self.left_turn()
                    self.c2 = True
                elif not self.gv.L_R_flag and right[0] >= self.gv.v_c:
                    self.right_turn()
                    self.c2 = True

            elif self.c2:
                print("444444")
                self.c = False
                t_flag = True
                if bottom[1] is not None and top[1] is not None:
                    b, t = bottom[1], top[1]
                    if bottom[1] > top[1]:
                        b, t = top[1], bottom[1]

                    if b - self.gv.e_ <= self.gv.h_c and self.gv.h_c <= t + self.gv.e_:
                        self.c2 = False
                        t_flag = False
                        print("일단 완료")
                        time.sleep(30)

                elif w_ is not None and h_ is not None:
                    if self.gv.v_c - self.gv.e_v <= h_ and h_ <= self.gv.v_c + self.gv.e_v:
                        if w_ - self.gv.e_ <= self.gv.h_c and self.gv.h_c <= w_ + self.gv.e_:
                            self.c2 = False
                            t_flag = False
                            print("일단 완료 1111")
                            time.sleep(30)

                if t_flag:
                    if self.gv.L_R_flag:
                        self.left_turn()
                    else:
                        self.right_turn()

            if not self.c and not self.c2:
                print("33333")
                if top[1] is not None and bottom[1] is not None:
                    bottom[1] = bottom[1] - ((top[1] - bottom[1]) * self.re_b)
                    if bottom[1] - self.gv.e_ <= self.gv.h_c and self.gv.h_c <= bottom[1] + self.gv.e_:
                        b, t = bottom[1], top[1]
                        if bottom[1] > top[1]:
                            b, t = top[1], bottom[1]
                        # 제자리에 있지만 선이 중심을 가로지른다면 그냥 앞으로
                        if b <= self.gv.h_c and self.gv.h_c <= t:
                            self.forward()
                        # 제자리에 있지만 가로지르지 않는다면 각도에 따라서..
                        else:
                            dy = (top[1] - bottom[1])
                            dx = (top[0] - bottom[0])
                            angle = 0
                            if dx != 0:
                                angle = math.atan(dy / dx) * (180.0 / math.pi)

                            if -self.gv.e_a <= angle <= self.gv.e_a:
                                self.forward()
                            elif angle > 0:
                                self.left_turn()
                            else:
                                self.right_turn()

                    else:
                        b, t = bottom[1], top[1]
                        if bottom[1] > top[1]:
                            b, t = top[1], bottom[1]
                        if b <= self.gv.h_c and self.gv.h_c <= t:
                            self.forward()
                        elif b < self.gv.h_c:
                            self.left_turn()
                        else:
                            self.right_turn()

                elif w_ - self.gv.e_ <= self.gv.h_c and self.gv.h_c <= w_ + self.gv.e_:
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
        h = h // 4 * 3
        w = w // 2
        if cy > h:
            self.head_control()
            f = False

        if not head_check:
            if f:
                if cx - self.gv.e_ <= w and w <= cx + self.gv.e_:
                    self.forward()
                elif cx < w:
                    self.left_turn()
                else:
                    self.right_turn()

    # 머리 한 단계씩 낮추기
    def head_control(self):
        if self.gv.head_count == 1:
            while True:
                self.head1()
                if self.mg.get_head1():
                    break
            self.gv.head_count = 2

        elif self.gv.head_count == 2:
            while True:
                self.head2()
                if self.mg.get_head2():
                    break
            self.gv.head_count = 3

        elif self.gv.head_count == 3:
            while True:
                self.head3()
                if self.mg.get_head3():
                    break
            self.gv.head_count = 4

        elif self.gv.head_count == 4:
            while True:
                self.head4()
                if self.mg.get_head4():
                    break
            self.gv.head_count = 5

    def forward(self):
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