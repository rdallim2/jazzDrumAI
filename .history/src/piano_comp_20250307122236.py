import random
import time

# Define piano voicings (root, 3rd, 5th, 7th, 9th, 13th) for jazz comping

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

piano_chords = {
    #73595, 3795r, 3r57
    "C7": [(47, 52, 55, 62, 67), (40, 46, 50, 55, 60), (40, 48, 55, 58)],  # C7 (I)
    "F7": [(51, 57, 60, 67, 72), (57, 63, 67, 72, 79), (57, 65, 72, 77)],  # F7 (IV)
    "G7": [(41, 47, 50, 57, 62), (59, 65, 69, 74, 79), (59, 67, 74, 77)]   # G7 (V)
}

# Rhythmic comping patterns (swing feel)
comping_patterns = [

]

BEATS_PER_BAR = 4

def piano_comp(fs, time_per_beat, channel=10):
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