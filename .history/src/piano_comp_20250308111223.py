import random
import time

from piano_phrases import *

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
    "C7": [(59, 64, 67, 74, 79), (52, 58, 62, 67, 72), (52, 60, 67, 70)],  # C7 (I)
    "F7": [(51, 57, 60, 67, 72), (57, 63, 67, 72, 79), (57, 65, 72, 77)],  # F7 (IV)
    "G7": [(41, 47, 50, 57, 62), (59, 65, 69, 74, 79), (59, 67, 74, 77)]   # G7 (V)
}

# Rhythmic comping patterns (swing feel)
comping_patterns = [
    [1, 0, 0, 1]
]

BEATS_PER_BAR = 4

def piano_comp(fs, time_per_beat, tempo, channel=10):
    """
    Simulates jazz piano comping over a 12-bar blues progression in C.
    
    Args:
        fs: FluidSynth instance
        time_per_beat: Duration of each beat in seconds
        tempo: Current tempo
        channel: MIDI channel to use for piano (default 10)
    """
    bar_count = 1
    total_bars = 12

    trip_spacing = get_trip_spacing(tempo)
    print(f"Piano starting on channel {channel}")
    chord_voicings = piano_chords["C7"]
    #chord_voicing = random.choice(chord_voicings)
    chord_voicing = chord_voicings[1]
    init_phrase(channel, fs, time_per_beat, trip_spacing, chord_voicing)
    
    while True:
        current_bar = bar_count % total_bars
        
        # Determine the current chord based on the bar
        if current_bar < 4:
            chord_voicings = piano_chords["C7"]  # I (C7)
        elif current_bar < 6:
            chord_voicings = piano_chords["F7"]  # IV (F7)
        elif current_bar < 8:
            chord_voicings = piano_chords["C7"]  # I (C7)
        elif current_bar == 8:
            chord_voicings = piano_chords["G7"]  # V (G7)
        elif current_bar == 9:
            chord_voicings = piano_chords["F7"]  # IV (F7)
        elif current_bar == 10:
            chord_voicings = piano_chords["C7"]  # I (C7)
        else:
            chord_voicings = piano_chords["G7"]  # V (G7) - Turnaround
        
        # Get a random voicing for this chord
        chord_voicing = random.choice(chord_voicings)
        
        # Choose and play a random phrase
        phrase_num = random.randint(1)  # Choose a random phrase between 1 and 3
        print(f"Playing piano phrase {phrase_num} on bar {current_bar}")


        if phrase_num == 1:
            phrase_one(channel, fs, time_per_beat, trip_spacing, chord_voicing)
        elif phrase_num == 2:
            phrase_two(channel, fs, time_per_beat, trip_spacing, chord_voicing)
        elif phrase_num == 3:
            phrase_three(channel, fs, time_per_beat, trip_spacing, chord_voicing)

        bar_count += 1
