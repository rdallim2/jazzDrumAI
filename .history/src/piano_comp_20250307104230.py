import random
import time

# Define the 12-bar blues progression in C
blues_progression = [
    ("C2", "E2", "G2", "A2"),  # I chord
    ("F2", "A2", "C3", "D3"),  # IV chord
    ("G2", "B2", "D3", "E3")   # V chord
]

# Convert note names to MIDI numbers
note_map = {
    "C2": 36, "C#2": 37, "Db2": 37, "D2": 38, "D#2": 39, "Eb2": 39, 
    "E2": 40, "F2": 41, "F#2": 42, "Gb2": 42, "G2": 43, "G#2": 44, "Ab2": 44, 
    "A2": 45, "A#2": 46, "Bb2": 46, "B2": 47,

    "C3": 48, "C#3": 49, "Db3": 49, "D3": 50, "D#3": 51, "Eb3": 51, 
    "E3": 52, "F3": 53, "F#3": 54, "Gb3": 54, "G3": 55, "G#3": 56, "Ab3": 56, 
    "A3": 57, "A#3": 58, "Bb3": 58, "B3": 59,

    "C4": 60, "C#4": 61, "Db4": 61, "D4": 62, "D#4": 63, "Eb4": 63, 
    "E4": 64, "F4": 65, "F#4": 66, "Gb4": 66, "G4": 67, "G#4": 68, "Ab4": 68, 
    "A4": 69, "A#4": 70, "Bb4": 70, "B4": 71,

    "C5": 72
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
    
    while True:  # Loop indefinitely for background bass
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
            note = random.choice(chord)  # Choose a random note from the chord
            midi_note = note_map[note]
            
            # Use the provided channel instead of hardcoding to 0
            fs.noteon(channel, midi_note, 80)  # Slightly reduced velocity for bass
            
            # Calculate a slightly swung rhythm
            if _ % 2 == 0:  # On beats
                time.sleep(time_per_beat * 0.6)  # Slightly longer
            else:  # Off beats
                time.sleep(time_per_beat * 0.4)  # Slightly shorter
                
            fs.noteoff(channel, midi_note)

        bar_count += 1  # Move to the next bar

# More interesting walking bass line pattern
def walking_bass_line(fs, time_per_beat, channel=9):
    """
    Plays a walking bass line for 12-bar blues.
    
    Args:
        fs: FluidSynth instance
        time_per_beat: Duration of each beat in seconds
        channel: MIDI channel to use for bass (default 9)
    """
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
        
        for note in pattern:
            fs.noteon(channel, note, 80)
            time.sleep(time_per_beat * 0.95)  # Leave a tiny gap between notes
            fs.noteoff(channel, note)
            time.sleep(time_per_beat * 0.05)
            
        bar_count += 1