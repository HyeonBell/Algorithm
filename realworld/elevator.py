'''
    Made by hyeonbell 2021.06.29

    This program is had copied elevator algorithm.

    I'm add several debug information on running program like: where am I?, elevator direction, current floor etc.

    One thing special is when you call elevator with pushing up or down button, the program show you emoji that how long you wait time for take elevator.

    Anyway, a lot of mistake or missing coding can be had in program. plz look at me with kindness. Thank you guys.

'''


import random
from threading import Thread
import os
from time import sleep
import traceback

global global_menu_thread


def global_debugging():
    print("오류 입니다 : " + str(traceback.print_stack()))

class Menu:
    def __init__(self):
        self.choice = """
        1. 엘레베이터 가동
        2. 종료
        """

    def show_menu(self):
        print("\n" + self.choice)


class Elevator:
    def __init__(self):
        self.calling_floor = 0
        self.current_floors = 0
        self.current_destination = None
        self.called_floors_list = list()
        self.max_floors = 24  # 건물 높이 (조정)
        self.init_max_count = None
        self.current_direction = None
        self.time = None
        self.max_people = 20  # 최대 인원 (조정)
        self.current_people = None
        self.stop_delay = 2
        self.move_delay = 2
        self.time_delay_per_people_count = 1
        self.time_increase_value = 1
        self.call_count = None
        self.face_state = 0  # 0, 1, 2
        self.state_face = [":D", ":)", ":("]  # 0, 1, 2
        self.state_2 = ["빠름", "보통", "혼잡"]
        self.standard_called = [3, 7]  # 함박 웃음, 웃는 얼굴, 우는 얼굴 (조정)
        self.direction_display = [" ", " "]
        self.up = "↑"
        self.down = "↓"
        self.sub_menu = ""
        self.padding_switch = 0
        self.floor_padding_switch = 0
        self.display_padding = ["  ", " "]

        self.up_button_switch = 0
        self.down_button_switch = 0
        self.up_button = ["△", "▲"]
        self.down_button = ["▽", "▼"]

        self.move_switch = 0
        self.move_thread = None

        self.stop_switch = 0
        self.stop_thread = None

        self.direction_priority_queue = list()
        self.up_calling_queue = list()
        self.down_calling_queue = list()


        self.total_call_count = 0
        self.total_call_list = list()

    def init_elevator(self):
        self.called_floors_list.clear()
        self.up_calling_queue.clear()
        self.down_calling_queue.clear()
        self.direction_priority_queue.clear()
        self.up_button_switch = 0
        self.down_button_switch = 0
        self.calling_floor = random.randrange(1,21) # 탈 사람 층
        self.current_people = random.randrange(0, 21)  # 0부터 20명의 초기 인원
        self.init_floor_and_direction()
        self.init_destination()
        self.init_call_count()
        self.init_called_floors()

    def init_floor_and_direction(self):
        self.current_floors = random.randrange(1, self.max_floors + 1)  # 1층부터 20층 까지 있는 건물
        if self.current_floors == self.max_floors:
            self.current_direction = "down"
        elif self.current_floors == 1:
            self.current_direction = "up"
        else:
            self.current_direction = "up" if random.randrange(0, 2) else "down"

    def init_destination(self):
        if self.current_direction == "up":
            if self.current_floors != self.max_floors:
                self.current_destination = random.randrange(self.current_floors+1, self.max_floors+1)  # 현재 층에 +1 부터 최대 층 수 까지의 범위

        if self.current_direction == "down":
            if self.current_floors != 1:
                self.current_destination = random.randrange(1, self.current_floors)  # 1층부터 현재 층 수-1 까지
        self.called_floors_list.append(self.current_destination)

    def init_call_count(self):
        if self.current_direction == "up":
            if self.max_floors == self.current_destination:
                self.init_max_count = self.max_floors - self.current_floors  # 도착지가 최대층 이면
            elif self.max_floors > self.current_destination:
                self.init_max_count = self.current_destination - self.current_floors  # 도착지가 최대 층 수보다 작으면 도착지 층 수만큼 호출 가능
        elif self.current_direction == "down":
            if self.current_destination == 1 and self.current_floors != 2:
                self.init_max_count = self.current_floors  # 도착지가 1층이면 현재 층수 만큼 호출 가능
            elif self.current_destination > 1 or (self.current_floors == 2 and self.current_destination == 1):
                self.init_max_count = self.current_floors - self.current_destination
        else:
            global_debugging()
        self.init_max_count -= 1

    def init_called_floors(self):
        if self.init_max_count == 0:
            return 0
        else:
            for i in range(0, self.init_max_count):
                if random.randrange(1, 101) <= 50:  # 100번의 경우중 절반은 타고 절반은 안탈꺼다.
                    if self.current_direction == "up" and self.init_max_count != 0:
                        self.called_floors_list.append(random.randrange(self.current_floors+1, self.current_destination))  # 자신 층 수 제외하고 호출 스택 쌓기
                    elif self.current_direction == "down" and self.init_max_count != 0:
                        self.called_floors_list.append(random.randrange(self.current_destination+1, self.current_floors))  # 자신 층 수 제외하고 호출 스택 쌓기
                    else:
                        global_debugging()
        self.called_floors_list.append(self.current_destination)
        self.called_floors_list = list(set(self.called_floors_list))  # 중복 제거

    @staticmethod
    def check_menu_alive():
        global global_menu_thread

        if global_menu_thread.is_alive():
            return 1
        else:
            return 0

    # 어떻게 하다보니 메뉴도 같이 display하는 로직
    def run_elevator(self):
        os.system("cls > nul")
        while True:
            if self.check_menu_alive() == 0:
                break
            else:
                self.update_display_button()
                self.update_display()
                self.show_display()


                print("탑승 인원 :" + str(self.current_people))
                print("건물 높이 : " + str(self.max_floors))
                print("현재 엘리베이터 방향 : " + self.current_direction)
                print("초기 호출 가능 수 : " + str(self.init_max_count))
                print("운행 할 층 수 : " + str(self.called_floors_list.__len__()))
                print("방향 우선 순위 큐 : "  + str(self.direction_priority_queue))

                print("현재 층 : " + str(self.calling_floor))
                print("현재 엘레베이터 위치 : " + str(self.current_floors) + " ->  마지막 목적지 : " + str(self.current_destination))
                print("눌러진 층 : " + str(self.called_floors_list))
                print("up 큐 : " + str(self.up_calling_queue))
                print("down 큐 :" + str(self.down_calling_queue))

                sleep(1)
                os.system("cls > nul")

                # 동작
                self.check_arrived_destination()
                self.check_limited_floor_condition()
                self.check_move_behavior()
                self.check_calling_queue()
                self.check_direction_priority()
                self.check_stop()
                self.random_calling_encounter()
                self.update_current_destination()
                self.assemble_total_call_count()

    def assemble_total_call_count(self):
        self.total_call_count = 0
        if self.up_button_switch == 1:
            if self.current_direction == "up":
                if self.current_floors < self.calling_floor:
                    for floor in self.called_floors_list:
                        if self.calling_floor > floor:
                            self.total_call_count +=1
                elif self.current_floors > self.calling_floor:
                    self.total_call_count = self.called_floors_list.__len__() + self.down_calling_queue.__len__()
                    for floor in self.up_calling_queue:
                        if self.calling_floor > floor:
                            self.total_call_count += 1
                elif self.current_floors == self.calling_floor:
                    self.total_call_count = 0
                else:
                    global_debugging()

            elif self.current_direction == "down":
                if self.current_floors <= self.calling_floor:
                    self.total_call_count = self.called_floors_list.__len__()
                    for floor in self.up_calling_queue:
                        if self.calling_floor >= floor:
                            self.total_call_count += 1
                elif self.current_floors > self.calling_floor:
                    if self.calling_floor > min(self.called_floors_list):
                        for floor in self.called_floors_list:
                            if self.calling_floor > floor:
                                self.total_call_count += 1
                    else:
                        self.total_call_count = self.called_floors_list.__len__()

            elif self.current_direction == "stop":
                self.total_call_count = 0
        elif self.down_button_switch == 1:
            if self.current_destination == "up":
                if self.current_floors < self.calling_floor:
                    if self.calling_floor < max(self.called_floors_list):
                        for floor in self.called_floors_list:
                            if self.calling_floor < floor:
                                self.total_call_count += 1
                    else:
                        self.total_call_count = self.called_floors_list.__len__()
                    for floor in self.down_calling_queue:
                        if self.calling_floor < floor:
                            self.total_call_count += 1

                elif self.current_floors >= self.calling_floor:
                    self.total_call_count = self.called_floors_list.__len__()
                    for floor in self.down_calling_queue:
                        if self.calling_floor <= floor:
                            self.total_call_count += 1
                else:
                    global_debugging()

            elif self.current_direction == "down":
                if self.current_floors < self.calling_floor:
                    for floor in self.called_floors_list:
                        if self.calling_floor > floor:
                            self.total_call_count += 1

                elif self.current_floors > self.calling_floor:
                    self.total_call_count = self.called_floors_list.__len__() + self.up_calling_queue.__len__()
                    for floor in self.down_calling_queue:
                        if self.calling_floor > floor:
                            self.total_call_count += 1

                elif self.current_floors == self.calling_floor:
                    self.total_call_count = 0
            elif self.current_direction == "stop":
                self.total_call_count = 0


    def update_current_destination(self):
        if self.current_direction == "up":
            if self.called_floors_list:
                self.current_destination = max(self.called_floors_list)
            elif not self.called_floors_list:
                pass
            else:
                global_debugging()
        elif self.current_direction == "down":
            if self.called_floors_list:
                self.current_destination = min(self.called_floors_list)
            elif not self.called_floors_list:
                pass
            else:
                global_debugging()
        elif self.current_direction == "stop":
            pass
        else:
            global_debugging()

    def random_calling_encounter(self):
        random_value = random.randrange(1, 201)
        random_base = 20
        if 1 <= random_value < random_base * 1:
            if self.current_direction == "up":
                if self.current_floors != self.max_floors:
                    random_calling = random.randrange(self.current_floors+1,
                                                      self.max_floors+1)  # 현재 엘레베이터의 층 +1 에서 최상층까지 랜덤으로 호출
                    self.called_floors_list.append(random_calling)
                else:
                    # 최상층
                    pass
            elif self.current_direction == "down":
                if self.current_floors != 1:
                    random_calling = random.randrange(1, self.current_floors)
                    self.called_floors_list.append(random_calling)
                else:
                    # 최하층
                    pass

            elif self.current_direction == "stop":
                if self.current_floors != 1 and self.current_floors != self.max_floors:
                    random_calling = random.randrange(1, self.max_floors)
                    self.called_floors_list.append(random_calling)
                else:
                    global_debugging()
            else:
                global_debugging()

        elif random_base * 1 <= random_value < random_base * 2:
            if self.current_direction == "up":
                if self.current_floors != 1:
                    if self.current_floors != self.max_floors:
                        random_calling = random.randrange(2, self.current_floors+1)
                        self.down_calling_queue.append(random_calling)
                        self.direction_priority_queue.append("down")
                else:
                    # 최하층
                    pass
            elif self.current_direction == "down":
                if self.current_floors != self.max_floors:
                    random_calling = random.randrange(self.current_floors,
                                                      self.max_floors)  # 현재 엘레베이터의 층 +1 에서 최상층까지 랜덤으로 호출
                    self.up_calling_queue.append(random_calling)
                    self.direction_priority_queue.append("up")
                else:
                    # 최상층
                    pass
            elif self.current_direction == "stop":
                if self.current_floors != 1 and self.current_floors != self.max_floors:
                    random_calling = random.randrange(1, self.max_floors)
                    self.up_calling_queue.append(random_calling)
                    self.direction_priority_queue.append("up")
                else:
                    global_debugging()
            else:
                global_debugging()
        elif random_base * 2 <= random_value < random_base * 3:
            if self.current_direction == "up":
                if self.current_floors != 1:
                    random_calling = random.randrange(1, self.current_floors)
                    self.up_calling_queue.append(random_calling)
                    self.direction_priority_queue.append("up")
                else:
                    # 최하층
                    pass
            elif self.current_direction == "down":
                if self.current_floors != self.max_floors:
                    random_calling = random.randrange(self.current_floors,
                                                      self.max_floors + 1)  # 현재 엘레베이터의 층 +1 에서 최상층까지 랜덤으로 호출
                    self.down_calling_queue.append(random_calling)
                    self.direction_priority_queue.append("down")
                else:
                    # 최상층
                    pass
            elif self.current_direction == "stop":
                if self.current_floors != 1 and self.current_floors != self.max_floors:
                    random_calling = random.randrange(2, self.max_floors+1)
                    self.down_calling_queue.append(random_calling)
                    self.direction_priority_queue.append("down")
                else:
                    global_debugging()
            else:
                global_debugging()
        elif random_base * 3 <= random_value <= 200:
            # 아무 일도 안일어남
            pass
        else:
            global_debugging()

    # move_elevator 부분
    def check_move_behavior(self):
        if self.current_direction == "stop":
            return 0
        else:
            if self.move_switch == 0 and self.stop_switch == 0:
                move_thread = Thread(target=self.move_elevator)
                self.move_thread = move_thread
                self.move_switch = 1
                move_thread.start()
            elif self.move_switch == 1 and self.stop_switch == 0:
                if self.move_thread.is_alive():
                    return 0
                else:
                    self.move_switch = 0

    def async_menu(self):
        while True:
            command = input()
            if command == "exit":
                print("종료.")
                return 0
            elif command == "1":
                print("위로 가는 엘레베이터 호출")
                self.update_button("up")
            elif command == "2":
                print("아래로 가는 엘레베이터 호출")
                self.update_button("down")
            else:
                print("입력 받은 값 : " + command)

    def show_display(self):
        print(self.sub_menu)

    def update_display(self):
        self.check_destination()
        self.check_display_direction()
        self.check_display_floor()
        self.check_display_face_state()
        #callcount = str(self.called_floors_list.__len__())
        callcount_padding = "  "
        if self.total_call_count >= 10:
            callcount_padding = " "
        stop_padding = ""
        if self.current_direction == "stop":
            stop_padding = " "
        if self.up_button_switch == 1 and self.down_button_switch == 0 or self.down_button_switch == 1 and self.up_button_switch == 0:
            self.sub_menu = """
    ┌────────────┬────────────┬───────────────────────────────────┐
    │            │ """+self.direction_display[0]+"  "+str(self.current_floors)+self.display_padding[self.padding_switch]+self.direction_display[1]+" "+self.state_face[self.face_state]+stop_padding+"""│                                   │
    │            └────────────┘         현재 호출 수 : """+str(self.total_call_count)+callcount_padding+"""        │
    │                                                             │
    │                 """+str(self.calling_floor)+self.display_padding[self.floor_padding_switch]+"""                                         │
    │             ┌───┬───┐                                       │
    │             │   │   │                                       │
    │             │   │   │                                       │
    └─────────────┴───┴───┴───────────────────────────────────────┘
    1.버튼"""+self.up_button[self.up_button_switch]+"""
    2.버튼"""+self.down_button[self.down_button_switch]+"""
        """
        else:
            self.sub_menu = """
    ┌────────────┬────────────┬───────────────────────────────────┐
    │            │ """+self.direction_display[0]+"  "+str(self.current_floors)+self.display_padding[self.padding_switch]+self.direction_display[1]+"   "+stop_padding+"""│                                   │
    │            └────────────┘                                   │
    │                                                             │ 
    │                 """+str(self.calling_floor)+self.display_padding[self.floor_padding_switch]+"""                                         │ 
    │             ┌───┬───┐                                       │ 
    │             │   │   │                                       │              
    │             │   │   │                                       │  
    └─────────────┴───┴───┴───────────────────────────────────────┘
    1.버튼"""+self.up_button[self.up_button_switch]+"""
    2.버튼"""+self.down_button[self.down_button_switch]+"""
            """

    def update_display_button(self):
        if self.stop_switch == 1 and self.calling_floor == self.current_floors:
            if self.current_direction == "up":
                self.up_button_switch = 0
            elif self.current_direction == "down":
                self.down_button_switch = 0
            elif self.current_floors == "stop":
                self.down_button_switch = 0
                self.up_button_switch = 0
            else:
                global_debugging()
        else:
            return 0

    def check_stop(self):
        if self.current_direction == "stop":
            if self.direction_priority_queue:
                if not self.called_floors_list:
                    if self.direction_priority_queue[0] == "up":
                        if self.current_floors > min(self.up_calling_queue):
                            tmp = list()
                            tmp2 = list()
                            for floor in self.up_calling_queue:
                                if self.current_floors > floor:
                                    tmp2.append(floor)
                                else:
                                    tmp.append(floor)
                            self.current_direction = "down"
                            self.called_floors_list = tmp2
                            self.current_destination = min(tmp2)
                            self.up_calling_queue = tmp
                        else:
                            self.current_direction = "up"
                            self.called_floors_list = self.up_calling_queue
                            self.current_destination = max(self.up_calling_queue)
                            self.up_calling_queue = list()
                            self.direction_priority_queue.remove("up")

                    elif self.direction_priority_queue[0] == "down":
                        if self.current_floors < max(self.down_calling_queue):
                            tmp = list()
                            tmp2 = list()
                            for floor in self.down_calling_queue:
                                if self.current_floors < floor:
                                    tmp2.append(floor)
                                else:
                                    tmp.append(floor)
                            self.current_direction = "up"
                            self.called_floors_list = tmp2
                            self.current_destination = max(tmp2)
                            self.down_calling_queue = tmp
                        else:
                            self.current_direction = "down"
                            self.called_floors_list = self.down_calling_queue
                            self.current_destination = min(self.down_calling_queue)
                            self.down_calling_queue = list()
                            self.direction_priority_queue.remove("down")
                    else:
                        pass
            else:
                pass
        else:
            return 0

    def check_calling_queue(self):
        # for unique
        self.up_calling_queue = list(set(self.up_calling_queue))
        self.down_calling_queue = list(set(self.down_calling_queue))

    def check_direction_priority(self):
        if self.direction_priority_queue:
            if self.direction_priority_queue.__len__() == 1:
                return 0
            else:
                if self.direction_priority_queue.__len__() >= 2:
                    up_index = 9999
                    down_index = 9999
                    if "up" in self.direction_priority_queue:
                        up_index = self.direction_priority_queue.index("up")
                    if "down" in self.direction_priority_queue:
                        down_index = self.direction_priority_queue.index("down")

                    if up_index != 9999 and down_index != 9999:
                        if up_index < down_index:
                            self.direction_priority_queue = ["up", "down"]
                        elif up_index > down_index:
                            self.direction_priority_queue = ["down", "up"]
                        else:
                            global_debugging()
                    else:
                        if up_index == 9999:
                            self.direction_priority_queue = ["down"]
                        elif down_index == 9999:
                            self.direction_priority_queue = ["up"]
                        else:
                            global_debugging()
        else:
            return 0

    def update_button(self, push_type):
        if push_type == "up":
            self.up_button_switch = 1
            if self.current_direction == "up":
                if self.current_floors > self.calling_floor:
                    self.up_calling_queue.append(self.calling_floor)
                    self.direction_priority_queue.append("up")
                elif self.current_floors < self.calling_floor:
                    self.called_floors_list.append(self.calling_floor)
                elif self.current_floors == self.calling_floor:
                    pass
            elif self.current_direction == "down":
                self.up_calling_queue.append(self.calling_floor)
                self.direction_priority_queue.append("up")
            elif self.current_direction == "stop":
                pass
            else:
                global_debugging()
        elif push_type == "down":
            self.down_button_switch = 1
            if self.current_direction == "down":
                if self.current_floors > self.calling_floor:
                    self.called_floors_list.append(self.calling_floor)
                elif self.current_floors < self.calling_floor:
                    self.down_calling_queue.append(self.calling_floor)
                    self.direction_priority_queue.append("down")
                elif self.current_floors == self.called_floors_list:
                    pass
            elif self.current_direction == "up":
                self.down_calling_queue.append(self.calling_floor)
                self.direction_priority_queue.append("down")
            elif self.current_direction == "stop":
                pass
            else:
                global_debugging()
        else:
            global_debugging()

    def check_display_direction(self):
        if self.current_direction == "up":
            self.direction_display[0] = self.up
            self.direction_display[1] = " "
        elif self.current_direction == "down":
            self.direction_display[0] = " "
            self.direction_display[1] = self.down
        elif self.current_direction == "stop":
            self.direction_display[0] = " "
            self.direction_display[1] = " "
        else:
            global_debugging()

    def check_display_floor(self):
        if self.current_floors >= 10:
            self.padding_switch = 1
        else:
            self.padding_switch = 0

        if self.calling_floor >= 10:
            self.floor_padding_switch = 1
        else:
            self.floor_padding_switch = 0

    def check_display_face_state(self):
        if 0 <= self.total_call_count <= self.standard_called[0]:
            self.face_state = 0
        elif self.standard_called[0] < self.total_call_count <= self.standard_called[1]:
            self.face_state = 1
        elif self.standard_called[1] < self.total_call_count:
            self.face_state = 2
        else:
            global_debugging()

    def check_limited_floor_condition(self):
        if not self.called_floors_list:
            self.current_direction = "stop"
        else:
            return 0

    def check_destination(self):
        if not self.called_floors_list:
            return 0
        else:
            if self.current_direction == "stop":
                return 0
            else:
                if self.current_direction == "up":
                    if not self.called_floors_list:
                        change_destination = max(self.called_floors_list)
                        self.current_destination = change_destination
                elif self.current_destination == "down":
                    if not self.called_floors_list:
                        change_destination = min(self.called_floors_list)
                        self.current_destination = change_destination
                self.called_floors_list = list(set(self.called_floors_list))

    def random_arrived_action(self):
        random_value = random.randrange(1, 151)
        if 1 <= random_value < 50:  # 사람 탄다.
            if self.current_people != self.max_people:
                to_be_added = random.randrange(1, (self.max_people-self.current_people)+1)
                #print("사람 탔다 :" + str(to_be_added))
                self.current_people += to_be_added
        elif 50 <= random_value < 100: # 사람 내렸다.
            if self.current_people != 0:
                to_be_subtracted = random.randrange(1,self.current_people+1)
                #print("사람 내렸다 : " + str(to_be_subtracted))
                self.current_people -= to_be_subtracted
        elif 100 <= random_value <= 150: # 아무도 안내리고 아무도 안탄다.
            #print("아무도 안타고 안내렸다.")
            self.current_people = self.current_people
        else:
            global_debugging()
        self.called_floors_list.remove(self.current_floors)
        sleep(2)
        self.stop_switch = 0

    def check_arrived_destination(self):
        if self.current_floors in self.called_floors_list:
            if self.stop_switch == 0 and self.move_switch == 0:
                stop_thread = Thread(target=self.random_arrived_action)
                self.stop_thread = stop_thread
                self.stop_switch = 1
                stop_thread.start()
            elif self.stop_switch == 1 and self.move_switch == 0:
                if self.stop_thread.is_alive():
                    return 0
                else:
                    self.stop_switch = 0
        else:
            pass
            """
            print("stop_switch : " + str(self.stop_switch))
            print("move_switch : " + str(self.move_switch))
            print("출발!")
            """

    def move_elevator(self):
        if self.current_direction == "up":
            sleep(1)
            self.current_floors += 1
        elif self.current_direction == "down":
            sleep(1)
            self.current_floors -= 1
        elif self.current_direction == "stop":
            return 0
        else:
            global_debugging()


def main_function():
    menu = Menu()
    elevator = Elevator()
    global global_menu_thread

    while True:
        menu.show_menu()
        selected = input("선택 >")
        elevator.init_elevator()
        menu_thread = Thread(target=elevator.async_menu)
        global_menu_thread = menu_thread
        run_thread = Thread(target=elevator.run_elevator)

        if selected == "1":
            menu_thread.start()
            run_thread.start()
            run_thread.join()
            menu_thread.join()
        elif selected == "2":
            print("종료 합니다.")
            break
        else:
            print("값이 올바르지 않습니다.")

if __name__ == "__main__":
    main_function()