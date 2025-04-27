import threading

instrument_sync = threading.Event()
instrument_sync.set()