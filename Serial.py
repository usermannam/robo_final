import serial, time

# 통신 클래스
class Message:
    def __init__(self, global_var):
        self.gv = global_var
        self.tx_flag = False
        
    def TX_data_py2(self, ser, one_byte):  # one_byte= 0~255
        ser.write(serial.to_bytes([one_byte]))  # python3

    def RX_data(self, ser):
        if ser.inWaiting() > 0:
            result = ser.read(1)
            self.gv.RX = ord(result)
            return self.gv.RX
        else:
            return 0

    def Receiving(self, ser):
        receiving_exit = 1
        while True:
            if receiving_exit == 0:
                break
            time.sleep(self.gv.threading_Time)
            while ser.inWaiting() > 0:
                self.tx_flag = True
                result = ser.read(1)
                self.RX_append(ord(result))

                # 넘어짐 신호 오면 멈춤
                if 15 in self.gv.RX:
                    self.gv.crush = True
                    self.tx_flag = False
                    continue
                self.gv.crush = False

                # 로봇 움직일 때 이거 키면 동작 수행함.
                self.TX_pop()
                self.tx_flag = False

                # -----  remocon 16 Code  Exit ------
                if self.gv.RX == 16:
                    receiving_exit = 0
                    break
    
    # 대기함수
    def release(self):
        while self.tx_flag:
            pass

    def re_hangul_text(self, cur_TX):
        if cur_TX == 33:
            print("Receive Data : 앞으로 이동 시작")
        elif cur_TX == 34:
            print("Receive Data : 오른쪽 회전")
        elif cur_TX == 35:
            print("Receive Data : 왼쪽 회전")
        elif cur_TX == 36:
            print("Receive Data : 제자리 오른쪽 회전")
        elif cur_TX == 37:
            print("Receive Data : 제자리 왼쪽 회전")
        elif cur_TX == 38:
            print("Receive Data : 머리 최대로 숙이기")
        elif cur_TX == 39:
            print("Receive Data : 머리 초기 상태")
        elif cur_TX == 40:
            print("Receive Data : 정지 신호")
        elif cur_TX == 41:
            print("Receive Data : 머리 숙이기 시작")
        elif cur_TX == 42:
            print("Receive Data : 머리 초기화(올리기) 시작")
        elif cur_TX == 44:
            print("Receive Data : 머리 다 숙임")
        elif cur_TX == 111:
            print("Receive Data : Main")
        elif cur_TX == 200:
            print("Receive Data : Forward_2")
        elif cur_TX == 500:
            print("Receive Data : Forward_5")
        elif cur_TX == 222:
            print("Receive Data : Main_2")
        elif cur_TX == 333:
            print("Receive Data : RX_EXIT")
        elif cur_TX == 1:
            print("Receive Data : 머리 1단계")
        elif cur_TX == 2:
            print("Receive Data : 머리 2단계")
        elif cur_TX == 3:
            print("Receive Data : 머리 3단계")
        elif cur_TX == 4:
            print("Receive Data : 머리 4단계")

    # 가장 최근 신호를 끝에 놓는 함수 --> 한 신호에 대해 무조건 하나만 존재
    def RX_append(self, data):
        # self.re_hangul_text(data)
        if not data in self.gv.RX:
            self.gv.RX.append(data)
        else:
            self.gv.RX.remove(data)
            self.gv.RX.append(data)

    # 머리 올린 신호 왔는지 체크
    def get_up(self):
        self.release()
        if 39 in self.gv.RX:
            self.gv.RX.remove(39)
            return True
        return False

    def get_down(self):
        self.release()
        # print("self.gv.RX: ", self.gv.RX)
        if 38 in self.gv.RX:
            self.gv.RX.remove(38)
            return True
        return False

    def get_left(self):
        self.release()
        # print("self.gv.RX: ", self.gv.RX)
        if 35 in self.gv.RX:
            self.gv.RX.remove(35)
            return True
        return False

    def get_right(self):
        self.release()
        # print("self.gv.RX: ", self.gv.RX)
        if 34 in self.gv.RX:
            self.gv.RX.remove(34)
            return True
        return False

    def get_righton(self):
        self.release()
        # print("self.gv.RX: ", self.gv.RX)
        if 36 in self.gv.RX:
            self.gv.RX.remove(36)
            return True
        return False

    # 가장 최근 신호를 유지하기 위한 함수
    def TX_append(self, data):
        self.release()
        self.gv.TX = []
        self.gv.TX.append(data)

    def hangul_text(self, cur_TX):
        if cur_TX == 33:
            print("Send Data : 앞으로 이동")
        elif cur_TX == 34:
            print("Send Data : 오른쪽 회전")
        elif cur_TX == 35:
            print("Send Data : 왼쪽 회전")
        elif cur_TX == 36:
            print("Send Data : 제자리 오른쪽 회전")
        elif cur_TX == 37:
            print("Send Data : 제자리 왼쪽 회전")
        elif cur_TX == 38:
            print("Send Data : 머리 최대로 숙이기")
        elif cur_TX == 39:
            print("Send Data : 머리 초기 상태")
        elif cur_TX == 40:
            print("Send Data : 정지 신호")


    def max_dic(self, x):
        return self.gv.TX[x]

    # 제어보드에서 신호가 오면 가장 최근 데이터 보내고 전부 pop --> 데이터 보내는 부분
    def TX_pop(self):
        if len(self.gv.TX) != 0:
            # cur_TX = max(self.gv.TX.keys(), key=self.max_dic)
            cur_TX = self.gv.TX[-1]

            self.hangul_text(cur_TX)
            self.TX_data_py2(self.gv.serial_port, cur_TX)
            self.gv.TX_old = cur_TX

        # 초기화
        self.gv.TX = []


