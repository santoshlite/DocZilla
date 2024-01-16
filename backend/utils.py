from pathlib import Path
import pyautogui
import os, time
import pygetwindow as gw
from pynput import keyboard
import re
import glob
from PIL import ImageDraw

INSTRUCTS : list = []
WINDOWS : list = []

# Define the shared directory
def get_shared_directory():
    return Path.home() / "Documents" / "GrimoireOutput"

# Modify get_next_filename to use the shared directory
def get_next_filename():
    shared_dir = get_shared_directory()
    pattern = str(shared_dir / 'result_*.md')
    files = glob.glob(pattern)
    max_num = 0

    for file in files:
        match = re.search(r'result_(\d+).md', file)
        if match:
            num = int(match.group(1))
            if num > max_num:
                max_num = num

    next_num = max_num + 1
    return str(shared_dir / f'result_{next_num}.md')

README_PATH : str = get_next_filename()

def capture_screenshot(click_coords=None):
    shared_dir = get_shared_directory()
    screenshots_dir = shared_dir / "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    screenshot_file = f'screenshot_{timestamp}.png'
    
    # Get the currently active window
    active_window = gw.getActiveWindow()
    geometry_window = gw.getWindowGeometry(active_window)

    if active_window is not None:
        # Ensure all values are integers
        left, top, width, height = map(int, [
            geometry_window[0],
            geometry_window[1],
            geometry_window[2],
            geometry_window[3]
        ])
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        if click_coords:
            draw = ImageDraw.Draw(screenshot)
            # Adjust click coordinates relative to the active window
            x, y = click_coords[0] - left, click_coords[1] - top
            radius = 30  # Radius of the circle
            # Draw a circle at the adjusted click coordinates
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline="red", width=2)
        screenshot.save(screenshots_dir / screenshot_file)
        screenshot_relative_path = str(Path('./screenshots') / screenshot_file)
        INSTRUCTS.append(f"![Screenshot]({screenshot_relative_path})\n\n")
    else:
        print("No active window found.")
    
def update_readme(instructs: list[str]):
    with open(README_PATH, 'w') as file:
        for index, instruction in enumerate(instructs, start=1):
            file.write(f"{index}. {instruction}\n")

    print(f"Readme updated: {README_PATH}")

# todo: maintain a buffer for text typed
def update_instructions(new_input: str):
    if new_input == 'enter':
        # Directly add 'Type Enter' as a new instruction
        INSTRUCTS.append("Type 'Enter'")
    elif INSTRUCTS and INSTRUCTS[-1] == "Type 'Enter'":
        # If the last instruction is 'Type Enter', replace it with the new input
        if new_input != 'backspace':
            # Replace 'Type Enter' with the new instruction
            INSTRUCTS[-1] = f"Type '{new_input}'"
    elif INSTRUCTS and INSTRUCTS[-1].startswith("Type '"):
        # If the last instruction is a typing instruction, update it
        current_text = INSTRUCTS[-1][6:-1]  # Extract current text from the instruction
        if new_input == 'backspace':
            # Handle backspace
            updated_text = current_text[:-1]
        elif new_input == 'space':
            # Handle space
            updated_text = current_text + ' '
        else:
            # Append new character
            updated_text = current_text + new_input
        INSTRUCTS[-1] = f"Type '{updated_text}'"
    else:
        # For other characters or if the list is empty, add a new instruction
        if new_input == 'space':
            INSTRUCTS.append("Type ' '")
        elif new_input != 'backspace':
            # Exclude backspace from adding a new instruction
            INSTRUCTS.append(f"Type '{new_input}'")
            
def on_press(key):
    try:
        char = key.char
    except AttributeError:
        char = ''

    if key == keyboard.Key.space:
        char = 'space'
    elif key == keyboard.Key.backspace:
        char = 'backspace'
    elif key == keyboard.Key.enter:
        char = 'enter'

    update_instructions(char)

    # Take screenshot and update readme for Enter key
    if char:
        update_readme(INSTRUCTS)
        if key == keyboard.Key.enter:
            capture_screenshot()
            
def on_click(x, y, button, pressed):
    if pressed:
        capture_screenshot((x, y))  # Pass the click coordinates to the screenshot function
        
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
                INSTRUCTS.append(f"Go to {window_title}")
        time.sleep(1)