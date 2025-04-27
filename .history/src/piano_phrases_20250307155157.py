import time
from sync_utils_new import clock as music_clock

def get_trip_spacing(tempo):
    spacing = .5 + (.666 - .5) * ((275 - tempo) / (275 - 200))
    if tempo < 200:
        return .666
    elif 200 <= tempo <= 275:
        print(f"Triplet spacing = {spacing}")
        return spacing
    elif tempo > 275:
        return .5

# 2 and 3
def init_phrase(channel, fs, time_per_beat, trip_spacing, chord):
    time.sleep(time_per_beat)
    for note in chord:
        fs.noteon(channel, note, 70)
    print("phrase init")
    time.sleep(time_per_beat)
    for note in chord:
        fs.noteon(channel, note, 70)
    time.sleep(time_per_beat)

#and of four
def phrase_one(channel, fs, time_per_beat, trip_spacing, chord_voicing):
    """Play a basic comping pattern"""
    for note in chord_voicing:
        fs.noteon(channel, note, 100)
    time.sleep(time_per_beat * 0.95)
    for note in chord_voicing:
        fs.noteoff(channel, note)
    time.sleep(time_per_beat * 0.05)

#one and three
def phrase_two(channel, fs, time_per_beat, trip_spacing, chord_voicing):
    """Play a syncopated comping pattern"""
    time.sleep(time_per_beat * 0.5)  # Wait for half a beat
    for note in chord_voicing:
        fs.noteon(channel, note, 100)
    time.sleep(time_per_beat * 0.45)
    for note in chord_voicing:
        fs.noteoff(channel, note)
    time.sleep(time_per_beat * 0.05)

#and of four, two, three and
def phrase_three(channel, fs, time_per_beat, trip_spacing, chord_voicing):
    """Play a triplet-based comping pattern"""
    time.sleep(time_per_beat * 0.33)  # First triplet
    for note in chord_voicing:
        fs.noteon(channel, note, 100)
    time.sleep(time_per_beat * 0.33)  # Second triplet
    for note in chord_voicing:
        fs.noteoff(channel, note)
    time.sleep(time_per_beat * 0.34)  # Third triplet
