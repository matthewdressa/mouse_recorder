import tkinter as tk
from pynput import mouse, keyboard
import time
import pyautogui

class MouseClickRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Click Recorder")

        self.label = tk.Label(root, text="Click 'Start Recording' to begin recording mouse clicks.")
        self.label.pack(pady=10)

        self.start_button = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.recorded_clicks = []
        self.start_time = 0
        self.listener = None
        self.recording_in_progress = False

        # Set up keyboard listener for toggling buttons
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()

    def on_key_press(self, key):
        try:
            # Check if any key is pressed
            if hasattr(key, 'char'):
                # Toggle buttons based on the pressed key
                if key.char.lower() == 'r':
                    if not self.recording_in_progress:
                        self.start_recording()
                    else:
                        self.stop_recording()
        except AttributeError:
            # Handle special keys (non-characters)
            pass

    def start_recording(self):
        self.label.config(text="Recording... Press 'R' to stop.")
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.recorded_clicks = []
        self.start_time = time.time()
        self.recording_in_progress = True

        # Start the mouse click listener
        self.listener = mouse.Listener(on_click=self.record_click)
        self.listener.start()

    def stop_recording(self):
        self.label.config(text="Recording stopped. Press 'R' to start recording again.")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        # Stop the mouse click listener
        if self.listener:
            self.listener.stop()
            self.listener.join()

        # Print the recorded clicks (excluding the stop recording click)
        print("Recorded Clicks:")
        for index, click in enumerate(self.recorded_clicks, start=1):
            print(f"Click {index}: {click}")

        # Print the number of clicks and the time elapsed
        num_clicks = len(self.recorded_clicks)
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        print(f"Number of Clicks: {num_clicks}")
        print(f"Time elapsed: {elapsed_time:.2f} seconds")

        self.recording_in_progress = False

    def record_click(self, x, y, button, pressed):
        # Record the mouse click coordinates if recording is in progress
        if self.recording_in_progress and pressed:
            screen_width, screen_height = pyautogui.size()
            click_coordinates = (x, screen_height - y)  # Adjust y-coordinate to be from bottom left
            self.recorded_clicks.append(click_coordinates)
            print(f"Click recorded at coordinates: {click_coordinates}")

    def __del__(self):
        # Stop the keyboard listener when the object is deleted
        if self.keyboard_listener:
            self.keyboard_listener.stop()
            self.keyboard_listener.join()

if __name__ == "__main__":
    root = tk.Tk()
    app = MouseClickRecorder(root)
    root.mainloop()
