import time
from sync import instrument_sync, stop_event

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
    if not stop_event.is_set():
        instrument_sync.wait()
        time.sleep(time_per_beat)
        for note in chord:
            fs.noteon(channel, note, 70)
        time.sleep(time_per_beat)

        instrument_sync.wait()
        for note in chord:
            fs.noteon(channel, note, 70)
        time.sleep(time_per_beat)


#and of four
def phrase_one(channel, fs, time_per_beat, trip_spacing, chord):
    if not stop_event.is_set():
        print("phrase one")
        time.sleep(time_per_beat * (trip_spacing))
        for note in chord:
            fs.noteon(channel, note, 70)
        time.sleep(.0032)
        time.sleep(time_per_beat * (1-trip_spacing))
        instrument_sync.wait()
        time.sleep(time_per_beat * 2)
        time.sleep(.0032)
        instrument_sync.wait()
        time.sleep(time_per_beat)

#one and three
def phrase_two(channel, fs, time_per_beat, trip_spacing, chord):
    if not stop_event.is_set():
        print("phrase two")
        time.sleep(time_per_beat)
        time.sleep(.0032)
        instrument_sync.wait()
        for note in chord:
            fs.noteon(channel, note, 70)
        time.sleep(2 * time_per_beat)
        time.sleep(.0032)
        instrument_sync.wait()
        for note in chord:
            fs.noteon(channel, note, 70)
        time.sleep(time_per_beat)

#and of four, two, three and
def phrase_three(channel, fs, time_per_beat, trip_spacing, chord):
    if not stop_event.is_set():
        print("phrase 3")
        time.sleep(time_per_beat * (trip_spacing))
        for note in chord:
            fs.noteon(channel, note, 70)
        time.sleep(time_per_beat * (1-trip_spacing))
        time.sleep(.0032)
        instrument_sync.wait()
        time.sleep(time_per_beat)
        for note in chord:
            fs.noteon(channel, note, 70)
        time.sleep(time_per_beat)
        time.sleep(.0032)
        instrument_sync.wait()
        for note in chord:
            fs.noteon(channel, note, 70)
        time.sleep(time_per_beat * (trip_spacing))
        for note in chord:
            fs.noteon(channel, note, 70)
        time.sleep(time_per_beat * (1 - trip_spacing))
