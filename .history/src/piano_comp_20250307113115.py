import random
import time

# Define piano voicings (root, 3rd, 5th, 7th, 9th, 13th) for jazz comping
piano_chords = {
    "C7": [(36, 40, 43, 46, 50, 53), (48, 52, 55, 58, 62, 65), (60, 64, 67, 70, 74, 77)],  # C7 (I)
    "F7": [(41, 45, 48, 51, 55, 58), (53, 57, 60, 63, 67, 70), (65, 69, 72, 75, 79, 82)],  # F7 (IV)
    "G7": [(43, 47, 50, 53, 57, 60), (55, 59, 62, 65, 69, 72), (67, 71, 74, 77, 81, 84)]   # G7 (V)
}

# Rhythmic comping patterns (swing feel)
comping_patterns = [
    [1, 0, 1],  # Skip beat 2
    [1, 1, 0],  # Skip beat 3
    [1, 1, 1],  # Skip beat 4
    [1, 0, 1],  # Half-time feel
    [1, 0, 0]   # Sparse hits
]

BEATS_PER_BAR = 4

def piano_comp(fs, time_per_beat, channel=1):
    """
    Simulates jazz piano comping over a 12-bar blues progression in C.
    
    Args:
        fs: FluidSynth instance
        time_per_beat: Duration of each beat in seconds
        channel: MIDI channel to use for piano (default 1)
    """
    bar_count = 0
    total_bars = 12
    
    while True:
        current_bar = bar_count % total_bars
        
        # Determine the current chord based on the bar
        if current_bar < 4:
            chord = piano_chords["C7"]  # I (C7)
        elif current_bar < 6:
            chord = piano_chords["F7"]  # IV (F7)
        elif current_bar < 8:
            chord = piano_chords["C7"]  # I (C7)
        elif current_bar == 8:
            chord = piano_chords["G7"]  # V (G7)
        elif current_bar == 9:
            chord = piano_chords["F7"]  # IV (F7)
        elif current_bar == 10:
            chord = piano_chords["C7"]  # I (C7)
        else:
            chord = piano_chords["G7"]  # V (G7) - Turnaround
        
        # Get the chord voicing for this bar
        comping_pattern = random.choice(comping_patterns)  # Choose a rhythmic pattern
        chord_voicing = random.choice(chord)  # Choose a random voicing
        
        # Comping for the current bar
        for i in range(BEATS_PER_BAR - 1):
            if comping_pattern[i]:  # Play only on marked beats
                for note in chord_voicing:
                    fs.noteon(channel, note, 70)  # Softer velocity for comping
                
                time.sleep(time_per_beat * 0.666)  # Swung feel
                
                for note in chord_voicing:
                    fs.noteoff(channel, note)
                
                time.sleep(time_per_beat * 0.333)  # Slight gap before the next beat
        
        # Anticipate the chord of the next bar on the "and" of beat 4
        next_bar = (bar_count + 1) % total_bars
        if next_bar < 4:
            next_chord = piano_chords["C7"]  # I (C7)
        elif next_bar < 6:
            next_chord = piano_chords["F7"]  # IV (F7)
        elif next_bar < 8:
            next_chord = piano_chords["C7"]  # I (C7)
        elif next_bar == 8:
            next_chord = piano_chords["G7"]  # V (G7)
        elif next_bar == 9:
            next_chord = piano_chords["F7"]  # IV (F7)
        elif next_bar == 10:
            next_chord = piano_chords["C7"]  # I (C7)
        else:
            next_chord = piano_chords["G7"]  # V (G7) - Turnaround
        
        anticipatory_voicing = random.choice(next_chord)  # Get voicing for next chord
        
        # Play anticipatory chord on the "and" of beat 4
        time.sleep(time_per_beat * (2/3))
        for note in anticipatory_voicing:
            fs.noteon(channel, note, 70)  # Softer velocity for comping
            
        # A short sleep to make sure it's played just before the next bar
        time.sleep(time_per_beat * (4/3))  # Short duration for anticipation
        
        for note in anticipatory_voicing:
            fs.noteoff(channel, note)
        
        bar_count += 1  # Move to the next bar