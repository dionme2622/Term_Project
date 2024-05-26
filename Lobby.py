from stdafx import *


class LobbyWindow:
    def __init__(self):
        self.lwindow = Tk()
        self.lwindow.title('Term_Project')
        self.lwindow.geometry('1000x900')  # 창의 크기를 1000x900으로 설정

        # 출발지, 도착지 Label
        self.TempFont = font.Font(size=22, weight='bold', family='Consolas')
        self.start_label = Label(self.lwindow, text='출발지', font=self.TempFont)
        self.start_label.place(x=110, y=60)

        self.arrive_label = Label(self.lwindow, text='도착지', font=self.TempFont)
        self.arrive_label.place(x=410, y=60)

        # Entry 출발지, 도착지
        self.start_entry = Entry(self.lwindow, font=("Arial", 16, 'bold'), width=10)
        self.start_entry.place(x=100, y=100)
        self.arrive_entry = Entry(self.lwindow, font=("Arial", 16, 'bold'), width=10)
        self.arrive_entry.place(x=400, y=100)


        self.listbox_x, self.listbox_y = 50, 200
        self.scrollbar = Scrollbar(self.lwindow)
        self.scrollbar.place(x=self.listbox_x + 880, y=self.listbox_y, height=550)

        self.listbox = Listbox(self.lwindow, yscrollcommand=self.scrollbar.set, font=("Arial", 20))
        self.listbox.place(x=self.listbox_x, y=self.listbox_y, width=880, height=550)
        self.scrollbar.config(command=self.listbox.yview)

        # 라디오 버튼 추가
        # 선택된 라디오 버튼의 값을 저장할 변수
        self.selected_option = StringVar(value="Option 1")
        self.on_radio_button1_selected()
        self.radio_button1 = Radiobutton(self.lwindow, text="출발지 -> 인천", value="Option 1",
                                         variable=self.selected_option, command=self.on_radio_button1_selected, )
        self.radio_button1.place(x=600, y=50)

        self.radio_button2 = Radiobutton(self.lwindow, text="인천 -> 도착지", value="Option 2",
                                         variable=self.selected_option, command=self.on_radio_button2_selected)
        self.radio_button2.place(x=600, y=100)

        # 뒤로가기 버튼 추가
        self.button_image = PhotoImage(file="image/back.png")
        self.back_button = Button(self.lwindow, image=self.button_image, text="뒤로가기", font=("Arial", 16), width=50, height=50)
        self.back_button.place(x=50, y=800)

        self.lwindow.mainloop()

        # 라디오 버튼 콜백 함수
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
