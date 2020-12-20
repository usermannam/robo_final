# -*-coding:utf-8-*-
import cv2
import platform
import sys
import serial
import time
from threading import Thread

from global_var import Global_var
from Serial import Message
from img_process import Img
from Stage_decision import Stage

if __name__ == '__main__':
    # cap = None
    print("-------------------------------------")
    print("---- (2020-1-20)  MINIROBOT Corp. ---")
    print("-------------------------------------")

    os_version = platform.platform()
    print(" ---> OS " + os_version)
    python_version = ".".join(map(str, sys.version_info[:3]))
    print(" ---> Python " + python_version)
    opencv_version = cv2.__version__
    print(" ---> OpenCV  " + opencv_version)
    print("-------------------------------------")

    W_View_size = 320  # 320  #640
    H_View_size = 240

    cap = cv2.VideoCapture(0)
    cap.set(3, W_View_size)
    cap.set(4, H_View_size)

    BPS = 4800  # 4800,9600,14400, 19200,28800, 57600, 115200

    # ---------local Serial Port : ttyS0 --------
    # ---------USB Serial Port : ttyAMA0 --------

    # serial_port = serial.Serial('/dev/ttyS0', BPS, timeout=0.01)
    # serial_port.flush()  # serial cls

    # --------------------------- 통신 설정 끝

    gv = Global_var()
    mg = Message(gv)
    st = Stage(gv, mg)
    lp = Img(gv, st, mg, cap)
    # at = Action(gv)

    # lp.var_init(sd)
    # at.var_init(mg)

    serial_t = Thread(target=mg.Receiving, args=(gv.serial_port,))
    serial_t.daemon = True
    serial_t.start()
    time.sleep(0.1)
    # ---------------------------
    # First -> Start Code Send
    mg.TX_data_py2(gv.serial_port, 128)
    time.sleep(1)
    i = 0
    while True:
        if gv.task_step == 1:
            while True:
                if gv.step != 3:    # 라인 복귀가 아니라면 머리 박기
                    mg.TX_append(gv.down_head)
                    if mg.get_down():
                        time.sleep(0.5)
                        break
                else:               # 라인 복귀라면 머리 들기
                    mg.TX_append(gv.up_head)
                    if mg.get_up():
                        time.sleep(0.5)
                        break
                        
            lp.img_process()

        elif gv.task_step == 2:
            while True:
                mg.TX_append(gv.up_head)
                if mg.get_up():
                    break
            ''' 화면 인식, 
            화면 인식 후에 어떤 작업해야하는지 상황에 따라 task_step값 변경 필요
             예를 들어 동서남북 인식후에는 문 통과
             ABCD 인식후에는 물체탐지작업 필요'''
            
            ''' 또한 이동 step 결정 필요..
            화살표 다음에는 step = 2
            ABCD 다름에는 step = 3'''
            i += 1
            print("화면 인식 시작")
            time.sleep(0.5)
            print("화면 인식 끝")
            
        elif gv.task_step == 3:
            '''물체탐지 및 물체 옮기기'''
            '''끝나고 task_step = 1로 변경 step = 3으로 변경'''
            pass

        elif gv.task_step == 4:
            '''문 통과 모션'''
            '''끝나고 task_step = 1로 변경 step = 1로 변경'''
            pass

        # 나가기 플래그 True이면 step == 4로 변경
        if gv.exit_flag:
            gv.step = 4
            gv.door_flag = True