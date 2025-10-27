from pynput import keyboard
import os
import shutil
import getpass
import sys

buffer = ''
controller = keyboard.Controller()

def on_press(key):
    global buffer
    try:
        char = key.char
    except AttributeError:
        return  # Skip non-character keys

    buffer += char
    if len(buffer) > 2:
        buffer = buffer[-2:]

    if buffer == 'vv':
        # Erase the two typed 'v's
        for _ in range(2):
            controller.press(keyboard.Key.backspace)
            controller.release(keyboard.Key.backspace)


        # Type 'w' instead
        controller.press('w')
        controller.release('w')

        buffer = ''


def on_release(key):
    if key == keyboard.Key.esc:
        return False  # Stop listener on ESC


def add_to_startup(script_path):

    startup_folder = os.path.join(
        os.getenv('APPDATA'),
        'Microsoft\\Windows\\Start Menu\\Programs\\Startup'
    )

    script_name = os.path.splitext(os.path.basename(script_path))[0]
    bat_path = os.path.join(startup_folder, f"{script_name}.bat")

    pythonw_path = os.path.join(sys.exec_prefix, 'pythonw.exe')

    if not os.path.exists(bat_path):
        with open(bat_path, 'w') as bat_file:
            bat_file.write(f'"{pythonw_path}" "{script_path}"\n')
        print(f"Added to startup: {bat_path}")
    else:
        print("Already in startup folder.")


if __name__ == "__main__":
    script_path = os.path.abspath(sys.argv[0])
    add_to_startup(script_path)

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
