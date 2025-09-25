import pygetwindow

class Main:
    def __init__(self, active_window=None, opened_windows=None):
        self.active_window = active_window
        self.opened_windows = opened_windows
        
    def get_active_window(self):
        self.active_window = pygetwindow.getActiveWindow()
        
        print(self.active_window)
        
    def count_active_time(self):
        


app = Main()
app.get_active_window()
