import tkinter as tk
from tkinter import  ttk
from PIL import ImageTk, Image
from tkinter import StringVar
import time
from threading import Thread

import cv2
class VideoMonitorApp(tk.Tk):
    def __init__(self, mqtt):
        super().__init__()
        self.title("Video Monitor App")
        self.geometry("1230x640")
        
        
        # Bagian baris pertama untuk video monitoring
        self.video_frame_1 = tk.Label(self, text="Video 1", bg="gray", width=55, height=20)
        self.video_frame_2 = tk.Label(self, text="Video 2", bg="gray", width=55, height=20)
        self.video_frame_3 = tk.Label(self, text="Video 3", bg="gray", width=55, height=20)
        
        self.video_frame_1.grid(row=0, column=0, padx=10, pady=10)
        self.video_frame_2.grid(row=0, column=1, padx=10, pady=10)
        self.video_frame_3.grid(row=0, column=2, padx=10, pady=10)
        
        # Baris kedua, kolom pertama untuk detail koordinat dan informasi
        self.detail_frame = tk.Frame(self, bg="white", width=10, height=10)
        self.detail_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        # Data 1
        self.coordinate_label = tk.Label(self.detail_frame, text="Azimuth:")
        self.coordinate_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.coordinate_value = StringVar()
        self.coordinate_value.set("(X: 0, Y: 0)")
        self.coordinate_value_label = tk.Label(self.detail_frame, textvariable=self.coordinate_value)
        self.coordinate_value_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        #Data 2
        self.counter_label = tk.Label(self.detail_frame, text="Counter:")
        self.counter_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.counter_value = StringVar()
        self.counter_value.set("0")
        self.counter_value_label = tk.Label(self.detail_frame, textvariable=self.counter_value)
        self.counter_value_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        #Data 3
        self.lat = tk.Label(self.detail_frame, text="Lat:")
        self.lat.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        
        self.lat_value = StringVar()
        self.lat_value.set("0")
        self.LatValue = tk.Label(self.detail_frame, textvariable=self.lat_value)
        self.LatValue.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        #Data 4
        self.long = tk.Label(self.detail_frame, text="Long:")
        self.long.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        
        self.long_value = StringVar()
        self.long_value.set("0")
        self.LongValue = tk.Label(self.detail_frame, textvariable=self.long_value)
        self.LongValue.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        #Data 5
        self.latdir = tk.Label(self.detail_frame, text="Lat Direction:")
        self.latdir.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        
        self.ld_value = StringVar()
        self.ld_value.set("0")
        self.latDirection = tk.Label(self.detail_frame, textvariable=self.ld_value)
        self.latDirection.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        
        #Data 6
        self.counter_label = tk.Label(self.detail_frame, text="Long Direction:")
        self.counter_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        
        self.lgd_value = StringVar()
        self.lgd_value.set("0")
        self.longDirection = tk.Label(self.detail_frame, textvariable=self.lgd_value)
        self.longDirection.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        
        #Data 1.1
        self.lat2_label = tk.Label(self.detail_frame, text="Lat 2:")
        self.lat2_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        self.lat2_value = StringVar()
        self.lat2_value.set("")
        self.lat2 = tk.Label(self.detail_frame, textvariable=self.lat2_value)
        self.lat2.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        #Data 1.2
        self.lon2_label = tk.Label(self.detail_frame, text="Lat 2:")
        self.lon2_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        self.lon2_value = StringVar()
        self.lon2_value.set("")
        self.lon2 = tk.Label(self.detail_frame, textvariable=self.lon2_value)
        self.lon2.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        
        # Baris kedua, kolom kedua untuk tombol pengaturan counter dan posisi
        self.control_frame = tk.Frame(self)
        self.control_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        
        self.update_counter_button = tk.Button(self.control_frame, text="Counter +", command=self.update_counter_plus)
        self.update_counter_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.update_position_button = tk.Button(self.control_frame, text="Counter -", command=self.update_counter_min)
        self.update_position_button.grid(row=1, column=0, padx=5, pady=5)
        
        self.counter_entry = tk.Entry(self.control_frame)
        self.counter_entry.grid(row=0, column=3, padx=5, pady=5)
        
        self.coor_entry = tk.Entry(self.control_frame)
        self.coor_entry.grid(row=0, column=4, padx=5, pady=5)
        
        #tambahan
        self.detail_frames = tk.Frame(self, bg="white", width=10, height=10)
        self.detail_frames.grid(row=2, column=0,columnspan=2, padx=10, pady=10, sticky="nsew")
        self.log_label = tk.Label(self.detail_frames, text="Log:")
        self.log_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.log_value = StringVar()
        self.log_value.set("0")
        self.log_area = tk.Label(self.detail_frames, textvariable=self.log_value)
        self.log_area.grid(row=1, column=0, padx=5, pady=5, sticky="w")


        # Counter dan posisi default
        self.counter = 0
        self.x_position = 0
        self.y_position = 0
        
        # Simulasi video update
        self.after(1000, self.update_video_frames)
        
        mqtt.setForm(self)
        self.mqtt = mqtt

    def update_video_frames(self):
        # Simulasi update frame video setiap detik
        current_time = time.strftime('%H:%M:%S')
        self.video_frame_1.config(text=f"Video 1 - {current_time}")
        self.video_frame_2.config(text=f"Video 2 - {current_time}")
        self.video_frame_3.config(text=f"Video 3 - {current_time}")
        self.after(1000, self.update_video_frames)  # Update setiap 1 detik
    
    def display_frame(self, label, frame):
        # Konversi frame BGR OpenCV ke RGB dan menampilkan di Tkinter Label
        frame = cv2.resize(frame , (400, 300))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        label.config(image=imgtk, width=400, height = 300)
        label.imgtk = imgtk
    
    
    def update_counter_plus(self):
        self.mqtt.counter +=1
        self.counter_value.set(str(self.mqtt.counter))
        
    def update_counter_min(self):
        self.mqtt.counter -=1
        self.counter_value.set(str(self.mqtt.counter))

    def update_position(self):
        self.x_position += 10
        self.y_position += 5
        self.coordinate_value.set(f"(X: {self.x_position}, Y: {self.y_position})")

    def update_log(self, msg):
        self.log_value.set(str(msg))

        
    def on_close(self):
        # Fungsi untuk menutup aplikasi dengan benar dan melepaskan resource
       
        self.destroy()

def launchApp(mqtt):
    global app
    app = VideoMonitorApp(mqtt)
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()


