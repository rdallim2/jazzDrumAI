import threading

# Synchronization event for instruments
instrument_sync = threading.Event()
instrument_sync.clear()

# Stop event to signal threads to terminate
stop_event = threading.Event()

# Global bar counter for bass
bar_count = 0