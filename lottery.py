import time
import threading
import random
import os
import json
from datetime import datetime, timedelta

LOG_FILE = 'lottery_log.txt'
SAVE_INTERVAL = 300 
DISPLAY_INTERVAL = 600  

participants = set()
start_time = datetime.now()
registration_end_time = start_time + timedelta(hours=1)
extended = False
lock = threading.Lock()


def save_progress():
    with lock:
        with open(LOG_FILE, 'w') as f:
            f.write(f"Registration Start Time: {start_time}\n")
            f.write(f"Current Time: {datetime.now()}\n")
            f.write("Participants:\n")
            for user in participants:
                f.write(f"{user}\n")


def periodic_saver():
    while datetime.now() < registration_end_time:
        time.sleep(SAVE_INTERVAL)
        save_progress()


def display_remaining_time():
    while datetime.now() < registration_end_time:
        time.sleep(DISPLAY_INTERVAL)
        remaining = registration_end_time - datetime.now()
        print(f"Time remaining for registration: {remaining}")


def register_user():
    global registration_end_time, extended
    print("Lottery Registration Started. You have 1 hour.")
    while datetime.now() < registration_end_time:
        username = input("Enter a unique username: ").strip()
        if not username or any(not c.isalnum() for c in username):
            print("Invalid input. Usernames must be alphanumeric and non-empty.")
            continue

        with lock:
            if username in participants:
                print("This username is already taken. Try another.")
            else:
                participants.add(username)
                print(f"{username} registered successfully. Total participants: {len(participants)}")

    if len(participants) < 5 and not extended:
        print("Fewer than 5 users registered. Extending registration by 30 minutes.")
        registration_end_time += timedelta(minutes=30)
        extended = True
        register_user()


def announce_winner():
    if not participants:
        print("No users registered. Exiting.")
        return

    winner = random.choice(list(participants))
    with open(LOG_FILE, 'a') as f:
        f.write(f"\nLottery Drawn At: {datetime.now()}\n")
        f.write(f"Total Participants: {len(participants)}\n")
        f.write(f"Winner: {winner}\n")

    print("\n===== LOTTERY RESULT =====")
    print(f"Total Participants: {len(participants)}")
    print(f"Winner: {winner}")
    print("==========================")


if __name__ == '__main__':
    try:
        saver_thread = threading.Thread(target=periodic_saver, daemon=True)
        timer_thread = threading.Thread(target=display_remaining_time, daemon=True)

        saver_thread.start()
        timer_thread.start()

        register_user()
        announce_winner()

    except KeyboardInterrupt:
        print("\nInterrupted. Saving progress...")
        save_progress()
        print("Progress saved. Exiting.")
