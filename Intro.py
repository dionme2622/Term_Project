from stdafx import *
from Lobby import LobbyWindow

class IntroWindow:

    def LobbyWindow(self):
        self.inwindow.destroy()
        LobbyWindow()
    def __init__(self):
        self.inwindow = Tk()  # 처음 인트로 화면
        self.inwindow.title('Term_Project')
        self.inwindow.geometry('1000x900')  # 창의 크기를 1000x600으로 설정

        # GIF 이미지 로드 및 애니메이션 설정
        self.gif_path = 'airplane.gif'  # GIF 이미지 경로 설정
        self.img = Image.open(self.gif_path)

        self.frames = []
        for frame in ImageSequence.Iterator(self.img):
            frame = frame.resize((500, 500), Image.LANCZOS)  # Image.ANTIALIAS 대신 Image.LANCZOS 사용
            self.frames.append(ImageTk.PhotoImage(frame))

        self.image_label = Label(self.inwindow)
        self.image_label.pack(pady=20)

        # 애니메이션 시작
        self.animate(0)

        # 버튼 추가
        self.start_button = Button(self.inwindow, text="Press Button for Start", font=("Arial", 16),
                                   command=self.LobbyWindow)
        self.start_button.place(x=400, y=700)

        self.inwindow.mainloop()


    def animate(self, counter):
        frame = self.frames[counter]
        counter += 1
        if counter == len(self.frames):
            counter = 0
        self.image_label.configure(image=frame)
        self.inwindow.after(50, self.animate, counter)  # 50ms 간격으로 프레임 변경