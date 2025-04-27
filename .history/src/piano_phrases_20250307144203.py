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
    time.sleep(time_per_beat)
    for note in chord:
        fs.noteon(channel, note, 70)
    print("shoudlve heard something in the piano")
    time.sleep(time_per_beat)
    for note in chord:
        fs.noteon(channel, note, 70)
    time.sleep(time_per_beat)

#and of four
def phrase_one(channel, fs, time_per_beat, trip_spacing, chord):
    time.sleep(time_per_beat * (trip_spacing))
    for note in chord:
        fs.noteon(channel, note, 70)
    time.sleep(time_per_beat * (1-trip_spacing) + 3 * time_per_beat)
    for note in chord:
        fs.noteoff(channel, note)

#one and three
def phrase_two(channel, fs, time_per_beat, trip_spacing, chord):
    time.sleep(time_per_beat)
    for note in chord:
        fs.noteon(channel, note, 70)
    time.sleep(2 * time_per_beat)
    for note in chord:
        fs.noteoff(channel, note)
    for note in chord:
        fs.noteon(channel, note, 70)
    time.sleep
    for note in chord:
        fs.noteoff(channel, note)

def phrase_three(channel, fs, time_per_beat, trip_spacing, chord):
    time.sleep(time_per_beat * (trip_spacing))
    for note in chord:
        fs.noteon(channel, note, 70)
    time.sleep(time_per_beat * (1-trip_spacing) +  time_per_beat)
    for note in chord:
        fs.noteon(channel, note, 70)
    time.sleep(time_per_beat)
    for note in chord:
        fs.noteon(channel, note, 70)
    time.sleep(time_per_beat * (trip_spacing))
    for note in chord:
        fs.noteon(channel, note, 70)
    time.sleep(time_per_beat * (1 - time_per_beat))
