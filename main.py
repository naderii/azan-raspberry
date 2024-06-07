import sys
import os
import csv
import random
from datetime import datetime, date, timedelta
import pygame
import time
from daemonize import Daemonize
import psutil

pid_file = "/tmp/prayer_times.pid"

def play_prayer_times():
    try:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, 'daily-event.csv')
        azan_audio_directory = os.path.join(current_directory, 'azan')
        prayer_audio_directory = os.path.join(current_directory, 'prayer')

        today_date = date.today().isoformat()
        print(f"Today's date: {today_date}")

        prayer_times = {}

        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Date'] == today_date:
                    prayer_times = {
                        'Dhuhr': row['Dhuhr'],
                        'Maghrib': row['Maghrib']
                    }
                    break
            else:
                print("No information found for today in the file.")
                return

        def get_time_object(prayer_time_str):
            return datetime.strptime(prayer_time_str, "%H:%M").time()

        prayer_times = {key: get_time_object(value) for key, value in prayer_times.items()}
        print(f"Prayer times: {prayer_times}")

        # Add 2 minutes to the Maghrib time
        prayer_times['Maghrib'] = (datetime.combine(date.today(), prayer_times['Maghrib']) + timedelta(minutes=2)).time()
        print(f"Adjusted Maghrib time: {prayer_times['Maghrib']}")

        azan_audio_files = [f for f in os.listdir(azan_audio_directory) if f.endswith('.mp3')]
        prayer_audio_files = [f for f in os.listdir(prayer_audio_directory) if f.endswith('.mp3')]
        print(f"Azan audio files: {azan_audio_files}")
        print(f"Prayer audio files: {prayer_audio_files}")

        pygame.mixer.init()

        log_file = os.path.join(current_directory, 'prayer_times_log.txt')
        print(f"Log file: {log_file}")

        while True:
            current_time = datetime.now().time()
            print(f"Current time: {current_time}")
            for prayer, prayer_time in prayer_times.items():
                if current_time.hour == prayer_time.hour and current_time.minute == prayer_time.minute:
                    if azan_audio_files:
                        azan_audio_file = random.choice(azan_audio_files)
                        print(f"Playing azan audio file: {azan_audio_file}")
                        pygame.mixer.music.load(os.path.join(azan_audio_directory, azan_audio_file))
                        pygame.mixer.music.play()
                        while pygame.mixer.music.get_busy():
                            continue
                    if prayer_audio_files:
                        prayer_audio_file = random.choice(prayer_audio_files)
                        print(f"Playing prayer audio file: {prayer_audio_file}")
                        pygame.mixer.music.load(os.path.join(prayer_audio_directory, prayer_audio_file))
                        pygame.mixer.music.play()
                        while pygame.mixer.music.get_busy():
                            continue
                    time.sleep(60)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        if os.path.exists(pid_file):
            with open(pid_file, 'r') as f:
                pid = int(f.read().strip())
            if psutil.pid_exists(pid):
                print("برنامه در حال اجرا است.")
                sys.exit()
            else:
                print(f"PID file exists but process {pid} is not running. Removing stale PID file.")
                os.remove(pid_file)
                
        print("Starting prayer times Daemon...")
        daemon = Daemonize(app="prayer_times", pid=pid_file, action=play_prayer_times)
        daemon.start()
    except Exception as e:
        print(f"An error occurred while starting the daemon: {e}")
        if os.path.exists(pid_file):
            os.remove(pid_file)
