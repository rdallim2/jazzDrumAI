import threading

instrument_sync = threading.Event()
instrument_sync.clear()

stop_event = threading.Event()