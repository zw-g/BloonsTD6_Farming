import signal
import sys
import time

import pyautogui
import pygetwindow as gw

import utility


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

    def play_games(self):
        while self.running:
            self.select_game_mode()
            self.setup_monkeys()
            self.total_games += 1
            success = self.run_game()
            self.finish_game()
            if success:
                self.successful_games += 1
            print(f"Game #{self.total_games} {'succeeded' if success else 'failed'}.")

    def select_game_mode(self):
        # Logic to select the game mode (starting from home screen)
        # 1. Locate the "BloonsTD6" window
        try:
            win = gw.getWindowsWithTitle('BloonsTD6')[0]
            if win:
                win.activate()  # This brings the window to the front
        except IndexError:
            print("BloonsTD6 window not found")
            sys.exit(1)

        # 2. Find and click the play button
        location = utility.wait_for_image('play_button.png')
        if location: pyautogui.click(location)

        # 3. Find and click the expert map button
        location = utility.wait_for_image('expert_map.png')
        if location: pyautogui.click(location)

        # 4. Find and click the ravine map button
        location = utility.wait_for_image('ravine_map.png')
        if location: pyautogui.click(location)

        # 5. Find and click the easy level button
        location = utility.wait_for_image('easy_level.png')
        if location: pyautogui.click(location)

        # 6. Find and click the deflation mode button
        location = utility.wait_for_image('deflation_mode.png')
        if location: pyautogui.click(location)

    def setup_monkeys(self):
        # Logic to set up monkeys
        # 1. Find and click the ok button
        location = utility.wait_for_image('deflation_ok_button.png')
        if location: pyautogui.click(location)

        time.sleep(0.5)

        # 2. setup 1st (discount) monkey village
        utility.press_key('k')
        utility.click_relative_to_window(188, 530, 2, 0.5)
        utility.press_key('/', 2, 0.5)

        # 3. place & upgrade monkey village, 2 monkey ace, alchemist
        utility.press_key('k')
        utility.click_relative_to_window(268, 530, 2, 0.5)
        utility.press_key(',', 3, 0.5)
        utility.press_key('.', 2, 0.5)

        utility.press_key('v')
        utility.click_relative_to_window(188, 600, 2, 0.5)
        utility.press_key(',', 2, 0.5)
        utility.press_key('/', 3, 0.5)

        utility.press_key('v')
        utility.click_relative_to_window(188, 657, 2, 0.5)
        utility.press_key(',', 2, 0.5)
        utility.press_key('/', 3, 0.5)

        utility.press_key('f')
        utility.click_relative_to_window(268, 600, 2, 0.5)
        utility.press_key(',', 4, 0.5)
        utility.press_key('/', 1, 0.5)

        # 5. sell 1st (discount) monkey village
        utility.click_relative_to_window(188, 526)
        location = utility.wait_for_image('sell_button.png')
        if location: pyautogui.click(location)

        # 6. place & upgrade bomb shooter, sniper monkey
        utility.press_key('e')
        utility.click_relative_to_window(467, 126, 2, 0.5)
        utility.press_key('.', 3, 0.5)
        utility.press_key('/', 1, 0.5)

        utility.press_key('z')
        utility.click_relative_to_window(488, 566)

    def run_game(self):
        # Run the game and check for popups until the game is complete.
        # Returns True if the game is successful, False otherwise.

        # 1. Press Play
        location = utility.wait_for_image('start_game.png')
        if location: pyautogui.click(location, clicks=2, interval=0.5)

        # 2. Game loop
        while True:
            if utility.wait_for_image('game_success.png', 0.25):
                location = utility.wait_for_image('victory_next.png')
                if location: pyautogui.click(location)
                return True  # Game completed successfully

            elif utility.wait_for_image('game_fail.png', 0.25):
                return False  # Game failed or ended unsuccessfully

            location = utility.wait_for_image('level_up.png', 0.25)
            if location:
                pyautogui.click(location)  # Click to dismiss level up popup

            location = utility.wait_for_image('knowledge_point.png', 0.25)
            if location:
                pyautogui.click(location)  # Click to dismiss gift popup

    def finish_game(self):
        # ANSI escape code for yellow text
        YELLOW = '\033[93m'
        ENDC = '\033[0m'  # ANSI code to end coloring

        # Logic to finish the game and return to the home screen
        location = utility.wait_for_image('home_button.png')
        if location: pyautogui.click(location)

        while not utility.wait_for_image('play_button.png', 0.25):
            if utility.wait_for_image('collection_event.png', 0.25):

                location = utility.wait_for_image('collection_event_collect.png')
                if location: pyautogui.click(location)

                while not utility.wait_for_image('monkey_award_continue.png'):
                    location = utility.locate_monkey_award('monkey_award.png')
                    if location:
                        pyautogui.click(location, clicks=2, interval=0.75)
                        print(YELLOW + "monkey_award Clicked at location: " + str(location) + ENDC)

                location = utility.wait_for_image('monkey_award_continue.png')
                if location: pyautogui.click(location)

                location = utility.wait_for_image('collection_event_back.png')
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
