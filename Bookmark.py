from tkinter import messagebox

from Alarm import AlarmWindow
from Email import EmailWindow
from stdafx import *
from tkhtmlview import HTMLLabel
import googlemaps
from PIL import Image, ImageTk
import requests
from io import BytesIO

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class BookmarkWindow:
    def __init__(self, master, scene_stack, bookmarks):
        global Google_API_Key
        self.master = master
        self.scene_stack = scene_stack
        self.master.title('Bookmark')
        self.master.geometry('1000x900')
        self.bookmarks = bookmarks

        Google_API_Key = 'AIzaSyCzFgc9OGnXckq1-JNhSCVGo9zIq1kSWcE'
        self.gmaps = googlemaps.Client(key=Google_API_Key)

        # 인천국제공항 지도 설정
        self.departure_airport = self.gmaps.geocode("인천국제공항")[0]['geometry']['location']
        self.departure_airport_map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={self.departure_airport['lat']},{self.departure_airport['lng']}&zoom=11&size=450x550&maptype=roadmap&key={Google_API_Key}"

        self.listbox_x, self.listbox_y = 50, 200
        self.scrollbar = Scrollbar(self.master)
        self.scrollbar.place(x=self.listbox_x + 880, y=self.listbox_y, height=550)

        self.listbox = Listbox(self.master, yscrollcommand=self.scrollbar.set, font=("Arial", 14))
        self.listbox.place(x=self.listbox_x, y=self.listbox_y, width=880, height=550)

        self.populate_listbox()
        self.scrollbar.config(command=self.listbox.yview)

        # 지도 표시를 위한 이미지 생성
        self.map_image1 = self.get_map_image(self.departure_airport_map_url)
        self.map_label1 = Label(self.master, image=self.map_image1)

        self.map_image2 = None
        self.map_label2 = Label(self.master)

        # 지도 버튼 추가
        self.map_button_image = PhotoImage(file="image/map.png")
        self.map_button = Button(self.master, image=self.map_button_image, width=50, height=50,
                                 command=self.show_map)
        self.map_button.place(x=790, y=130)

        # 이메일 버튼 추가
        self.email_button_image = PhotoImage(file="image/email.png")
        self.email_button = Button(self.master, image=self.email_button_image, width=50, height=50,
                                   command=self.go_email)
        self.email_button.place(x=650, y=130)

        # 이메일 Label
        self.TempFont = font.Font(size=18, weight='bold', family='Consolas')
        self.email_label = Label(self.master, text='보낼 주소 입력:', font=self.TempFont)
        self.email_label.place(x=200, y=140)

        # Entry 이메일
        self.email_entry = Entry(self.master, font=("Arial", 16, 'bold'), width=20)
        self.email_entry.place(x=400, y=140)


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

    def send_email(self):
        recipient_email = self.email_entry.get()
        if not recipient_email:
            messagebox.showwarning("Warning", "Please enter an email address.")
            return

        selected_text = self.get_selected_text()
        if not selected_text:
            messagebox.showwarning("Warning", "No item selected to send.")
            return

        subject = "Selected Bookmark Information"
        body = selected_text

        try:
            smtp_server = "smtp.naver.com"
            smtp_port = 587
            sender_email = "wolf1323@naver.com"  # 자신의 네이버 이메일 주소
            sender_password = "smreo0516"  # 자신의 네이버 앱 비밀번호

            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = recipient_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, msg.as_string())

            messagebox.showinfo("Info", "Email sent successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def get_selected_text(self):
        try:
            selected_index = self.listbox.curselection()[0]
            return self.listbox.get(selected_index)
        except IndexError:
            return None


    def get_map_image(self, url):
        try:
            response = requests.get(url)
            image_data = response.content
            image = Image.open(BytesIO(image_data))
            photo = ImageTk.PhotoImage(image)
            return photo
        except Exception as e:
            print("An error occurred while fetching the map image:", e)
            return None

    def show_map(self):
        selected_airport = self.get_selected_airport()
        if not selected_airport:
            messagebox.showwarning("Warning", "No item selected to show map.")
            return

        self.arrive_airport = self.gmaps.geocode(selected_airport)[0]['geometry']['location']
        self.arrive_airport_map_url = (f"https://maps.googleapis.com/maps/api/staticmap?center={self.arrive_airport['lat']},"
                                       f"{self.arrive_airport['lng']}&zoom=11&size=450x550&maptype=roadmap&key={Google_API_Key}")

        self.map_image2 = self.get_map_image(self.arrive_airport_map_url)
        self.map_label2.config(image=self.map_image2)

        self.map_label1.place(x=self.listbox_x, y=self.listbox_y)
        self.map_label2.place(x=self.listbox_x + 450, y=self.listbox_y)

    def get_selected_airport(self):
        try:
            selected_index = self.listbox.curselection()[0]
            selected_text = self.listbox.get(selected_index)
            for bookmark in self.bookmarks:
                display_text = (
                    f"Time: {bookmark['scheduleDateTime']}, "
                    f"항공사: {bookmark['airline']}, "
                    f"Airport: {bookmark['airport']}, "
                    f"GATE: {bookmark['gatenumber']}, "
                    f"terminal: {bookmark['terminalid']}"
                )
                if selected_text == display_text:
                    return bookmark['airport']
        except IndexError:
            return None

    def populate_listbox(self):
        self.listbox.delete(0, END)  # Listbox 초기화
        for bookmark in self.bookmarks:
            display_text = (
                f"Time: {bookmark['scheduleDateTime']}, "
                f"항공사: {bookmark['airline']}, "
                f"Airport: {bookmark['airport']}, "
                f"GATE: {bookmark['gatenumber']}, "
                f"terminal: {bookmark['terminalid']}"
            )
            self.listbox.insert(END, display_text)

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def go_back(self):
        self.clear_window()
        previous_scene = self.scene_stack.pop()
        previous_scene.__init__(self.master, self.scene_stack, self.bookmarks)

    def go_email(self):
        self.send_email()

    def go_alarm(self):
        self.scene_stack.append(self)
        self.clear_window()
        AlarmWindow(self.master, self.scene_stack, self.bookmarks)

    def removebook(self):
        try:
            # 선택된 항목의 인덱스 가져오기
            selected_index = self.listbox.curselection()[0]
            # 선택된 항목 삭제
            self.listbox.delete(selected_index)
            # bookmarks 리스트에서 해당 항목 삭제
            del self.bookmarks[selected_index]
        except IndexError:
            # 항목이 선택되지 않았을 때 메시지 박스 표시
            messagebox.showwarning("Warning", "No item selected to delete.")
