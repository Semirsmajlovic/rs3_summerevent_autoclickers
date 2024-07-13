import time
import random
import logging
import sys
import threading
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Listener, KeyCode

# Setup logging to output to the console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)

mouse = MouseController()

# Activation keys
START_STOP_KEY = KeyCode(char='-')
EXIT_KEY = KeyCode(char='+')

# Configuration
INITIAL_DELAY = 10  # Initial delay before the first click (seconds)
CLICK_INTERVAL_MIN = 55  # Minimum interval between clicks (seconds)
CLICK_INTERVAL_MAX = 68  # Maximum interval between clicks (seconds)
POST_CLICK_DELAY = 3  # Delay after each click (seconds)

running = False
click_count = 0
click_thread = None

def on_press(key):
    global running, click_thread
    try:
        if key == START_STOP_KEY:
            running = not running
            if running:
                logging.info("Script started.")
                click_thread = threading.Thread(target=click_loop)
                click_thread.start()
            else:
                logging.info("Script stopped.")
        elif key == EXIT_KEY:
            logging.info(f"Exiting script. Total clicks made: {click_count}")
            running = False
            if click_thread:
                click_thread.join()
            listener.stop()
    except Exception as e:
        logging.error(f"Error in on_press: {e}")

def click_loop():
    global click_count, running
    last_move = None
    try:
        logging.info(f"Initial delay of {INITIAL_DELAY} seconds before first click.")
        time.sleep(INITIAL_DELAY)
        while running:
            x_move, y_move, last_move = determine_next_move(last_move)
            mouse.move(x_move, y_move)
            mouse.click(Button.left, 1)
            click_count += 1
            logging.info(f"Clicked Hook a Duck. Total clicks: {click_count}")
            time.sleep(random.uniform(CLICK_INTERVAL_MIN, CLICK_INTERVAL_MAX))
            time.sleep(POST_CLICK_DELAY)
    except Exception as e:
        logging.error(f"Error in click_loop: {e}")
        running = False

def determine_next_move(last_move):
    x_move, y_move = random.randint(-3, 3), random.randint(-3, 3)

    if last_move == 'right':
        x_move = random.randint(-3, 0)
    elif last_move == 'left':
        x_move = random.randint(0, 3)
    elif last_move == 'up':
        y_move = random.randint(0, 3)
    elif last_move == 'down':
        y_move = random.randint(-3, 0)

    if x_move > 0:
        last_move = 'right'
    elif x_move < 0:
        last_move = 'left'
    if y_move > 0:
        last_move = 'down'
    elif y_move < 0:
        last_move = 'up'

    return x_move, y_move, last_move

with Listener(on_press=on_press) as listener:
    listener.join()