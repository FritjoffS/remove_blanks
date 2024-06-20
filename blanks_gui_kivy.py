import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
import pyperclip
import threading
import time

kivy.require('2.0.0') # replace with your current kivy version !

def remove_blanks(text):
    return ''.join(text.split())

class ClipboardMonitorApp(App): 
    def build(self):
        # Set the window size
        Window.size = (300, 200)

        self.is_monitoring = False
        self.stop_event = threading.Event()

        self.status_label = Label(text="Not Monitoring")
        self.start_button = Button(text="Start Monitoring", on_press=self.start_monitoring)
        self.stop_button = Button(text="Stop Monitoring", on_press=self.stop_monitoring, disabled=True)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(self.status_label)
        layout.add_widget(self.start_button)
        layout.add_widget(self.stop_button)

        return layout

    def monitor_clipboard(self, dt):
        recent_value = ""
        while not self.stop_event.is_set():
            clipboard_text = pyperclip.paste()
            if clipboard_text != recent_value:
                cleaned_text = remove_blanks(clipboard_text)
                pyperclip.copy(cleaned_text)
                recent_value = cleaned_text
            time.sleep(0.5)

    def start_monitoring(self, instance):
        if not self.is_monitoring:
            self.is_monitoring = True
            self.stop_event.clear()
            self.monitor_thread = threading.Thread(target=self.monitor_clipboard, args=(0,))  # Create a new thread
            self.monitor_thread.start()
            self.start_button.disabled = True
            self.stop_button.disabled = False
            self.status_label.text = "Monitoring"
            print("Started monitoring clipboard.")

    def stop_monitoring(self, instance):
        if self.is_monitoring:
            self.is_monitoring = False
            self.stop_event.set()
            self.monitor_thread.join()  # Wait for the thread to finish
            self.start_button.disabled = False
            self.stop_button.disabled = True
            self.status_label.text = "Not Monitoring"
            print("Stopped monitoring clipboard.")

if __name__ == "__main__":
    ClipboardMonitorApp().run()
