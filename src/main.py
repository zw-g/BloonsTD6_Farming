import pyautogui
import time
import signal
import sys
# opencv-python

class GameAutomator:
    def __init__(self):
        self.running = False
        self.total_games = 0
        self.successful_games = 0

    def start(self):
        self.running = True
        self.play_games()

    def stop(self):
        self.running = False
        success_rate = (self.successful_games / self.total_games) * 100 if self.total_games else 0
        print(f"{self.total_games} games completed with a {success_rate:.2f}% success rate.")

    def wait_for_image(self, image_filename, timeout=7.0):
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

    def play_games(self):
        while self.running:
            self.total_games += 1
            self.select_game_mode()
            self.setup_monkeys()
            success = self.run_game()
            self.finish_game()
            if success:
                self.successful_games += 1
            print(f"Game #{self.total_games} {'succeeded' if success else 'failed'}.")

    def select_game_mode(self):
        # Logic to select the game mode (starting from home screen)
        # 1. Locate the "BloonsTD6" window (the implementation depends on your OS and setup)

        # 2. Find and click the play button
        location = self.wait_for_image('play_button.png')
        if location: pyautogui.click(location)

        # 3. Find and click the expert map button
        location = self.wait_for_image('expert_map.png')
        if location: pyautogui.click(location)

        # 4. Find and click the ravine map button
        location = self.wait_for_image('ravine_map.png')
        if location: pyautogui.click(location)

        # 5. Find and click the easy level button
        location = self.wait_for_image('easy_level.png')
        if location: pyautogui.click(location)

        # 6. Find and click the deflation mode button
        location = self.wait_for_image('deflation_mode.png')
        if location: pyautogui.click(location)

    """
    Clicks on a specified screen location a certain number of times.
    pyautogui.click(x=x, y=y, clicks=clicks, interval=interval)
    
    :param x: The x-coordinate on the screen.
    :param y: The y-coordinate on the screen.
    :param clicks: Number of times to click. Default is 1.
    :param interval: The interval between clicks. Default is 0.25 seconds.
    
    Presses a specified key a certain number of times.
    pyautogui.press(key, presses=presses, interval=interval)

    :param key: The key to press.
    :param presses: Number of times to press the key. Default is 1.
    :param interval: The interval between key presses. Default is 0.25 seconds.
    """
    def setup_monkeys(self):
        # Logic to set up monkeys
        # 1. Find and click the ok button
        location = self.wait_for_image('deflation_ok_button.png')
        if location: pyautogui.click(location)
        time.sleep(1)

        # 2. setup 1st (discount) monkey village
        pyautogui.press('k')
        pyautogui.click(x=2750, y=800, clicks=2, interval=0.5)
        pyautogui.press('/', presses=2, interval=0.5)

        # 3. place & upgrade monkey village, 2 monkey ace, alchemist
        pyautogui.press('k')
        pyautogui.click(x=2830, y=800, clicks=2, interval=0.5)
        pyautogui.press(',', presses=3, interval=0.5)
        pyautogui.press('.', presses=2, interval=0.5)

        pyautogui.press('v')
        pyautogui.click(x=2750, y=870, clicks=2, interval=0.5)
        pyautogui.press(',', presses=2, interval=0.5)
        pyautogui.press('/', presses=3, interval=0.5)

        pyautogui.press('v')
        pyautogui.click(x=2750, y=927, clicks=2, interval=0.5)
        pyautogui.press(',', presses=2, interval=0.5)
        pyautogui.press('/', presses=3, interval=0.5)

        pyautogui.press('f')
        pyautogui.click(x=2830, y=870, clicks=2, interval=0.5)
        pyautogui.press(',', presses=4, interval=0.5)
        pyautogui.press('/', presses=1, interval=0.5)

        # 5. sell 1st (discount) monkey village
        pyautogui.click(x=2750, y=800)
        location = self.wait_for_image('sell_button.png')
        if location: pyautogui.click(location)

        # 6. place & upgrade bomb shooter, sniper monkey
        pyautogui.press('e')
        pyautogui.click(x=3029, y=400, clicks=2, interval=0.5)
        pyautogui.press('.', presses=3, interval=0.5)
        pyautogui.press('/', presses=1, interval=0.5)

        pyautogui.press('z')
        pyautogui.click(x=3050, y=840)

    def run_game(self):
        # Run the game and check for popups until the game is complete.
        # Returns True if the game is successful, False otherwise.

        # 1. Press Play
        location = self.wait_for_image('start_game.png')
        if location: pyautogui.click(location, clicks=2, interval=0.5)

        # 2. Game loop
        while True:
            if self.wait_for_image('game_success.png', 1):
                location = self.wait_for_image('victory_next.png')
                if location: pyautogui.click(location)
                return True  # Game completed successfully
            elif self.wait_for_image('game_fail.png', 1):
                return False  # Game failed or ended unsuccessfully

            if self.wait_for_image('level_up.png', 1):
                pyautogui.click(x=3357, y=431)  # Click to dismiss level up popup

            if self.wait_for_image('knowledge_point.png', 1):
                pyautogui.click(x=3357, y=431)  # Click to dismiss gift popup

    def finish_game(self):
        # Logic to finish the game and return to the home screen
        location = self.wait_for_image('home_button.png')
        if location: pyautogui.click(location)

def handle_exit(signum, frame):
    automator.stop()  # Call the stop method
    sys.exit(0)  # Exit the program cleanly

# set up signal handling
signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

automator = GameAutomator()
try:
    automator.start()
except KeyboardInterrupt:
    handle_exit(None, None)