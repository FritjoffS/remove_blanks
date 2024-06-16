import pyperclip
import time

def remove_blanks(text):
    return ''.join(text.split())

def monitor_clipboard():
    recent_value = ""
    while True:
        clipboard_text = pyperclip.paste()
        if clipboard_text != recent_value:
            cleaned_text = remove_blanks(clipboard_text)
            pyperclip.copy(cleaned_text)
            recent_value = cleaned_text
        time.sleep(0.5)

if __name__ == "__main__":
    print("Monitoring clipboard for changes. Press Ctrl+C to stop.")
    try:
        monitor_clipboard()
    except KeyboardInterrupt:
        print("Clipboard monitoring stopped.")