# main.py
import pyperclip
import time


def remove_blanks(text):
    """Remove all blanks from the given text."""
    return text.replace(" ", "")


def monitor_clipboard():
    """Continuously monitor the clipboard and update it if the text changes."""
    recent_value = ""
    while True:
        # Get the current text from the clipboard
        current_value = pyperclip.paste()
        if current_value != recent_value:
            # Process the text to remove blanks
            processed_value = remove_blanks(current_value)
            # Update the clipboard with the processed text
            pyperclip.copy(processed_value)
            # Update the recent value
            recent_value = processed_value
        # Delay to avoid excessive CPU usage
        time.sleep(0.5)


if __name__ == "__main__":
    monitor_clipboard()
