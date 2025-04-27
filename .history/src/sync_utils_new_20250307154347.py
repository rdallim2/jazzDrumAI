import threading
import time
import queue

class MusicClock:
    def __init__(self):
        self.running = False
        self.tempo = 120  # Default tempo
        self.subscribers = []
        self.thread = None
        self.beat_count = 0
    
    def set_tempo(self, tempo):
        """Set the tempo in beats per minute"""
        self.tempo = tempo
    
    def subscribe(self, callback):
        """Add a callback to be called on each beat"""
        self.subscribers.append(callback)
    
    def _clock_loop(self):
        """Main clock loop that broadcasts beats"""
        while self.running:
            beat_time = time.time()
            time_per_beat = 60.0 / self.tempo
            
            # Notify all subscribers
            for callback in self.subscribers:
                try:
                    callback(beat_time, self.beat_count)
                except Exception as e:
                    print(f"Error in subscriber callback: {e}")
            
            # Increment beat counter
            self.beat_count = (self.beat_count + 1) % 4
            
            # Sleep until next beat
            next_beat = beat_time + time_per_beat
            sleep_time = next_beat - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)
    
    def start(self):
        """Start the clock"""
        if not self.running:
            self.running = True
            self.beat_count = 0
            self.thread = threading.Thread(target=self._clock_loop)
            self.thread.daemon = True
            self.thread.start()
    
    def stop(self):
        """Stop the clock"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=0.1)
            self.thread = None
        self.beat_count = 0

# Global clock instance
clock = MusicClock() 