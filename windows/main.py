import signal
import sys
import time

import pyautogui
import pygetwindow as gw

import utility

# ANSI escape code for colors
WHITE = '\033[97m'
RED = '\033[91m'
PURPLE = '\033[95m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
ENDC = '\033[0m'  # ANSI code to end coloring

class GameAutomator:
    def __init__(self):
        self.running = False
        self.start_time = None
        self.total_games = 0
        self.successful_games = 0
        self.level_ups = 0
        self.monkey_knowledge_earned = 0
        self.monkeys_earned = 0

    def start(self):
        self.running = True
        self.start_time = time.time()
        self.play_games()

    def stop(self):
        self.running = False
        total_runtime = time.time() - self.start_time

        # Assumptions for simplicity:
        # 1 year = 365 days
        # 1 month = 30 days
        # 1 week = 7 days

        years, remainder = divmod(total_runtime, 31536000)  # 365 * 24 * 60 * 60
        months, remainder = divmod(remainder, 2592000)  # 30 * 24 * 60 * 60
        weeks, remainder = divmod(remainder, 604800)  # 7 * 24 * 60 * 60
        days, remainder = divmod(remainder, 86400)  # 24 * 60 * 60
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Create the formatted string
        formatted_runtime = []
        if years:
            year_label = "year" if years == 1 else "years"
            formatted_runtime.append(f"{int(years)} {year_label}")
        if months:
            month_label = "month" if months == 1 else "months"
            formatted_runtime.append(f"{int(months)} {month_label}")
        if weeks:
            week_label = "week" if weeks == 1 else "weeks"
            formatted_runtime.append(f"{int(weeks)} {week_label}")
        if days:
            day_label = "day" if days == 1 else "days"
            formatted_runtime.append(f"{int(days)} {day_label}")
        if hours:
            hour_label = "hour" if hours == 1 else "hours"
            formatted_runtime.append(f"{int(hours)} {hour_label}")
        if minutes:
            minute_label = "minute" if minutes == 1 else "minutes"
            formatted_runtime.append(f"{int(minutes)} {minute_label}")
        if seconds or not formatted_runtime:
            second_label = "second" if seconds == 1 else "seconds"
            formatted_runtime.append(f"{int(seconds)} {second_label}")

        formatted_runtime_str = ', '.join(formatted_runtime)

        success_rate = (self.successful_games / self.total_games) * 100 if self.total_games else 0

        print(f"⏱️ Number of games: {self.total_games} in {formatted_runtime_str}")
        print(f"✌️ Success rate: {success_rate:.2f}%")
        print(f"📈 Level ups: {self.level_ups}")
        print(f"🏆 Monkey Knowledge Earned: {self.monkey_knowledge_earned}")
        print(f"🐒 Monkeys Earned: {self.monkeys_earned}")

    def play_games(self):
        while self.running:
            self.select_game_mode()
            self.setup_monkeys()
            success = self.run_game()
            self.total_games += 1
            if success:
                self.successful_games += 1
                print(YELLOW + f"🎉 Victory o(*^▽^*)┛ {self.successful_games}/{self.total_games}" + ENDC)
            else:
                failed_games = self.total_games - self.successful_games
                print(RED + f"💔 Defeat （；´д｀）ゞ {failed_games}/{self.total_games}" + ENDC)
            self.finish_game()

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

        time.sleep(1)

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
        utility.click_relative_to_window(488, 570)

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
                self.level_ups += 1
                print(WHITE + "📈 Level + 1" + ENDC)
                pyautogui.click(location)  # Click to dismiss level up popup

                location = utility.wait_for_image('knowledge_point.png')
                if location:
                    self.monkey_knowledge_earned += 1
                    print(PURPLE + "🏆 Monkey Knowledge + 1" + ENDC)
                    pyautogui.click(location)  # Click to dismiss gift popup

    def finish_game(self):
        # Logic to finish the game and return to the home screen
        location = utility.wait_for_image('home_button.png')
        if location: pyautogui.click(location)

        while not utility.wait_for_image('play_button.png', 0.25):
            if utility.wait_for_image('collection_event.png', 0.25):

                location = utility.wait_for_image('collection_event_collect.png')
                if location: pyautogui.click(location)

                while not utility.wait_for_image('monkey_award_continue.png'):
                    location = utility.locate_monkey_award('monkey_award.png')
                    location1 = utility.locate_monkey_award('monkey_award_01.png')
                    if location:
                        self.monkeys_earned += 1
                        print(BLUE + "🐒 Insta Monkeys + 1" + ENDC)
                        pyautogui.click(location, clicks=2, interval=0.75)
                    if location1:
                        self.monkeys_earned += 1
                        print(BLUE + "🐒 Insta Monkeys + 1" + ENDC)
                        pyautogui.click(location, clicks=2, interval=0.75)

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
