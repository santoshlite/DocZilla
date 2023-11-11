import threading
import time
from pynput import keyboard, mouse
import pygetwindow as gw

def on_press(key):
    try:
        print(f"Typing '{key.char}'")
    except AttributeError:
        print(f"Typing {key}")

def on_click(x, y, button, pressed):
    if pressed:
        print("Clicked on something")

def check_active_window():
    current_active_window = None
    while True:
        new_active_window = gw.getActiveWindow()
        if new_active_window != current_active_window:
            current_active_window = new_active_window
            if current_active_window is not None:
                print(f"Go to {current_active_window.title}")
        time.sleep(1)


def check_active_window():
    current_active_window = None
    while True:
        new_active_window = gw.getActiveWindow()
        if new_active_window != current_active_window:
            current_active_window = new_active_window
            if current_active_window is not None:
                # Attempt to call the title method if it exists
                try:
                    window_title = current_active_window.title()
                except TypeError:
                    # If title is not a method, access it as an attribute
                    window_title = current_active_window.title
                except AttributeError:
                    # If there's no title attribute or method, use a generic placeholder
                    window_title = "Unknown Application"
 
                print(f"Go to [{window_title}]")
        time.sleep(1)



# Set up and start the threads
keyboard_listener = keyboard.Listener(on_press=on_press)
mouse_listener = mouse.Listener(on_click=on_click)
window_thread = threading.Thread(target=check_active_window)

keyboard_listener.start()
mouse_listener.start()
window_thread.start()

keyboard_listener.join()
mouse_listener.join()
window_thread.join()