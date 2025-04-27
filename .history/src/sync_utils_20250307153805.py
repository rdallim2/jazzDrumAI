import threading
import time

# Shared synchronization events
bar_ready = threading.Event()
beat_ready = threading.Event()

class BarSync:
    def __init__(self, time_per_beat):
        self.time_per_beat = time_per_beat
        self.bar_start = time.time()
    
    def start_bar(self):
        """Mark the start of a new bar"""
        self.bar_start = time.time()
        bar_ready.set()
        bar_ready.clear()
    
    def wait_for_bar(self):
        """Wait for the next bar to start"""
        bar_ready.wait()
    
    def get_bar_timing(self):
        """Get timing information for the current bar"""
        current_time = time.time()
        elapsed = current_time - self.bar_start
        expected = self.time_per_beat * 4  # 4 beats per bar
        return elapsed, expected 