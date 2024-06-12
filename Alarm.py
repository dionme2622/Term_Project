import requests
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import font, Label, Entry, Button, PhotoImage, END, messagebox, Scrollbar, HORIZONTAL, VERTICAL

class AlarmWindow:
    def __init__(self, master, scene_stack, bookmarks):
        self.master = master
        self.scene_stack = scene_stack
        self.master.title('Alarm')
        self.master.geometry('1000x900')
        self.url = 'http://apis.data.go.kr/1262000/CountryBasicService/getCountryBasicList'
        self.url2 = 'http://apis.data.go.kr/1262000/TravelWarningService/getTravelWarningInfo'
        self.service_key = "NG9lJeYMK4rXHUM/L63r5DZpbjjaAm2oddIgbEGnsGsiuWnqb/3BCqaEbBzlGDdyfbncB4XHj4Joe+xGMQHZgQ=="
        self.bookmarks = bookmarks
        # 텔레그램 봇 API 토큰과 채팅 ID 설정
        self.telegram_token = '7311459647:AAEuYSO5db6oU5nUujRcWrR5bT5mUJ2JUdA'
        self.chat_id = '7306619402'

        # 멤버 변수 초기화
        self.data = []  # 검색 결과를 저장할 리스트

        # 출발지, 도착지 Label
        self.TempFont = font.Font(size=22, weight='bold', family='Consolas')
        self.country_label = Label(self.master, text='나라 이름', font=self.TempFont)
        self.country_label.place(x=110, y=110)

        # Entry 출발지, 도착지
        self.country_entry = Entry(self.master, font=("Arial", 16, 'bold'), width=10)
        self.country_entry.place(x=100, y=150)

        # 캔버스 추가
        self.canvas_x, self.canvas_y = 50, 200
        self.canvas = tk.Canvas(self.master, width=880, height=550, bg="white", scrollregion=(0, 0, 1500, 1500))
        self.canvas.place(x=self.canvas_x, y=self.canvas_y)

        # Y축 스크롤바 추가
        self.v_scrollbar = Scrollbar(self.master, orient=VERTICAL, command=self.canvas.yview)
        self.v_scrollbar.place(x=self.canvas_x + 880, y=self.canvas_y, height=550)
        self.canvas.config(yscrollcommand=self.v_scrollbar.set)

        # X축 스크롤바 추가
        self.h_scrollbar = Scrollbar(self.master, orient=HORIZONTAL, command=self.canvas.xview)
        self.h_scrollbar.place(x=self.canvas_x, y=self.canvas_y + 550, width=880)
        self.canvas.config(xscrollcommand=self.h_scrollbar.set)

        # 뒤로가기 버튼 추가
        self.back_button_image = PhotoImage(file="image/back.png")
        self.back_button = Button(self.master, image=self.back_button_image, font=("Arial", 16), width=50,
                                  height=50, command=self.go_back)
        self.back_button.place(x=50, y=800)

        # 검색 버튼 추가
        self.search_button_image = PhotoImage(file="image/search.png")
        self.search_button = Button(self.master, image=self.search_button_image, font=("Arial", 16),
                                    width=50, height=50, command=self.search)
        self.search_button.place(x=750, y=130)

        # 텔레그램 버튼 추가
        self.telegram_button_image = PhotoImage(file="image/telegram.png")
        self.telegram_button = Button(self.master, image=self.telegram_button_image, font=("Arial", 16),
                                    width=50, height=50, command=self.telegram)
        self.telegram_button.place(x=850, y=130)

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def go_back(self):
        self.clear_window()
        previous_scene = self.scene_stack.pop()
        previous_scene.__init__(self.master, self.scene_stack, self.bookmarks)

    def telegram(self):
        # 캔버스의 텍스트 정보를 추출
        items = self.canvas.find_all()
        messages = []
        for item in items:
            if self.canvas.type(item) == 'text':
                messages.append(self.canvas.itemcget(item, 'text'))

        # 텔레그램 메시지로 전송
        if messages:
            message_text = "\n".join(messages)
            self.send_telegram_message(message_text)

    def send_telegram_message(self, message):
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': message
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            messagebox.showinfo("Success", "Message sent to Telegram successfully!")
        else:
            messagebox.showerror("Error", "Failed to send message to Telegram.")

    def search(self):
        self.countryName = self.country_entry.get()
        queryParams = {
            'serviceKey': self.service_key,
            'countryName': self.countryName,
            'type': 'xml'
        }

        response = requests.get(self.url, params=queryParams)
        # 캔버스 초기화
        self.canvas.delete("all")

        if self.countryName == '':
            messagebox.showinfo('error', '나라를 입력하시오')
            return

        if response.status_code == 200:
            root = ET.fromstring(response.content)
            self.data = []  # 검색 결과를 저장할 리스트 초기화
            y_position = 40  # 텍스트 시작 위치
            self.country_id = None

            for item in root.iter('item'):
                self.country_id = item.findtext('id')
                basic = item.findtext('basic')
                self.data.append({'id': self.country_id, 'basic': basic})
                self.canvas.create_text(10, y_position, anchor="nw", text=f"국가 정보: {basic}",
                                        font=("Arial", 12))
                y_position += 10  # 다음 텍스트의 y 위치를 조정

            if self.country_id:
                queryParams2 = {
                    'serviceKey': self.service_key,
                    'id': self.country_id,
                    'type': 'xml'
                }
                response2 = requests.get(self.url2, params=queryParams2)
                if response2.status_code == 200:
                    root2 = ET.fromstring(response2.content)
                    self.data2 = []  # 검색 결과를 저장할 리스트 초기화
                    for item in root2.iter('item'):
                        attentionNote = item.findtext('attentionNote')
                        self.data2.append({'attentionNote': attentionNote})
                        self.canvas.create_text(10, 10, anchor="nw", text=f"<경보지역>: {attentionNote}",
                                                font=("Arial", 12))
                        y_position += 20  # 다음 텍스트의 y 위치를 조정
                else:
                    messagebox.showerror("Error", f"Error fetching data from url2: {response2.status_code}")

        else:
            messagebox.showerror("Error", f"Error fetching data from url1: {response.status_code}")

    def clear_entries(self):
        self.country_entry.delete(0, END)


if __name__ == "__main__":
    root = tk.Tk()
    scene_stack = []
    app = AlarmWindow(root, scene_stack, [])
    root.mainloop()