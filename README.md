# BloonsTD6_Farming
A toolkit for automated resource farming in Bloons Tower Defense 6. It utilizes Python with PyAutoGUI and OpenCV for efficient in-game actions and image recognition, streamlining resource gathering.

## Pre-setup Requirements
Before using the automation script, make sure to configure your environment:

### Required:
- **Screen size**: 1280 x 720
- **Game Mode**: Unlock Expert - RAVINE map's Easy Mode's DEFLATION mode
- **Hotkeys**: Set to defaults

### Recommended:
- **Sound**: Turn off all sounds in the game
- **Graphics**: In Accessibility, set FX (effects scale) to off

## In-Game Setup
The script includes a pre-setup that should successfully complete levels. Adjustments can be made in the `setup_monkeys()` method in `main.py` based on your game progress and monkey knowledge.

### Modifying Monkeys:
- **Change Monkey**: `pyautogui.press('k')`
- **Change Placement**: Modify `x, y` in the script
- **Upgrade Skills**: Use `,` for path 1, `.` for path 2, `/` for path 3
- **Number of Upgrades**: Adjust `presses` as needed

```python
pyautogui.press('k')
pyautogui.click(x=2830, y=800, clicks=2, interval=0.5)
pyautogui.press(',', presses=3, interval=0.5)
pyautogui.press('.', presses=3, interval=0.5)
pyautogui.press('/', presses=2, interval=0.5)
```

## How to Run
1. Start BloonsTD6 and navigate to the screen with the "Play" button.
2. Run the script from your Python IDE.

## Downloading and Running the Repository
1. **Install Git**: Download from [git-scm.com](https://git-scm.com/downloads) if you don't already have it installed.
2. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/BloonsTD6_Farming.git
   ```
3. **Run the Script**:
   - Navigate to the cloned repository folder.
   - Open the script in your Python IDE.
   - Run the script as you would run any Python program.
