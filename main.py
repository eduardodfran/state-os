import pygetwindow
import json
from datetime import date
import datetime
import time
import keyboard
import copy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QSystemTrayIcon, QMenu
from PyQt6.QtCore import QTimer, QThread
import sys


class Main:
    def __init__(self, active_window=None):
        try:
            with open('activity_log.json', 'r') as f:
                self.active_log = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.active_log = {}
        
        self.active_window = active_window
        self.opened_windows = []
        self.active = 0
        self.inactive = 0
        self.opened = self.active + self.inactive
        self.today = date.today().strftime("%Y-%m-%d")
        
        self.timer = QTimer()
        self.app = QApplication([])
        self.window = QWidget()
        self.window.setWindowTitle("Window Activity Dashboard")
        self.layout = QVBoxLayout()
        self.window.setLayout(self.layout)

        self.tray = QSystemTrayIcon(self.window)
        self.tray.setIcon(QIcon(""))
        
        
    
    def get_active_window(self):
        window = pygetwindow.getActiveWindow()
        if window and window.title:
            self.active_window = window.title
            print(f"Active window: {self.active_window}")
        else:
            self.active_window = "Unknown"
            
    def get_opened_windows(self):
        windows = pygetwindow.getAllWindows()
        self.opened_windows = [w.title for w in windows if not w.isMinimized and w.title]
        for i in self.opened_windows:
            if self.today not in self.active_log:
                self.active_log[self.today] = {}
            if i and i not in self.active_log[self.today]:
                self.active_log[self.today][i] = {"Active": 0, "Inactive": 0, "Opened": 0}
                
        
    def check_time(self):
        print(self.today)
        if self.today in self.active_log:
            return self.today
        
    def increment_active(self):
        print("Active window for increment:", self.active_window)
        print("All window keys:", list(self.active_log[self.today].keys()))
        if self.active_window in self.active_log[self.today]:
            self.active_log[self.today][self.active_window]["Active"] += 1
        else:
            print("Active window not found in log!")
            
    def increment_inactive(self):
        for i in self.opened_windows:
            if i and i != self.active_window:
                self.active_log[self.today][i]["Inactive"] += 1
                       
    def load_log(self):
        self.active_log[self.today][self.active_window] = {
            "Active": self.active,
            "Inactive": self.inactive,
            "Opened": self.opened
        }
        
    def insert(self):
        with open('activity_log.json', 'w') as f:
            json.dump(self.active_log, f, indent=4)
            
    def export_with_timeformat(self):
        log_copy = copy.deepcopy(self.active_log)
        for day in log_copy:
            for win in log_copy[day]:
                for stat in ["Active", "Inactive", "Opened"]:
                    seconds = log_copy[day][win][stat]
                    log_copy[day][win][stat] = str(datetime.timedelta(seconds=seconds))
        with open('activity_log_human.json', 'w') as f:
            json.dump(log_copy, f, indent=4)
            
    def update_tracking(self):
        self.get_active_window()
        self.get_opened_windows()
        self.increment_active()
        self.increment_inactive()
        self.check_time()
        self.insert()
        self.export_with_timeformat()
        
class TrackingThread(QThread):
    def __init__(self, app):
        super().__init__()
        self.app = app
    
    def run(self):
        while True:
            self.app.get_active_window()
            self.app.get_opened_windows()
            self.app.increment_active()
            self.app.increment_inactive()
            self.app.check_time()
            self.app.insert()
            self.app.export_with_timeformat()
            if keyboard.is_pressed('a'):
                print("The 'a' key is pressed!")
                break  # Exit the loop after detection
            
            time.sleep(1)
        
    
        
            
if __name__ == "__main__":
    app = Main()
    thread = TrackingThread(app)
    thread.start()
    app.timer.timeout.connect(app.update_tracking)
    # app.timer.start(1000)
    
    app.window.show()
    sys.exit(app.app.exec())
