from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
import pyperclip
import threading
import time

def remove_blanks(text):
    return ''.join(text.split())

class ClipboardMonitorApp(MDApp):
    def build(self):
        # Set the theme
        self.theme_cls.primary_palette = "BlueGray"
        # Set the window size
        Window.size = (300, 200)

        self.is_monitoring = False
        self.stop_event = threading.Event()
        


        self.status_label = MDLabel(text="Not Monitoring", halign="center")
        
        self.start_button =  MDRectangleFlatButton(
            text="Start Monitoring", 
            on_press=self.start_monitoring, 
            size_hint=(None, None), 
            size=(200, 50), 
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            md_bg_color=(0.2, 0.6, 0.86, 1),
            radius=[20]
        )
        self.stop_button = MDRectangleFlatButton(
            text="Stop Monitoring", 
            on_press=self.stop_monitoring, 
            disabled=True, 
            size_hint=(None, None), 
            size=(200, 50), 
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            md_bg_color=(0.2, 0.6, 0.86, 1),
            radius=[20]
        )

        layout = MDBoxLayout(
            orientation='vertical', 
            padding=10, 
            spacing=10, 
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        # Add the toolbar and other widgets
        screen = MDScreen()
        screen.add_widget(self.toolbar)
        screen.add_widget(layout)
        layout.add_widget(self.status_label)
        layout.add_widget(self.start_button)
        layout.add_widget(self.stop_button)

        return screen

    def monitor_clipboard(self):
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
            self.monitor_thread = threading.Thread(target=self.monitor_clipboard)  # Create a new thread
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
