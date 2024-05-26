import Intro
from stdafx import *
from Intro import *

class LobbyWindow:
    def __init__(self, master, scene_stack):
        self.master = master
        self.scene_stack = scene_stack
        self.master.title('Lobby')
        self.master.geometry('1000x900')

        # 출발지, 도착지 Label
        self.TempFont = font.Font(size=22, weight='bold', family='Consolas')
        self.start_label = Label(self.master, text='출발지', font=self.TempFont)
        self.start_label.place(x=110, y=110)

        self.arrive_label = Label(self.master, text='도착지', font=self.TempFont)
        self.arrive_label.place(x=410, y=110)

        # Entry 출발지, 도착지
        self.start_entry = Entry(self.master, font=("Arial", 16, 'bold'), width=10)
        self.start_entry.place(x=100, y=150)
        self.arrive_entry = Entry(self.master, font=("Arial", 16, 'bold'), width=10)
        self.arrive_entry.place(x=400, y=150)


        self.listbox_x, self.listbox_y = 50, 200
        self.scrollbar = Scrollbar(self.master)
        self.scrollbar.place(x=self.listbox_x + 880, y=self.listbox_y, height=550)

        self.listbox = Listbox(self.master, yscrollcommand=self.scrollbar.set, font=("Arial", 20))
        self.listbox.place(x=self.listbox_x, y=self.listbox_y, width=880, height=550)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.insert(0, '18:00                                    제주 -> 인천')  # '인천' 텍스트 입력
        self.listbox.insert(1, '20:00')  # '인천' 텍스트 입력


        # 라디오 버튼 추가
        # 선택된 라디오 버튼의 값을 저장할 변수
        self.selected_option = StringVar(value="Option 1")
        self.on_radio_button1_selected()
        self.radio_button1 = Radiobutton(self.master, text="출발지 -> 인천", value="Option 1",
                                         variable=self.selected_option, command=self.on_radio_button1_selected, )
        self.radio_button1.place(x=600, y=50)

        self.radio_button2 = Radiobutton(self.master, text="인천 -> 도착지", value="Option 2",
                                         variable=self.selected_option, command=self.on_radio_button2_selected)
        self.radio_button2.place(x=600, y=100)

        # 뒤로가기 버튼 추가
        self.back_button_image = PhotoImage(file="image/back.png")
        self.back_button = Button(self.master, image=self.back_button_image, text="뒤로가기", font=("Arial", 16), width=50, height=50
                                  , command=self.go_back)
        self.back_button.place(x=50, y=800)

        # 검색 버튼 추가
        self.search_button_image = PhotoImage(file="image/search.png")
        self.search_button = Button(self.master, image=self.search_button_image, text="뒤로가기", font=("Arial", 16), width=50,
                                  height=50)
        self.search_button.place(x=750, y=130)

        # 즐겨찾기 버튼 추가
        self.star_button_image = PhotoImage(file="image/star.png")
        self.star_button = Button(self.master, image=self.star_button_image, text="뒤로가기", font=("Arial", 16), width=50,
                                    height=50)
        self.star_button.place(x=820, y=130)


        self.master.mainloop()
        # 라디오 버튼 콜백 함수

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def go_back(self):
        self.clear_window()
        previous_scene = self.scene_stack.pop()
        previous_scene.__init__(self.master, self.scene_stack)
    def on_radio_button1_selected(self):
        self.clear_entries()
        self.arrive_entry.insert(0, '인천')  # '인천' 텍스트 입력

    def on_radio_button2_selected(self):
        self.clear_entries()
        self.start_entry.insert(0, '인천')  # '인천' 텍스트 입력

    # Entry 내용 삭제 함수
    def clear_entries(self):
        self.start_entry.delete(0, END)
        self.arrive_entry.delete(0, END)

    # 라디오 버튼 생성
