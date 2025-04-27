import threading
import time

class SyncManager:
    def __init__(self):
        self.bar_start = threading.Event()
        self.bar_end = threading.Event()
        self.instruments_ready = 0
        self.instruments_done = 0
        self.total_instruments = 0
        self.lock = threading.Lock()
        self.running = False
        self.tempo = 120
        
    def set_tempo(self, tempo):
        """Set the tempo in beats per minute"""
        self.tempo = tempo
        
    def register_instrument(self):
        """Register a new instrument to be synchronized"""
        with self.lock:
            self.total_instruments += 1
            
    def wait_for_bar(self):
        """Wait for the next bar to start"""
        with self.lock:
            self.instruments_ready += 1
            if self.instruments_ready == self.total_instruments:
                self.instruments_ready = 0
                self.bar_start.set()
        self.bar_start.wait()
        self.bar_start.clear()
        
    def end_bar(self):
        """Signal that an instrument has finished its bar"""
        with self.lock:
            self.instruments_done += 1
            if self.instruments_done == self.total_instruments:
                self.instruments_done = 0
                self.bar_end.set()
        self.bar_end.wait()
        self.bar_end.clear()
        
    def start(self):
        """Start synchronization"""
        self.running = True
        self.instruments_ready = 0
        self.instruments_done = 0
        
    def stop(self):
        """Stop synchronization"""
        self.running = False
        self.bar_start.set()
        self.bar_end.set()

# Global sync manager instance
sync = SyncManager() 