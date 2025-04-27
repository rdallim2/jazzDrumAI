import time

def get_trip_spacing(tempo):
    spacing = .5 + (.666 - .5) * ((350 - tempo) / (350 - 250))
    if tempo < 250:
        return .666
    elif 250 <= tempo <= 350:
        print(f"Triplet spacing = {spacing}")
        return spacing
    elif tempo > 350:
        return .5

# 2 and 3
def init_phrase(channel, fs, time_per_beat, trip_spacing, chord):
    # Play on beat 2 and 3 of the first bar
    time.sleep(time_per_beat)  # Wait for beat 2
    for note in chord:
        fs.noteon(channel, note, 70)
    time.sleep(time_per_beat)  # Wait for beat 3
    for note in chord:
        fs.noteon(channel, note, 70)
    time.sleep(time_per_beat * 2)  # Wait for remaining beats

#and of four
def phrase_one(channel, fs, time_per_beat, trip_spacing, chord):
    # Play on the 'and' of beat 4
    time.sleep(time_per_beat * 3)  # Wait for first three beats
    time.sleep(time_per_beat * trip_spacing)  # Wait for the 'and'
    for note in chord:
        fs.noteon(channel, note, 70)
    time.sleep(time_per_beat * (1-trip_spacing))  # Wait for remaining time

#one and three
def phrase_two(channel, fs, time_per_beat, trip_spacing, chord):
    # Play on beats 1 and 3
    for note in chord:
        fs.noteon(channel, note, 70)
    time.sleep(time_per_beat * 2)  # Wait for beat 3
    for note in chord:
        fs.noteon(channel, note, 70)
    time.sleep(time_per_beat * 2)  # Wait for remaining beats

def phrase_three(channel, fs, time_per_beat, trip_spacing, chord):
    # More complex pattern over one bar
    time.sleep(time_per_beat)  # Wait for beat 2
    for note in chord:
        fs.noteon(channel, note, 70)
    time.sleep(time_per_beat)  # Wait for beat 3
    for note in chord:
        fs.noteon(channel, note, 70)
    time.sleep(time_per_beat)  # Wait for beat 4
    for note in chord:
        fs.noteon(channel, note, 70)
    time.sleep(time_per_beat)  # Wait for end of bar
