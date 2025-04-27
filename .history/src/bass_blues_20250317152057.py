import random
import time
import threading

from sync import instrument_sync, stop_event
from chord_scale_maps import * 

# Global variable for tracking current bar
bar_count = 0

# List to store callback functions for bar updates
bar_update_callbacks = []

def register_bar_update_callback(callback_func):
    """Register a function to be called when the bar changes"""
    if callback_func not in bar_update_callbacks:
        bar_update_callbacks.append(callback_func)
        print(f"Registered callback: {callback_func.__name__}")

def unregister_bar_update_callback(callback_func):
    """Unregister a previously registered callback function"""
    if callback_func in bar_update_callbacks:
        bar_update_callbacks.remove(callback_func)
        print(f"Unregistered callback: {callback_func.__name__}")

def notify_bar_update(current_bar):
    """Notify all registered callbacks about the bar update"""
    for callback in bar_update_callbacks:
        try:
            callback(current_bar)
        except Exception as e:
            print(f"Error in bar update callback: {e}")

# Define the 12-bar blues progression in C
blues_progression = [
    ("C2", "E2", "G2", "Bb2", "C3"),  # I chord
    ("F2", "A2", "C3", "Eb3", "F3"),  # IV chord
    ("G2", "B2", "D3", "F3", "G3")   # V chord
]

# Convert note names to MIDI numbers
note_map = {
    "C2": 36, "E2": 40, "G2": 43, "A2": 45,
    "F2": 41, "A2": 45, "C3": 48, "D3": 50,
    "G2": 43, "B2": 47, "D3": 50, "E3": 52
}

BEATS_PER_BAR = 4

# Define the pattern (shuffle feel)
def play_bar(fs, time_per_beat, channel=9):
    """
    Plays a 12-bar blues cycle, randomly choosing notes from the given chord.
    
    Args:
        fs: FluidSynth instance
        time_per_beat: Duration of each beat in seconds
        channel: MIDI channel to use for bass (default 9)
    """
    bar_count = 0
    total_bars = 12  # Standard 12-bar blues
    
    while True and not stop_event.is_set():  # Loop indefinitely for background bass
        # Calculate the current position in the 12-bar progression
        current_bar = bar_count % total_bars
        
        if current_bar < 4:
            chord = blues_progression[0]  # I (C)
        elif current_bar < 6:
            chord = blues_progression[1]  # IV (F)
        elif current_bar < 8:
            chord = blues_progression[0]  # I (C)
        elif current_bar == 8:
            chord = blues_progression[2]  # V (G)
        elif current_bar == 9:
            chord = blues_progression[1]  # IV (F)
        elif current_bar == 10:
            chord = blues_progression[0]  # I (C)
        else:
            chord = blues_progression[2]  # V (G) - Turnaround

        last = 1

        for _ in range(BEATS_PER_BAR):  # Play 4 notes per bar    
            if not stop_event.is_set():
                #print(f"Beat num: {_}")          
                if _ % 2 == 0:
                    #print("bass waiting for bar ready")
                    instrument_sync.wait()
                    #print("cleared!")
                note = random.choice(chord)  # Choose a random note from the chord
                midi_note = bass_note_map[note]
                
                # Use the provided channel instead of hardcoding to 0
                fs.noteon(channel, midi_note, 80)  # Slightly reduced velocity for bass
                
                # Calculate a slightly swung rhythm
                time.sleep(time_per_beat + .001)
                    
                fs.noteoff(channel, midi_note)  


        bar_count += 1  # Move to the next bar


note_choice_mat = [
    [.05, .10, .30, .20, .35],
    [.30, .01, .14, .15, .20],
    [.30, .10, .10, .10, .40],
    [.10, .10, .15, .05, .60], 
    [.60, .05, .10, .20, .05]
]