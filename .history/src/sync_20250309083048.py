import threading

# Synchronization event for instruments
instrument_sync = threading.Event()
# Initially set it so the first beat doesn't hang
instrument_sync.set()

# Stop event to signal threads to terminate
stop_event = threading.Event()

# Global bar counter for bass
bar_count = 0