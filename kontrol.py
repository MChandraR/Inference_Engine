import tkinter as tk
import paho.mqtt.client as mqtt

# MQTT Configuration
MQTT_BROKER = "192.168.1.105"  # Ganti dengan alamat broker MQTT Anda
MQTT_PORT = 1883
MQTT_TOPIC = "keyboard/input"

# Fungsi untuk mengirim pesan melalui MQTT
def send_mqtt_message(key):
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.publish(MQTT_TOPIC, key)
    client.disconnect()

# Fungsi untuk menangani input keyboard
def on_key_press(event):
    key = event.char.lower()  # Mengambil input karakter kecil
    if key in ['a', 's', 'w', 'd']:  # Hanya tangani ASWD
        print(f"Key Pressed: {key}")
        send_mqtt_message(key)

# Inisialisasi Tkinter
root = tk.Tk()
root.title("Keyboard Input to MQTT")

# Binding input keyboard ke fungsi on_key_press
root.bind("<KeyPress>", on_key_press)

# Loop Tkinter
root.mainloop()
