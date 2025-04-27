import time
from test_kivy_app import bar_ready, sync

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
    time.sleep(time_per_beat)  # Beat 1
    
    sync.wait_for_beat()  # Wait on beat 2
    for note in chord:
        fs.noteon(channel, note, 70)
    time.sleep(time_per_beat)
    
    for note in chord:  # Beat 3
        fs.noteon(channel, note, 70)
    time.sleep(time_per_beat)
    
    sync.wait_for_beat()  # Wait on beat 4
    time.sleep(time_per_beat)

#and of four
def phrase_one(channel, fs, time_per_beat, trip_spacing, chord):
    print("phrase one")
    time.sleep(time_per_beat * (trip_spacing))
    for note in chord:
        fs.noteon(channel, note, 70)
    time.sleep(time_per_beat * (1-trip_spacing))
    sync.wait_for_beat()
    time.sleep(time_per_beat * 2)
    sync.wait_for_beat()
    time.sleep(time_per_beat)

#one and three
def phrase_two(channel, fs, time_per_beat, trip_spacing, chord):
    print("phrase two")
    for note in chord:  # Beat 1
        fs.noteon(channel, note, 70)
    time.sleep(time_per_beat)
    
    sync.wait_for_beat()  # Wait on beat 2
    time.sleep(time_per_beat)
    
    for note in chord:  # Beat 3
        fs.noteon(channel, note, 70)
    time.sleep(time_per_beat)
    
    sync.wait_for_beat()  # Wait on beat 4
    time.sleep(time_per_beat)

#and of four, two, three and
def phrase_three(channel, fs, time_per_beat, trip_spacing, chord):
    print("phrase 3")
    time.sleep(time_per_beat * trip_spacing)  # Beat 1
    for note in chord:
        fs.noteon(channel, note, 70)
    time.sleep(time_per_beat * (1-trip_spacing))
    
    sync.wait_for_beat()  # Wait on beat 2
    for note in chord:
        fs.noteon(channel, note, 70)
    time.sleep(time_per_beat)
    
    for note in chord:  # Beat 3
        fs.noteon(channel, note, 70)
    time.sleep(time_per_beat * trip_spacing)
    for note in chord:
        fs.noteon(channel, note, 70)
    time.sleep(time_per_beat * (1 - trip_spacing))
    
    sync.wait_for_beat()  # Wait on beat 4
    time.sleep(time_per_beat)
