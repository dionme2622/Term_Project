from tkinter import messagebox

from stdafx import *

class BookmarkWindow:
    def __init__(self, master, scene_stack):
        self.master = master
        self.scene_stack = scene_stack
        self.master.title('Bookmark')
        self.master.geometry('1000x900')

        self.listbox_x, self.listbox_y = 50, 200
        self.scrollbar = Scrollbar(self.master)
        self.scrollbar.place(x=self.listbox_x + 880, y=self.listbox_y, height=550)

        self.listbox = Listbox(self.master, yscrollcommand=self.scrollbar.set, font=("Arial", 20))
        self.listbox.place(x=self.listbox_x, y=self.listbox_y, width=880, height=550)

        self.scrollbar.config(command=self.listbox.yview)

        # 지도 버튼 추가
        self.map_button_image = PhotoImage(file="image/map.png")
        self.map_button = Button(self.master, image=self.map_button_image, width=50, height=50,
                                 command=self.go_map)
        self.map_button.place(x=720, y=130)

        # 이메일 버튼 추가
        self.email_button_image = PhotoImage(file="image/email.png")
        self.email_button = Button(self.master, image=self.email_button_image, width=50, height=50,
                                   command=self.go_email)
        self.email_button.place(x=790, y=130)

        # 경보 버튼 추가
        self.alarm_button_image = PhotoImage(file="image/alarm.png")
        self.alarm_button = Button(self.master, image=self.alarm_button_image, width=50, height=50,
                                   command=self.go_alarm)
        self.alarm_button.place(x=860, y=130)

        # 제거 버튼 추가
        self.remove_button_image = PhotoImage(file="image/trash.png")
        self.remove_button = Button(self.master, image=self.remove_button_image, width=50, height=50,
                                    command=self.removebook)
        self.remove_button.place(x=930, y=130)

        # 뒤로가기 버튼 추가
        self.back_button_image = PhotoImage(file="image/back.png")
        self.back_button = Button(self.master, image=self.back_button_image, width=50, height=50, command=self.go_back)
        self.back_button.place(x=50, y=800)

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def go_back(self):
        self.clear_window()
        previous_scene = self.scene_stack.pop()
        previous_scene.__init__(self.master, self.scene_stack)


    def go_map(self):
        pass

    def go_email(self):
        pass

    def go_alarm(self):
        pass

    def removebook(self):
        try:
            # 선택된 항목의 인덱스 가져오기
            selected_index = self.listbox.curselection()[0]
            # 선택된 항목 삭제
            self.listbox.delete(selected_index)
        except IndexError:
            # 항목이 선택되지 않았을 때 메시지 박스 표시
            messagebox.showwarning("Warning", "No item selected to delete.")
