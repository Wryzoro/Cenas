
import os
import time

def alarm(seconds):
    time_elapsed = 0

    while time_elapsed < seconds:
        time.sleep(1)
        time_elapsed += 1

        time_left = seconds - time_elapsed
        minutes = time_left // 60
        seconds_left = time_left % 60

        print(f"\rTime left: {minutes}:{seconds_left:02d}", end="")

alarm(10)