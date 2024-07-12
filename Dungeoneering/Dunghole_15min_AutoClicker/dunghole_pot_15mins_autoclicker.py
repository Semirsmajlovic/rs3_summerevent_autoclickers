import time
import random
import logging
import sys
import threading
import pyautogui
from pynput.keyboard import Listener, KeyCode

# Setup logging to output to the console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)

# Activation keys
START_STOP_KEY = KeyCode(char='s')
EXIT_KEY = KeyCode.from_vk(27)

# Configuration
INITIAL_DELAY = 10  # Initial delay before the first click (seconds)
CLICK_INTERVAL_MIN = 230  # Minimum interval between clicks (seconds)
CLICK_INTERVAL_MAX = 240  # Maximum interval between clicks (seconds)
POST_CLICK_DELAY = 3  # Delay after each click (seconds)

# Global state
running = False
click_count = 0
click_thread = None
lock = threading.Lock()

def on_press(key):
    global running, click_thread
    try:
        if key == START_STOP_KEY:
            with lock:
                running = not running
            if running:
                logging.info("Script started.")
                click_thread = threading.Thread(target=click_loop)
                click_thread.start()
            else:
                logging.info("Script stopped.")
        elif key == EXIT_KEY:
            logging.info(f"Exiting script. Total clicks made: {click_count}")
            with lock:
                running = False
            if click_thread:
                click_thread.join()
            listener.stop()
    except Exception as e:
        logging.error(f"Error in on_press: {e}")

def click_loop():
    global click_count, running
    try:
        logging.info(f"Initial delay of {INITIAL_DELAY} seconds before first click.")
        time.sleep(INITIAL_DELAY)

        while True:
            with lock:
                if not running:
                    break
            try:
                perform_click_sequence()
            except Exception as e:
                logging.error(f"Error during click loop iteration: {e}")
                with lock:
                    running = False
    except Exception as e:
        logging.error(f"Error in click_loop: {e}")
        with lock:
            running = False

def perform_click_sequence():
    global click_count
    try:
        click("Hole in one", 1700, random.randint(810, 815))
        time.sleep(POST_CLICK_DELAY)
        click("Lemon Sour", 1700, random.randint(845, 850))
        time.sleep(POST_CLICK_DELAY)

        end_time = time.time() + random.randint(905, 907)
        while time.time() < end_time:
            with lock:
                if not running:
                    return
            click("Dung hole", 860 + random.randint(-1, 1), 690 + random.randint(-1, 1))
            time.sleep(random.uniform(CLICK_INTERVAL_MIN, CLICK_INTERVAL_MAX))
            logging.info("Waiting to Enter Dungeoneering Hole.")
            time.sleep(POST_CLICK_DELAY)

        click("Coordinates (860, 585)", 860, 585)
        time.sleep(POST_CLICK_DELAY)
        logging.info("15 minutes and 30 seconds interval completed. Restarting drink sequence.")
    except Exception as e:
        logging.error(f"Error in perform_click_sequence: {e}")

def click(description, x, y):
    global click_count
    pyautogui.moveTo(x, y)
    pyautogui.click()
    click_count += 1
    logging.info(f"Clicked {description}. Total clicks: {click_count}")

def determine_next_move(last_move):
    try:
        if last_move == 'right':
            x_move = random.randint(-2, 0)
            y_move = random.randint(-2, 2)
        elif last_move == 'left':
            x_move = random.randint(0, 2)
            y_move = random.randint(-2, 2)
        elif last_move == 'up':
            x_move = random.randint(-2, 2)
            y_move = random.randint(0, 2)
        elif last_move == 'down':
            x_move = random.randint(-2, 2)
            y_move = random.randint(-2, 0)
        else:
            x_move = random.randint(-2, 2)
            y_move = random.randint(-2, 2)

        if x_move > 0:
            last_move = 'right'
        elif x_move < 0:
            last_move = 'left'
        if y_move > 0:
            last_move = 'down'
        elif y_move < 0:
            last_move = 'up'

        return x_move, y_move, last_move
    except Exception as e:
        logging.error(f"Error in determine_next_move: {e}")
        return 0, 0, last_move

try:
    with Listener(on_press=on_press) as listener:
        logging.info("Listener started. Press 's' to start/stop and 'e' to exit.")
        listener.join()
except Exception as e:
    logging.error(f"Error starting listener: {e}")