import fluidsynth
import random
import time

# Initialize FluidSynth
fs = fluidsynth.Synth()
fs.start()

# Load soundfont (update path if necessary)

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
def play_bar(time_per_beat, bars):
    """Plays a 12-bar blues cycle, randomly choosing notes from the given chord."""
    bar_count = 0
    while bar_count < bars:
        if bar_count < 4:
            chord = blues_progression[0]  # I (C)
        elif bar_count < 6:
            chord = blues_progression[1]  # IV (F)
        elif bar_count < 8:
            chord = blues_progression[0]  # I (C)
        elif bar_count == 8:
            chord = blues_progression[2]  # V (G)
        elif bar_count == 9:
            chord = blues_progression[1]  # IV (F)
        elif bar_count == 10:
            chord = blues_progression[0]  # I (C)
        else:
            chord = blues_progression[2]  # V (G) - Turnaround

        for _ in range(BEATS_PER_BAR):  # Play 4 notes per bar
            note = random.choice(chord)  # Choose a random note from the chord
            midi_note = note_map[note]
            fs.noteon(0, midi_note, 100)
            time.sleep(time_per_beat))  # Hold the note
            fs.noteoff(0, midi_note)
            time.sleep(0.1)  # Slight gap for groove

        bar_count += 1  # Move to the next bar


# Cleanup
fs.delete()
