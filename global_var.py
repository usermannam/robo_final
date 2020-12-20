import serial

class Global_var:
    def __init__(self):
        self.task_step = 2      # 현재 수행해야 하는 연산
        self.L_R_flag = False   # 왼쪽방향 오른쪽방향 (True: 왼쪽, False: 오른쪽)
        self.exit_flag = True       # 다음에는 나간다는 플래그
        self.door_flag = False      # 문 통과작업 여부(True: 문 통과해야함, False: 문 통과 필요X)
        self.m_count = 0            # 지역 몇 개 통과했는지 --> 3개가 되면 나가기 플래그(exit_flag) True 해야함

        self.serial_use = 1
        self.BPS = 4800  # 4800,9600,14400, 19200,28800, 57600, 115200
        self.serial_port = serial.Serial('/dev/ttyS0', self.BPS, timeout=0.01)
        self.serial_port.flush()  # serial cls
        self.Read_RX = 0
        self.receiving_exit = 1
        self.threading_Time = 0.01

        self.RX = []
        self.TX = {}
        self.TX_old = None
        self.crush = False
        self.delay_num = 0

        # 3. 라인 탐색 --> 상황 단계에 따라서
        self.step = 1

        # 제어 신호들 --- v2
        self.Forward = 33       # 앞으로 이동
        self.Right_turn = 34    # 오른쪽 회전
        self.Left_turn = 35     # 왼쪽 회전
        self.Right_onturn = 36  # 제자리 오른쪽 회전
        self.Left_onturn = 37   # 제자리 왼쪽 회전
        self.down_head = 38     # 머리 최대로 숙이기
        self.up_head = 39       # 머리 초기 상태
        self.head1 = 40         # 머리 1단계 숙이기
        self.head2 = 41         # 머리 2단계 숙이기
        self.head3 = 42         # 머리 3단계 숙이기
        self.head4 = 43         # 머리 4단계 숙이기
        self.head_count = 1     # 머리 숙이기 단계 진행도
        self.phead_count = 1    # 머리 숙이기 단계 진행도

        # 화면 해상도
        self.size_y = 320
        self.size_x = 240

        # 화면 자르기
        self.y1 = 110   # 세로 위에
        self.y2 = 165   # 세로 아래
        self.x1 = 110   # 가로 왼쪽
        self.x2 = 231   # 가로 오른쪽

        # 1. 라인 색_v2 대비효과를 활용한 버전
        # True면 배경이 선보다 밝은 거
        # False면 선이 배경보다 밝은 거
        self.thresh = 100   # S 임계값
        self.thresh_d = 15   # H_down
        self.thresh_u = 30   # H_UP

        # 화면 기준 값
        # self.h_c = self.size_y // 2
        self.h_c = (self.x2 - self.x1) // 2    # 가로 중간값
        self.v_c = (self.y2 - self.y1) // 2    # 세로 중간값

        # 오차 수용도
        self.e_ = 20        # 가로 오차 범위
        self.e_v = 10       # 세로 오차 범위
        self.e_a = 10       # 각도 오차 범위
        self.p_group = 20   # 포인트 그룹화 정도
        self.s_group = 30   # 기울기 그룹화 정도
        self.sb = 20        # 교차점 기울기 기준
