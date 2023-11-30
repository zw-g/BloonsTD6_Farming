import time

import cv2
import keyboard
import numpy as np
import pyautogui
import pygetwindow as gw


def locate_monkey_award(image_filename):
    # Take a screenshot with PyAut oGUI
    screenshot = pyautogui.screenshot()

    # Convert the PyAutoGUI Image object to a numpy array, then to OpenCV's BGR format
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Load the image we want to locate
    target_image = cv2.imread(f'../picture/{image_filename}')

    # Convert to grayscale for template matching
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    target_gray = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)

    # Perform template matching
    result = cv2.matchTemplate(screenshot_gray, target_gray, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    # Check for a good match
    if max_val > 0.8:
        # Get the size of the icon image
        icon_height, icon_width = target_gray.shape[:2]
        # Calculate the center of the icon
        center_x = max_loc[0] + icon_width // 2
        center_y = max_loc[1] + icon_height // 2
        return (center_x, center_y)  # Return the center coordinates of the icon
    else:
        return None


def press_key(key, presses=1, interval=0.25):
    """
    Simulates key presses.

    :param key: The key to press.
    :param presses: Number of times to press the key. Default is 1.
    :param interval: The interval between key presses. Default is 0.25 seconds.
    """
    for _ in range(presses):
        keyboard.press_and_release(key)
        time.sleep(interval)


def get_window_position(window_name):
    # Windows-specific implementation
    try:
        win = gw.getWindowsWithTitle(window_name)[0]  # Get the first window with the given title
        if win:
            return win.left, win.top
    except IndexError:
        # No window found
        return None, None


def click_relative_to_window(rel_x, rel_y, clicks=1, interval=0.25):
    window_pos = get_window_position('BloonsTD6')
    if window_pos:
        x, y = window_pos
        absolute_x, absolute_y = x + rel_x, y + rel_y
        pyautogui.moveTo(absolute_x, absolute_y, duration=0.1)
        pyautogui.click(absolute_x, absolute_y, clicks=clicks, interval=interval)


def wait_for_image(image_filename, timeout=7.0):
    image_path = f'../picture/{image_filename}'
    start_time = time.time()
    while True:
        current_time = time.time()
        if current_time - start_time > timeout:
            return None
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
            if location is not None:
                return location
        except pyautogui.ImageNotFoundException:
            pass
