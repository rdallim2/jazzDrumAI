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

def init_phrase(channel, fs, time_per_beat, trip_spacing, chord):
    time.sleep(time_per_beat)
    for note in chord:
        fs.noteon(channel, note, 70)