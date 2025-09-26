import pygetwindow
import json
import time


class Main:
    def __init__(self, active_window=None, opened_windows=None):
        self.active_log = open('./activity_log.json')
        self.active_window = active_window
        self.opened_windows = opened_windows
        self.time = 0
        self.today = time.date().today()
        
    def get_active_window(self):
        self.active_window = pygetwindow.getActiveWindow()
        
        window = self.active_window.title.split(" - ")
        print(window[2])
        
        
        
        
    def count_active_time(self):
        if self.active_window not in self.active_log:
            # Add the active window to the json
            # Then start the time
            while True:
                self.time += 1
                if pygetwindow.getActiveWindow() != self.active_window:
                    break
                
                
            # if the active window is closed it should stop the time


app = Main()
app.get_active_window()
