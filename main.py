import pygetwindow
import json
from datetime import date


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

        
        
    def get_active_window(self):
        window = pygetwindow.getActiveWindow()
        if window and window.title:
            self.active_window = window.title
            print(f"Active window: {self.active_window}")
        else:
            self.active_window = "Unknown"
            
    def get_opened_windows(self):
        self.opened_windows = pygetwindow.getAllTitles()
        for i in self.opened_windows:
            if self.today not in self.active_log:
                self.active_log[self.today] = {}
            if i and i not in self.active_log[self.today]:
                self.active_log[self.today][i] = {"Active": 0, "Inactive": 0, "Opened": 0}
                
        
    def check_time(self):
        print(self.today)
        if self.today in self.active_log:
            return self.today
        
    def count_active_time(self):
        # Check if date in log
        if self.today in self.active_log:
            print(f"{self.today} is in Activity log, inserting window...")
            if self.active_window in self.active_log[self.today]:
                self.active_log[self.today][self.active_window] = {
                    "Active": self.active,
                    "Inactive": self.inactive,
                    "Opened": self.opened
                }
            
        else:
            self.active_log[self.today] = {
                self.active_window: {
                    "Active": self.active, 
                    "Inactive": self.inactive, 
                    "Opened": self.opened 
                }
            }
            
    def load_log(self):
        self.active_log[self.today][self.active_window] = {
            "Active": self.active,
            "Inactive": self.inactive,
            "Opened": self.opened
        }
        
    def insert(self):
        with open('activity_log.json', 'w') as f:
            json.dump(self.active_log, f, indent=4)
            
            

if __name__ == "__main__":
    app = Main()
    app.get_opened_windows()
    app.get_active_window()
    app.check_time()
    app.count_active_time()
    app.insert()
    
