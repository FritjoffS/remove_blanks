# Added allways on top

import tkinter as tk
from tkinter import messagebox
import pyperclip
import time
import threading

def remove_blanks(text):
    return ''.join(text.split())

def monitor_clipboard(stop_event, status_var):
    recent_value = ""
    while not stop_event.is_set():
        clipboard_text = pyperclip.paste() 
        if clipboard_text != recent_value:
            cleaned_text = remove_blanks(clipboard_text)
            pyperclip.copy(cleaned_text)
            recent_value = cleaned_text
        time.sleep(0.5)

class ClipboardMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clipboard Monitor")
        self.is_monitoring = False
        self.stop_event = threading.Event()

        self.status_var = tk.StringVar()
        self.status_var.set("Not Monitoring")

        self.start_button = tk.Button(root, text="Start Monitoring", command=self.start_monitoring)
        self.start_button.pack(pady=10, padx=20)

        self.stop_button = tk.Button(root, text="Stop Monitoring", command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_button.pack(pady=10, padx=20)

        self.status_label = tk.Label(root, textvariable=self.status_var)
        self.status_label.pack(pady=10, padx=20)

        # Set the window attribute to make it always on top
        self.root.wm_attributes("-topmost", True)

    def start_monitoring(self):
        if not self.is_monitoring:
            self.is_monitoring = True
            self.stop_event.clear()
            self.monitor_thread = threading.Thread(target=monitor_clipboard, args=(self.stop_event, self.status_var)) # Create a new thread
            self.monitor_thread.start()
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_var.set("Monitoring")
            print("Started monitoring clipboard.")

    def stop_monitoring(self):
        if self.is_monitoring:
            self.is_monitoring = False
            self.stop_event.set()
            self.monitor_thread.join() # Wait for the thread to finish
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.status_var.set("Not Monitoring")
            print("Stopped monitoring clipboard.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardMonitorApp(root)
    root.mainloop()
