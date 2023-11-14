import  threading
from pynput import keyboard, mouse
from utils import *


def main():    
    # Set up and start the threads that listen for events from the user
    keyboard_listener = keyboard.Listener(on_press=on_press)
    mouse_listener = mouse.Listener(on_click=on_click)
    window_thread = threading.Thread(target=check_active_window)

    keyboard_listener.start()
    mouse_listener.start()
    window_thread.start()

    keyboard_listener.join()
    mouse_listener.join()
    window_thread.join()

if __name__ == "__main__":
    main()