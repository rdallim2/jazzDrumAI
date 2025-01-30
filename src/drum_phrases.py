import time
from time import sleep
import fluidsynth

fs = fluidsynth.Synth()
fs.start(driver="coreaudio")

# MIDI note for Ride Cymbal (General MIDI standard)
RIDE_CYMBAL = 51
BASS_DRUM = 35
SNARE_DRUM = 38
HI_HAT_CLOSED = 42

def swing_pattern(fs, time_per_beat):
    fs.noteon(0, BASS_DRUM, 40)  
    fs.noteon(0, RIDE_CYMBAL, 100)
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 40) 
    fs.noteon(0, RIDE_CYMBAL, 100)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 75)
    sleep(time_per_beat * 1/3)  

def phrase_one(fs, time_per_beat):
    fs.noteon(0, BASS_DRUM, 40)  
    fs.noteon(0, RIDE_CYMBAL, 100)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, SNARE_DRUM, 60)
    sleep(time_per_beat * 1/3) 

    fs.noteon(0, BASS_DRUM, 110) 
    fs.noteon(0, RIDE_CYMBAL, 100)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 75)
    sleep(time_per_beat * 1/3)  

def phrase_two(fs, time_per_beat):
    fs.noteon(0, BASS_DRUM, 40)  
    fs.noteon(0, RIDE_CYMBAL, 100)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 30)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 60)
    sleep(time_per_beat * 1/3)

    fs.noteon(0, BASS_DRUM, 90) 
    fs.noteon(0, RIDE_CYMBAL, 100)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 30)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 60)
    fs.noteon(0, RIDE_CYMBAL, 75)
    sleep(time_per_beat * 1/3)  


def phrase_three(fs, time_per_beat):
    fs.noteon(0, BASS_DRUM, 40)  
    fs.noteon(0, RIDE_CYMBAL, 100)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 30)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 60)
    sleep(time_per_beat * 1/3)

    fs.noteon(0, BASS_DRUM, 110) 
    fs.noteon(0, RIDE_CYMBAL, 100)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 75)
    sleep(time_per_beat * 1/3)

def phrase_four(fs, time_per_beat):
    fs.noteon(0, BASS_DRUM, 85)  
    fs.noteon(0, RIDE_CYMBAL, 100)
    sleep(time_per_beat) 
    
    fs.noteon(0, RIDE_CYMBAL, 100)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 2/3)    
    fs.noteon(0, BASS_DRUM, 85) 
    fs.noteon(0, RIDE_CYMBAL, 75)
    sleep(time_per_beat * 1/3)  

def phrase_five(fs, time_per_beat):
    fs.noteon(0, BASS_DRUM, 40)  
    fs.noteon(0, RIDE_CYMBAL, 100)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, SNARE_DRUM, 70)
    sleep(time_per_beat * 1/3)

    fs.noteon(0, BASS_DRUM, 40)
    fs.noteon(0, RIDE_CYMBAL, 100)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 75)
    sleep(time_per_beat * 1/3)  

def phrase_six(fs, time_per_beat):
    fs.noteon(0, RIDE_CYMBAL, 100)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, BASS_DRUM, 80)  
    sleep(time_per_beat * 1/3)


    fs.noteon(0, RIDE_CYMBAL, 100)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 75)
    sleep(time_per_beat * 1/3) 

def phrase_seven(fs, time_per_beat): 
    fs.noteon(0, RIDE_CYMBAL, 100)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 40)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, BASS_DRUM, 70)
    sleep(time_per_beat * 1/3)

    fs.noteon(0, SNARE_DRUM, 40) 
    fs.noteon(0, RIDE_CYMBAL, 100)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 40)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, BASS_DRUM, 70)
    fs.noteon(0, RIDE_CYMBAL, 75)
    sleep(time_per_beat * 1/3)  

def phrase_eight(fs, time_per_beat):
    fs.noteon(0, BASS_DRUM, 40)  
    fs.noteon(0, RIDE_CYMBAL, 100)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 70) 
    sleep(time_per_beat * 2/3)

    fs.noteon(0, BASS_DRUM, 40) 
    fs.noteon(0, SNARE_DRUM, 70) 
    fs.noteon(0, RIDE_CYMBAL, 100)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 75)
    fs.noteon(0, SNARE_DRUM, 70) 
    sleep(time_per_beat * 1/3)  