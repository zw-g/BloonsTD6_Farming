import pyautogui
import time
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
        time.sleep(2)
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
        pass

    def setup_monkeys(self):
        # Logic to set up monkeys
        # 1. Find and click the ok button
        location = self.wait_for_image('deflation_ok_button.png')
        if location: pyautogui.click(location)

        # 2. setup 1st (discount) monkey village

        # 3. place monkey village, 2 monkey ace, alchemist

        # 4. upgrade monkey village, 2 monkey ace, alchemist

        # 5. sell 1st (discount) monkey village

        # 6. place bomb shooter, sniper monkey

        # 7. upgrade bomb shooter, sniper monkey

        pass

    def run_game(self):
        # Logic to run the game, checking for popups
        # run the game and looking for popups until game complete
        # Return True if the game is successful, False otherwise
        pass

    def finish_game(self):
        # Logic to finish the game and return to the home screen
        # finish game and go back to home screen
        pass

# Example usage
automator = GameAutomator()
automator.start()

# To stop, you can call automator.stop()
