import random
import time

# Define shell voicings (root, 3rd, 7th) for jazz guitar comping
jazz_chords = {
    "C7": [(36, 40, 46), (48, 52, 58), (60, 64, 70)],  # I chord (C7)
    "F7": [(41, 45, 51), (53, 57, 63), (65, 69, 75)],  # IV chord (F7)
    "G7": [(43, 47, 53), (55, 59, 65), (67, 71, 77)]   # V chord (G7)
}

# Rhythmic comping patterns (swing feel)
comping_patterns = [
    [1, 0, 1, 1],  # Skip beat 2
    [1, 1, 0, 1],  # Skip beat 3
    [1, 1, 1, 0],  # Skip beat 4
    [1, 0, 1, 0],  # Half-time feel
    [1, 0, 0, 1]   # Sparse hits
]

BEATS_PER_BAR = 4

def guitar_comp(fs, time_per_beat, channel=1):
    """
    Simulates jazz guitar comping over a 12-bar blues progression in C.
    
    Args:
        fs: FluidSynth instance
        time_per_beat: Duration of each beat in seconds
        channel: MIDI channel to use for guitar (default 1)
    """
    bar_count = 0
    total_bars = 12
    
    while True:
        current_bar = bar_count % total_bars
        
        if current_bar < 4:
            chord = jazz_chords["C7"]  # I (C7)
        elif current_bar < 6:
            chord = jazz_chords["F7"]  # IV (F7)
        elif current_bar < 8:
            chord = jazz_chords["C7"]  # I (C7)
        elif current_bar == 8:
            chord = jazz_chords["G7"]  # V (G7)
        elif current_bar == 9:
            chord = jazz_chords["F7"]  # IV (F7)
        elif current_bar == 10:
            chord = jazz_chords["C7"]  # I (C7)
        else:
            chord = jazz_chords["G7"]  # V (G7) - Turnaround
        
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
            next_chord = jazz_chords["C7"]  # I (C7)
        elif next_bar < 6:
            next_chord = jazz_chords["F7"]  # IV (F7)
        elif next_bar < 8:
            next_chord = jazz_chords["C7"]  # I (C7)
        elif next_bar == 8:
            next_chord = jazz_chords["G7"]  # V (G7)
        elif next_bar == 9:
            next_chord = jazz_chords["F7"]  # IV (F7)
        elif next_bar == 10:
            next_chord = jazz_chords["C7"]  # I (C7)
        else:
            next_chord = jazz_chords["G7"]  # V (G7) - Turnaround
        
        anticipatory_voicing = random.choice(next_chord)  # Get voicing for next chord
        
        # Play anticipatory chord on the "and" of beat 4
        for note in anticipatory_voicing:
            time.sleep(time_per_beat * .66)
            fs.noteon(channel, note, 50)  # Play softly for anticipation
            
        # A short sleep to make sure it's played just before the next bar
        time.sleep(time_per_beat * 1.33)  # Short duration for anticipation
        
        for note in anticipatory_voicing:
            fs.noteoff(channel, note)
        
        bar_count += 1  # Move to the next bar
