import requests
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import font, Label, Entry, Listbox, Scrollbar, Radiobutton, Button, PhotoImage, StringVar, END, messagebox
from Bookmark import BookmarkWindow

bookmarks = []  # 즐겨찾기 리스트 초기화


class LobbyWindow:
    def __init__(self, master, scene_stack):
        self.master = master
        self.scene_stack = scene_stack
        self.master.title('Lobby')
        self.master.geometry('1000x900')
        self.url = 'https://apis.data.go.kr/B551177/StatusOfPassengerFlightsOdp/getPassengerDeparturesOdp'
        self.service_key = "NG9lJeYMK4rXHUM/L63r5DZpbjjaAm2oddIgbEGnsGsiuWnqb/3BCqaEbBzlGDdyfbncB4XHj4Joe+xGMQHZgQ=="

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

        self.listbox = Listbox(self.master, yscrollcommand=self.scrollbar.set, font=("Arial", 14))
        self.listbox.place(x=self.listbox_x, y=self.listbox_y, width=880, height=550)
        self.scrollbar.config(command=self.listbox.yview)

        # 라디오 버튼 추가
        self.selected_option = StringVar(value="Option 1")
        self.on_radio_button1_selected()
        self.radio_button1 = Radiobutton(self.master, text="출발지 -> 인천", value="Option 1",
                                         variable=self.selected_option, command=self.on_radio_button1_selected)
        self.radio_button1.place(x=600, y=50)

        self.radio_button2 = Radiobutton(self.master, text="인천 -> 도착지", value="Option 2",
                                         variable=self.selected_option, command=self.on_radio_button2_selected)
        self.radio_button2.place(x=600, y=100)

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

        # 즐겨찾기 버튼 추가
        self.star_button_image = PhotoImage(file="image/bookmark.png")
        self.star_button = Button(self.master, image=self.star_button_image, font=("Arial", 16), width=50,
                                  height=50, command=self.addbookmark)
        self.star_button.place(x=820, y=130)

        # 즐겨찾기 리스트로 가는 버튼 추가
        self.book_button_image = PhotoImage(file="image/star.png")
        self.book_button = Button(self.master, image=self.book_button_image, font=("Arial", 16), width=50,
                                  height=50, command=self.go_bookmark)
        self.book_button.place(x=900, y=800)

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def go_back(self):
        self.clear_window()
        previous_scene = self.scene_stack.pop()
        previous_scene.__init__(self.master, self.scene_stack)

    def go_bookmark(self):
        self.scene_stack.append(self)
        self.clear_window()
        BookmarkWindow(self.master, self.scene_stack, bookmarks)

    def search(self):
        if self.selected_option.get() == "Option 1":
            self.airport = self.start_entry.get()
        else:
            self.airport = self.arrive_entry.get()
        queryParams = {
            'serviceKey': self.service_key,
            'airport_code': self.airport,
            'type': 'xml'
        }

        response = requests.get(self.url, params=queryParams)
        # Listbox 초기화
        self.listbox.delete(0, END)

        if self.airport == '':
            messagebox.showinfo('error', 'code를 입력하시오')
            return

        if response.status_code == 200:
            root = ET.fromstring(response.content)
            seen_schedule_times = set()  # 중복된 schedule_time을 체크하기 위한 set
            self.data = []  # 여기서 data를 인스턴스 변수로 저장
            for item in root.iter('item'):
                schedule_time = item.findtext('scheduleDateTime')
                if schedule_time and len(schedule_time) == 12:  # "YYYYMMDDHHMM" 형식인지 확인
                    schedule_time = f"{schedule_time[:4]}.{schedule_time[4:6]}.{schedule_time[6:8]} {schedule_time[8:10]}:{schedule_time[10:12]}"  # "YYYY.MM.DD HH:MM" 형식으로 변환
                if schedule_time in seen_schedule_times:
                    continue  # 이미 본 schedule_time이면 건너뜀
                seen_schedule_times.add(schedule_time)

                airline = item.findtext('airline')
                airport = item.findtext('airport')
                gatenumber = item.findtext('gatenumber')
                terminalid = item.findtext('terminalid')
                self.data.append({
                    'scheduleDateTime': schedule_time,
                    'airline': airline,
                    'airport': airport,
                    'gatenumber': gatenumber,
                    'terminalid': terminalid
                })

            if self.data:
                for entry in self.data:
                    self.listbox.insert(END,
                                        f"Time: {entry['scheduleDateTime']}, 항공사: {entry['airline']}, Airport: {entry['airport']}")
            else:
                self.listbox.insert(END, "No data available")
        else:
            messagebox.showerror("Error", f"Error fetching data: {response.status_code}")

    def addbookmark(self):
        selected_items = self.listbox.curselection()
        if selected_items:
            for index in selected_items:
                item = self.listbox.get(index)
                # data dictionary에서 항목을 찾아서 저장
                for entry in self.data:
                    if f"Time: {entry['scheduleDateTime']}, 항공사: {entry['airline']}, Airport: {entry['airport']}" == item:
                        bookmarks.append(entry)
                        break
            messagebox.showinfo("Success", "Selected item(s) added to bookmarks.")
        else:
            messagebox.showwarning("Warning", "No item selected to bookmark.")

    def on_radio_button1_selected(self):
        self.clear_entries()
        self.arrive_entry.insert(0, '인천')
        self.url = 'http://apis.data.go.kr/B551177/StatusOfPassengerFlightsDSOdp/getPassengerDeparturesDSOdp'

    def on_radio_button2_selected(self):
        self.clear_entries()
        self.start_entry.insert(0, '인천')
        self.url = "http://apis.data.go.kr/B551177/StatusOfPassengerFlightsDSOdp/getPassengerArrivalsDSOdp"

    def clear_entries(self):
        self.start_entry.delete(0, END)
        self.arrive_entry.delete(0, END)

if __name__ == "__main__":
    root = tk.Tk()
    scene_stack = []
    app = LobbyWindow(root, scene_stack)
    root.mainloop()
