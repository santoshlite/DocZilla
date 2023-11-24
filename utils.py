from PIL import ImageGrab, ImageDraw
import os, time
import pygetwindow as gw
from pynput import keyboard
import pyautogui

INSTRUCTS : list = []
README_PATH = "./output/result.md"

def capture_screenshot(click_coords=None):
    """Captures a screenshot and optionally highlights the click coordinates."""
    os.makedirs('output/screenshots', exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    screenshot_file = f'screenshot_{timestamp}.png'
    
    # get the currently active window
    active_window = gw.getActiveWindow()

    # take screenshot of the active window
    if active_window is not None:
            screenshot = pyautogui.screenshot(region=(
                active_window.left,
                active_window.top,
                active_window.width,
                active_window.height
            ))


    if click_coords:
            draw = ImageDraw.Draw(screenshot)
            # Adjust click coordinates relative to the active window
            x, y = click_coords[0] - active_window.left, click_coords[1] - active_window.top
            radius = 30  # Radius of the circle
            # Draw a circle at the adjusted click coordinates
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline="red", width=2)

    screenshot.save(os.path.join('./output/screenshots', screenshot_file))
    screenshot_relative_path = os.path.join('./screenshots', screenshot_file)
    INSTRUCTS.append(f"![Screenshot]({screenshot_relative_path})\n\n")
    
def update_readme(instructs: list[str]):

    os.makedirs('output', exist_ok=True)
    readme_path = os.path.join('output', 'result.md')

    with open(readme_path, 'w') as file:
        for index, instruction in enumerate(instructs, start=1):
            file.write(f"{index}. {instruction}\n")

    print(f"Readme updated with {len(instructs)} instructions.")


# todo: maintain a buffer for text typed
def update_instructions(new_input: str):
    if new_input == 'enter':
        # Directly add 'Type Enter' as a new instruction
        INSTRUCTS.append("Type 'Enter'")
    elif INSTRUCTS and INSTRUCTS[-1] == "Type 'Enter'":
        # If the last instruction is 'Type Enter', replace it with the new input
        if new_input == 'space':
            INSTRUCTS[-1] = "Type ' '"
        elif new_input != 'backspace':
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
    print(instructs)