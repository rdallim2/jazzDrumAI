import random
import time
import threading

from sync import instrument_sync, stop_event


# Define the 12-bar blues progression in C
blues_progression = [
    ("C2", "E2", "G2", "A2"),  # I chord
    ("F2", "A2", "C3", "D3"),  # IV chord
    ("G2", "B2", "D3", "E3")   # V chord
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

        for _ in range(BEATS_PER_BAR):  # Play 4 notes per bar    
            if not stop_event.is_set():
                #print(f"Beat num: {_}")          
                if _ % 2 == 0:
                    #print("bass waiting for bar ready")
                    instrument_sync.wait()
                    #print("cleared!")
                note = random.choice(chord)  # Choose a random note from the chord
                midi_note = note_map[note]
                
                # Use the provided channel instead of hardcoding to 0
                fs.noteon(channel, midi_note, 80)  # Slightly reduced velocity for bass
                
                # Calculate a slightly swung rhythm
                time.sleep(time_per_beat + .001)
                    
                fs.noteoff(channel, midi_note)  


        bar_count += 1  # Move to the next bar

# Walking bass patterns for each chord
C_patterns = [
    [36, 38, 40, 41],  # C, D, E, F
    [36, 43, 41, 43],  # C, G, F, G
    [36, 40, 43, 45],  # C, E, G, A
    [36, 38, 40, 43]   # C, D, E, G
]

F_patterns = [
    [41, 43, 45, 46],  # F, G, A, Bb
    [41, 45, 48, 46],  # F, A, C, Bb
    [41, 43, 41, 39],  # F, G, F, E
    [41, 38, 36, 43]   # F, D, C, G
]

G_patterns = [
    [43, 45, 47, 48],  # G, A, B, C
    [43, 47, 50, 48],  # G, B, D, C
    [43, 45, 43, 41],  # G, A, G, F
    [43, 40, 41, 43]   # G, E, F, G
]

def walking_bass_line(fs, time_per_beat, channel=1):
    """
    Plays a walking bass line for 12-bar blues.
    
    Args:
        fs: FluidSynth instance
        time_per_beat: Duration of each beat in seconds
        channel: MIDI channel to use for bass (default 1)
    """
    bar_count = 0
    total_bars = 12
    
    while True:
        current_bar = bar_count % total_bars
        
        if current_bar < 4:
            pattern = random.choice(C_patterns)  # I (C)
        elif current_bar < 6:
            pattern = random.choice(F_patterns)  # IV (F)
        elif current_bar < 8:
            pattern = random.choice(C_patterns)  # I (C)
        elif current_bar == 8:
            pattern = random.choice(G_patterns)  # V (G)
        elif current_bar == 9:
            pattern = random.choice(F_patterns)  # IV (F)
        elif current_bar == 10:
            pattern = random.choice(C_patterns)  # I (C)
        else:
            pattern = random.choice(G_patterns)  # V (G) - Turnaround
        
        while not stop_event.is_set():
            for i, note in enumerate(pattern):
                if i % 2 == 0:
                    instrument_sync.wait()
                fs.noteon(channel, note, 80)
                time.sleep(time_per_beat * 0.95)  # Leave a tiny gap between notes
                fs.noteoff(channel, note)
                time.sleep(time_per_beat * 0.05)
            
        bar_count += 1