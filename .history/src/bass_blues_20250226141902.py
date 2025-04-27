import fluidsynth
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

# Define the pattern (shuffle feel)
def play_bar(chord_notes):
    for note in chord_notes:
        midi_note = note_map[note]
        fs.noteon(0, midi_note, 100)
        time.sleep(0.4)  # Adjust for shuffle swing feel
        fs.noteoff(0, midi_note)
        time.sleep(0.1)  # Slight space for groove

# Play 12-bar blues
for _ in range(2):  # Two rounds of 12-bar blues
    for _ in range(4): play_bar(blues_progression[0])  # C chord
    for _ in range(2): play_bar(blues_progression[1])  # F chord
    for _ in range(2): play_bar(blues_progression[0])  # C chord
    play_bar(blues_progression[2])  # G chord
    play_bar(blues_progression[1])  # F chord
    play_bar(blues_progression[0])  # C chord
    play_bar(blues_progression[2])  # G chord (Turnaround)

# Cleanup
fs.delete()
