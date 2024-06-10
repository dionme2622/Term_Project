from tkinter import *
from PIL import Image, ImageTk, ImageSequence

import Lobby
from Lobby import *
class IntroWindow:
    def __init__(self, master, scene_stack, bookmarks):
        self.master = master
        self.scene_stack = scene_stack
        self.master.title('Term_Project')
        self.master.geometry('1000x900')



        # GIF 이미지 로드 및 애니메이션 설정
        self.gif_path = 'image/airplane.gif'  # GIF 이미지 경로 설정
        self.img = Image.open(self.gif_path)

        self.frames = []
        for frame in ImageSequence.Iterator(self.img):
            frame = frame.resize((500, 500), Image.LANCZOS)  # Image.ANTIALIAS 대신 Image.LANCZOS 사용
            self.frames.append(ImageTk.PhotoImage(frame))

        self.image_label = Label(self.master)
        self.image_label.pack(pady=20)

        self.animation_running = False
        self.animation_id = None

        self.animate(0)

        # 시작 버튼 추가
        self.start_button_lobby = Button(self.master, text="Press Button for Start", font=("Arial", 16),
                                         command=self.go_lobby)
        self.start_button_lobby.place(x=400, y=800)

    def animate(self, counter):
        frame = self.frames[counter]
        counter += 1
        if counter == len(self.frames):
            counter = 0
        self.image_label.configure(image=frame)
        self.animation_id = self.master.after(50, self.animate, counter)  # 50ms 간격으로 프레임 변경


    def stop_animation(self):
        self.master.after_cancel(self.animation_id)


    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def go_lobby(self):
        self.stop_animation()
        self.scene_stack.append(self)
        self.clear_window()
        LobbyWindow(self.master, self.scene_stack, bookmarks)


