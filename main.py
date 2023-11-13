import threading
import time
import os
from pynput import keyboard, mouse
import pygetwindow as gw

instructs:list[str] = []


def update_readme(instructs: list[str]):

    os.makedirs('output', exist_ok=True)
    readme_path = os.path.join('output', 'result.md')

    with open(readme_path, 'w') as file:
        for index, instruction in enumerate(instructs, start=1):
            file.write(f"{index}. {instruction}\n")

    print(f"Readme updated with {len(instructs)} instructions.")
    

def update_instructions(new_input: str):
    if new_input == 'enter':
        # Directly add 'Type Enter' as a new instruction
        instructs.append("Type 'Enter'")
    elif instructs and instructs[-1] == "Type 'Enter'":
        # If the last instruction is 'Type Enter', replace it with the new input
        if new_input == 'space':
            instructs[-1] = "Type ' '"
        elif new_input != 'backspace':
            # Replace 'Type Enter' with the new instruction
            instructs[-1] = f"Type '{new_input}'"
    elif instructs and instructs[-1].startswith("Type '"):
        # If the last instruction is a typing instruction, update it
        current_text = instructs[-1][6:-1]  # Extract current text from the instruction
        if new_input == 'backspace':
            # Handle backspace
            updated_text = current_text[:-1]
        elif new_input == 'space':
            # Handle space
            updated_text = current_text + ' '
        else:
            # Append new character
            updated_text = current_text + new_input
        instructs[-1] = f"Type '{updated_text}'"
    else:
        # For other characters or if the list is empty, add a new instruction
        if new_input == 'space':
            instructs.append("Type ' '")
        elif new_input != 'backspace':
            # Exclude backspace from adding a new instruction
            instructs.append(f"Type '{new_input}'")


def on_press(key):
    try:
        update_instructions(key.char)
    except AttributeError:
        # Handle special keys
        if key == keyboard.Key.space:
            update_instructions('space')
        elif key == keyboard.Key.backspace:
            update_instructions('backspace')
        elif key == keyboard.Key.enter:
            update_instructions('enter')
    update_readme(instructs)


def on_click(x, y, button, pressed):
    if pressed:
        ## Commented as those are very annoying and appear everytimg
        ## We can use those for screenshots but not to show in the instructions (2B discussed)
        ##instructs.append(f"Clicked at ({x}, {y})")
        return

def check_active_window():
    current_active_window = None
    while True:
        new_active_window = gw.getActiveWindow()
        if new_active_window != current_active_window:
            current_active_window = new_active_window
            if current_active_window is not None:
                try:
                    window_title = current_active_window.title()
                except TypeError:
                    window_title = current_active_window.title
                except AttributeError:
                    window_title = "Unknown Application"
                instructs.append(f"Go to {window_title}")
        time.sleep(1)
    print(instructs)


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