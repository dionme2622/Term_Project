from stdafx import *


class LobbyWindow:


    def __init__(self):
        self.lwindow = Tk()
        self.lwindow.title('Term_Project')
        self.lwindow.geometry('1000x900')  # 창의 크기를 1000x600으로 설정
        # self.inwindow.destroy()             # 인트로 화면 제거
    
        # 출발지, 도착지 Label
        self.TempFont = font.Font(size=16, weight='bold', family='Consolas')
        self.start_label = Label(self.lwindow, text='출발지', font=self.TempFont)
        self.start_label.place(x=140, y=60)
    
        self.arrive_label = Label(self.lwindow, text='도착지', font=self.TempFont)
        self.arrive_label.place(x=340, y=60)
    
        # Entry 출발지, 도착지
        self.start_entry = Entry(self.lwindow)
        self.start_entry.place(x=100, y=100)
        self.arrive_entry = Entry(self.lwindow)
        self.arrive_entry.place(x=300, y=100)
    
        self.scrollbar = Scrollbar(self.lwindow)
        self.scrollbar.place(x=930, y=470, height=200)
    
        self.listbox = Listbox(self.lwindow, yscrollcommand=self.scrollbar.set, font=("Arial", 16))
        self.listbox.place(x=50, y=150, width=880, height=500)
        self.scrollbar.config(command=self.listbox.yview)
    
        # 뒤로가기 버튼 추가
        self.back_button = Button(self.lwindow, text="뒤로가기", font=("Arial", 16))
        self.back_button.place(x=50, y=700)
    
        self.lwindow.mainloop()