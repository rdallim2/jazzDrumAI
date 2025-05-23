import time
import random
from time import sleep
import threading
import fluidsynth
import mido
import pygame.midi

from sync import instrument_sync

fs = fluidsynth.Synth()
fs.start(driver="coreaudio")

# MIDI note for Ride Cymbal (General MIDI standard)
RIDE_CYMBAL = 54
BASS_DRUM = 25
SNARE_DRUM = 37
H_TOM = 29
HI_HAT_CLOSED = 13
CRASH_SIZ_V1 = 7
CRASH_SIZ_V2 = 58
CRASH_SIZ_V3 = 9

def get_trip_spacing(tempo):
    spacing = .5 + (.666 - .5) * ((275 - tempo) / (275 - 200))
    if tempo < 200:
        return .666
    elif 200 <= tempo <= 275:
        print(f"Triplet spacing = {spacing}")
        return spacing
    elif tempo > 275:
        return .5
        
def swing_pattern(fs, time_per_beat, trip_spacing):
    instrument_sync.set()
    
    fs.noteon(0, BASS_DRUM, 15)  
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 70)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)    
    instrument_sync.clear()
    sleep(time_per_beat * (1 - trip_spacing))  


#--------------------------------- 8TH PATTERNS ENDING ON SNARE  ------------------------


def s8_s_one(fs, time_per_beat, trip_spacing):
    instrument_sync.set()

    fs.noteon(0, BASS_DRUM, 15)    
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, SNARE_DRUM, 50)
    sleep(time_per_beat * 1/3) 

    fs.noteon(0, BASS_DRUM, 15) 
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)    
    instrument_sync.clear()
    sleep(time_per_beat * (1 - trip_spacing))  


def s8_s_two(fs, time_per_beat, trip_spacing):
    instrument_sync.set()
    fs.noteon(0, BASS_DRUM, 15)  
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)
    fs.noteon(0, SNARE_DRUM, 50)    
    instrument_sync.clear()
    sleep(time_per_beat * (1 - trip_spacing))  


def s8_s_three(fs, time_per_beat, trip_spacing):
    instrument_sync.set()
    fs.noteon(0, BASS_DRUM, 15)    
    fs.noteon(0, RIDE_CYMBAL, 90)
    fs.noteon(0, SNARE_DRUM, 35)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, SNARE_DRUM, 50)
    sleep(time_per_beat * (1 - trip_spacing)) 

    fs.noteon(0, BASS_DRUM, 15) 
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)    
    instrument_sync.clear()
    sleep(time_per_beat * (1 - trip_spacing)) 


def s8_s_four(fs, time_per_beat, trip_spacing):
    instrument_sync.set()
    fs.noteon(0, BASS_DRUM, 15)  
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    fs.noteon(0, SNARE_DRUM, 35)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)
    fs.noteon(0, SNARE_DRUM, 50)    
    instrument_sync.clear()
    sleep(time_per_beat * (1 - trip_spacing))  


def s8_s_five(fs, time_per_beat, trip_spacing):
    instrument_sync.set()
    fs.noteon(0, BASS_DRUM, 15)    
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, BASS_DRUM, 50)
    sleep(time_per_beat * (1 - trip_spacing)) 

    fs.noteon(0, BASS_DRUM, 50)
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)
    fs.noteon(0, SNARE_DRUM, 50)    
    instrument_sync.clear()
    sleep(time_per_beat * (1 - trip_spacing)) 



def s8_s_six(fs, time_per_beat, trip_spacing):
    instrument_sync.set()
    fs.noteon(0, BASS_DRUM, 15)    
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, SNARE_DRUM, 50)
    sleep(time_per_beat * (1 - trip_spacing))

    fs.noteon(0, BASS_DRUM, 15)
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, SNARE_DRUM, 50)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)    
    instrument_sync.clear()
    sleep(time_per_beat * (1 - trip_spacing)) 



def s8_s_seven(fs, time_per_beat, trip_spacing):
    instrument_sync.set()
    fs.noteon(0, BASS_DRUM, 15)    
    fs.noteon(0, RIDE_CYMBAL, 90)
    fs.noteon(0, SNARE_DRUM, 35)
    sleep(time_per_beat)

    fs.noteon(0, BASS_DRUM, 15)
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)
    fs.noteon(0, SNARE_DRUM, 40)    
    instrument_sync.clear()
    sleep(time_per_beat * (1 - trip_spacing)) 


def s8_s_eight(fs, time_per_beat, trip_spacing):
    instrument_sync.set()
    fs.noteon(0, BASS_DRUM, 15)    
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, SNARE_DRUM, 45)
    sleep(time_per_beat * (1 - trip_spacing)) 

    fs.noteon(0, BASS_DRUM, 15)
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)
    fs.noteon(0, SNARE_DRUM, 50)    
    instrument_sync.clear()
    sleep(time_per_beat * (1 - trip_spacing)) 


#---------------------------------------- 8TH BASS DRUM BASS DRUM PHRASES ----------------------------
    
def s8_b_one(fs, time_per_beat, trip_spacing):   
    instrument_sync.set()
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, BASS_DRUM, 50)
    sleep(time_per_beat * (1 - trip_spacing)) 

    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)    
    instrument_sync.clear()
    sleep(time_per_beat * (1 - trip_spacing))  


def s8_b_two(fs, time_per_beat, trip_spacing):
    instrument_sync.set()
    print("four beat drum phrase")
    fs.noteon(0, BASS_DRUM, 15)  
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat) 
  
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)
    fs.noteon(0, BASS_DRUM, 50)    
    instrument_sync.clear()
    sleep(time_per_beat * (1 - trip_spacing))  


    instrument_sync.set()
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)    
    instrument_sync.clear()
    sleep(time_per_beat * (1 - trip_spacing)) 


def s8_b_three(fs, time_per_beat, trip_spacing):
    instrument_sync.set()
    fs.noteon(0, BASS_DRUM, 35)    
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, BASS_DRUM, 40)
    sleep(time_per_beat * (1 - trip_spacing)) 

    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)    
    instrument_sync.clear()
    sleep(time_per_beat * (1 - trip_spacing)) 


def s8_b_four(fs, time_per_beat, trip_spacing):
    instrument_sync.set()
    print("four beat drum phrase")
    fs.noteon(0, BASS_DRUM, 15)  
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 45)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)
    fs.noteon(0, BASS_DRUM, 40)    
    instrument_sync.clear()
    sleep(time_per_beat * (1 - trip_spacing))  


    instrument_sync.set()
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)    
    instrument_sync.clear()
    sleep(time_per_beat * (1 - trip_spacing)) 


def s8_b_five(fs, time_per_beat, trip_spacing):
    instrument_sync.set()
    print("four beat drum phrase")
    fs.noteon(0, BASS_DRUM, 15)    
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, SNARE_DRUM, 50)
    sleep(time_per_beat * (1 - trip_spacing)) 

    fs.noteon(0, SNARE_DRUM, 60)
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)
    fs.noteon(0, BASS_DRUM, 50)    
    instrument_sync.clear()
    sleep(time_per_beat * (1 - trip_spacing)) 

 
    instrument_sync.set()
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)    
    instrument_sync.clear()
    sleep(time_per_beat * (1 - trip_spacing)) 



def s8_b_six(fs, time_per_beat, trip_spacing):
    instrument_sync.set()
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, BASS_DRUM, 45)
    sleep(time_per_beat * (1 - trip_spacing)) 

    fs.noteon(0, BASS_DRUM, 55)
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)    
    instrument_sync.clear()
    sleep(time_per_beat * (1 - trip_spacing)) 



def s8_b_seven(fs, time_per_beat, trip_spacing):
    instrument_sync.set()
    print("four beat drum phrase")
    fs.noteon(0, BASS_DRUM, 40)    
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat)

    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)
    fs.noteon(0, BASS_DRUM, 45)    
    instrument_sync.clear()
    sleep(time_per_beat * (1 - trip_spacing)) 

  
    instrument_sync.set()
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)    
    instrument_sync.clear()
    sleep(time_per_beat * (1 - trip_spacing)) 


def s8_b_eight(fs, time_per_beat, trip_spacing):  
    instrument_sync.set()
    print("four beat drum phrase")
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, BASS_DRUM, 45)
    sleep(time_per_beat * (1 - trip_spacing)) 

    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)
    fs.noteon(0, BASS_DRUM, 50)    
    instrument_sync.clear()
    sleep(time_per_beat * (1 - trip_spacing)) 

 
    instrument_sync.set()
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)    
    instrument_sync.clear()
    sleep(time_per_beat * (1 - trip_spacing)) 



#-------------------------------8TH CRASH PHRASES ------------------------------------
    
def s8_crash_one(fs, time_per_beat, trip_spacing):
    instrument_sync.set()
    print("four beat drum phrase")
    fs.noteon(0, BASS_DRUM, 15)    
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, SNARE_DRUM, 55)
    sleep(time_per_beat * (1 - trip_spacing)) 

    fs.noteon(0, SNARE_DRUM, 70)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, CRASH_SIZ_V2, 90)
    fs.noteon(0, BASS_DRUM, 50)    
    instrument_sync.clear()
    sleep(time_per_beat * (1 - trip_spacing)) 


    instrument_sync.set()
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)    
    instrument_sync.clear()
    sleep(time_per_beat * (1 - trip_spacing)) 


def s8_crash_two(fs, time_per_beat, trip_spacing):
    instrument_sync.set()
    print("four beat drum phrase")
    fs.noteon(0, BASS_DRUM, 15)    
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, SNARE_DRUM, 50)
    sleep(time_per_beat * (1 - trip_spacing)) 

    fs.noteon(0, BASS_DRUM, 80)
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, CRASH_SIZ_V2, 85)
    fs.noteon(0, SNARE_DRUM, 70) 
    instrument_sync.clear()
    sleep(time_per_beat * (1 - trip_spacing))    


    instrument_sync.set()
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)    
    instrument_sync.clear()
    sleep(time_per_beat * (1 - trip_spacing)) 





#--------------------------------- TRIP SNARE PHRASES -----------------------------------
def t8_s_one(fs, time_per_beat):
    instrument_sync.set()
    fs.noteon(0, BASS_DRUM, 15)  
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 40)  
    sleep(time_per_beat * 2/3)  

    fs.noteon(0, BASS_DRUM, 15) 
    fs.noteon(0, SNARE_DRUM, 40)  
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 95)
    fs.noteon(0, SNARE_DRUM, 55)    
    instrument_sync.clear()
    sleep(time_per_beat * 1/3)  


def t8_s_two(fs, time_per_beat):
    instrument_sync.set()
    fs.noteon(0, BASS_DRUM, 15)  
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 45)  
    sleep(time_per_beat * 1/3)  
    fs.noteon(0, SNARE_DRUM, 50) 
    sleep(time_per_beat * 1/3) 

    fs.noteon(0, BASS_DRUM, 45)  
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 45)  
    sleep(time_per_beat * 1/3)  
    fs.noteon(0, RIDE_CYMBAL, 95)
    fs.noteon(0, SNARE_DRUM, 55)    
    instrument_sync.clear()
    sleep(time_per_beat * 1/3)  


def t8_s_three(fs, time_per_beat):
    instrument_sync.set()
    fs.noteon(0, BASS_DRUM, 15)  
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 45)  
    sleep(time_per_beat * 1/3)  
    fs.noteon(0, SNARE_DRUM, 50) 
    sleep(time_per_beat * 1/3) 

    fs.noteon(0, BASS_DRUM, 60)  
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3) 
    fs.noteon(0, RIDE_CYMBAL, 95)
    fs.noteon(0, SNARE_DRUM, 60)    
    instrument_sync.clear() 
    sleep(time_per_beat * 1/3) 



def t8_s_four(fs, time_per_beat):
    instrument_sync.set()
    fs.noteon(0, BASS_DRUM, 15)  
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 45)  
    sleep(time_per_beat * 1/3)  
    fs.noteon(0, BASS_DRUM, 50) 
    sleep(time_per_beat * 1/3) 

    fs.noteon(0, SNARE_DRUM, 65)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 95)    
    instrument_sync.clear()
    sleep(time_per_beat * 1/3)  



#---------------------------------- TRIP BASS DRUM PHRASES ----------------------
def t8_b_one(fs, time_per_beat):
    instrument_sync.set()
    fs.noteon(0, BASS_DRUM, 15)  
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 40)  
    sleep(time_per_beat * 2/3)  
 
    fs.noteon(0, SNARE_DRUM, 45)  
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 95)
    fs.noteon(0, BASS_DRUM, 60)    
    instrument_sync.clear()
    sleep(time_per_beat * 1/3)  


    instrument_sync.set()
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 95)    
    instrument_sync.clear()
    sleep(time_per_beat * 1/3) 


def t8_b_two(fs, time_per_beat):
    instrument_sync.set()
    fs.noteon(0, BASS_DRUM, 15)  
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 45)  
    sleep(time_per_beat * 1/3)  
    fs.noteon(0, SNARE_DRUM, 50) 
    sleep(time_per_beat * 1/3) 

    fs.noteon(0, BASS_DRUM, 45)  
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 45)  
    sleep(time_per_beat * 1/3)  
    fs.noteon(0, RIDE_CYMBAL, 95)
    fs.noteon(0, BASS_DRUM, 60)    
    instrument_sync.clear()
    sleep(time_per_beat * 1/3)  


    instrument_sync.set()
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 95)    
    instrument_sync.clear()
    sleep(time_per_beat * 1/3) 


def t8_b_three(fs, time_per_beat):
    instrument_sync.set()
    fs.noteon(0, BASS_DRUM, 15)  
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 45)  
    sleep(time_per_beat * 1/3)  
    fs.noteon(0, SNARE_DRUM, 50) 
    sleep(time_per_beat * 1/3) 

    fs.noteon(0, BASS_DRUM, 60)  
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3)  
    fs.noteon(0, RIDE_CYMBAL, 95)    
    instrument_sync.clear()
    sleep(time_per_beat * 1/3)  


def t8_b_four(fs, time_per_beat):
    instrument_sync.set()
    fs.noteon(0, BASS_DRUM, 15)  
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 45)  
    sleep(time_per_beat * 1/3)  
    fs.noteon(0, SNARE_DRUM, 50) 
    sleep(time_per_beat * 1/3) 

    fs.noteon(0, SNARE_DRUM, 60)  
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50) 
    sleep(time_per_beat * 2/3)  
    fs.noteon(0, RIDE_CYMBAL, 95)
    fs.noteon(0, BASS_DRUM, 60)    
    instrument_sync.clear()
    sleep(time_per_beat * 1/3)  

 
    instrument_sync.set()
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 95)    
    instrument_sync.clear()
    sleep(time_per_beat * 1/3) 



#---------------- TRIP CRASH PHRASES ----------------------------
    
def t8_crash_one(fs, time_per_beat):
    instrument_sync.set()
    fs.noteon(0, BASS_DRUM, 15)  
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 55)  
    sleep(time_per_beat * 1/3)  
    fs.noteon(0, BASS_DRUM, 60) 
    sleep(time_per_beat * 1/3) 

    fs.noteon(0, SNARE_DRUM, 60)  
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 65)  
    sleep(time_per_beat * 1/3)  
    fs.noteon(0, CRASH_SIZ_V2, 85)
    fs.noteon(0, BASS_DRUM, 80)    
    instrument_sync.clear()
    sleep(time_per_beat * 1/3)  

    instrument_sync.set()
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 95)    
    instrument_sync.clear()
    sleep(time_per_beat * 1/3) 


def t8_crash_two(fs, time_per_beat):
    instrument_sync.set()
    fs.noteon(0, BASS_DRUM, 15)  
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 45)  
    sleep(time_per_beat * 1/3)  
    fs.noteon(0, SNARE_DRUM, 55) 
    sleep(time_per_beat * 1/3) 

    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 65)  
    sleep(time_per_beat * 1/3)  
    fs.noteon(0, CRASH_SIZ_V2, 85)
    fs.noteon(0, BASS_DRUM, 80)    
    instrument_sync.clear()
    sleep(time_per_beat * 1/3)  


    instrument_sync.set()
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 95)    
    instrument_sync.clear()
    sleep(time_per_beat * 1/3) 


def t8_crash_three(fs, time_per_beat):
    instrument_sync.set()
    fs.noteon(0, BASS_DRUM, 15)  
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 45)  
    sleep(time_per_beat * 1/3)  
    fs.noteon(0, SNARE_DRUM, 55) 
    sleep(time_per_beat * 1/3) 

    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    fs.noteon(0, SNARE_DRUM, 70)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 75)  
    sleep(time_per_beat * 1/3)  
    fs.noteon(0, CRASH_SIZ_V2, 85)
    fs.noteon(0, BASS_DRUM, 80)    
    instrument_sync.clear()
    sleep(time_per_beat * 1/3)  


    instrument_sync.set()
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 95)    
    instrument_sync.clear()
    sleep(time_per_beat * 1/3) 