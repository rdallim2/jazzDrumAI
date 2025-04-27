import threading

class SyncManager:
    def __init__(self):
        self.beat_event = threading.Event()
        
    def signal_beat(self):
        """Signal that a beat has occurred"""
        self.beat_event.set()
        self.beat_event.clear()
        
    def wait_for_beat(self):
        """Wait for the next beat signal"""
        self.beat_event.wait()

# Global instance
sync = SyncManager() 