from tkinter import messagebox

from stdafx import *


class EmailWindow:
    def __init__(self, master, scene_stack, bookmarks):
        global Google_API_Key
        self.master = master
        self.scene_stack = scene_stack
        self.master.title('Bookmark')
        self.master.geometry('1000x900')
        self.bookmarks = bookmarks

        Google_API_Key = 'AIzaSyCzFgc9OGnXckq1-JNhSCVGo9zIq1kSWcE'


        # 지도 버튼 추가
        self.map_button_image = PhotoImage(file="image/map.png")
        self.map_button = Button(self.master, image=self.map_button_image, width=50, height=50,
                                 command=self.show_map)
        self.map_button.place(x=720, y=130)

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



