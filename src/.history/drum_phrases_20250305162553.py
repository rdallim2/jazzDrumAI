import time
import random
from time import sleep
import threading
import fluidsynth
import mido
import pygame.midi


fs = fluidsynth.Synth()
fs.start(driver="coreaudio")

# MIDI note for Ride Cymbal (General MIDI standard)
RIDE_CYMBAL = 3
BASS_DRUM = 25
SNARE_DRUM = 37
H_TOM = 29
HI_HAT_CLOSED = 13
CRASH_SIZ_V1 = 7
CRASH_SIZ_V2 = 8
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
    fs.noteon(0, BASS_DRUM, 15)  
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 70)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)
    sleep(time_per_beat * (1 - trip_spacing))  


#--------------------------------- 8TH PATTERNS ENDING ON SNARE  ------------------------


def s8_s_one(fs, time_per_beat, trip_spacing):
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
    sleep(time_per_beat * (1 - trip_spacing))  

def s8_s_two(fs, time_per_beat, trip_spacing):
    fs.noteon(0, BASS_DRUM, 15)  
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)
    fs.noteon(0, SNARE_DRUM, 50)
    sleep(time_per_beat * (1 - trip_spacing))  

def s8_s_three(fs, time_per_beat, trip_spacing):
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
    sleep(time_per_beat * (1 - trip_spacing)) 

def s8_s_four(fs, time_per_beat, trip_spacing):
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
    sleep(time_per_beat * (1 - trip_spacing))  

def s8_s_five(fs, time_per_beat, trip_spacing):
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
    sleep(time_per_beat * (1 - trip_spacing)) 


def s8_s_six(fs, time_per_beat, trip_spacing):
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
    sleep(time_per_beat * (1 - trip_spacing)) 


def s8_s_seven(fs, time_per_beat, trip_spacing):
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
    sleep(time_per_beat * (1 - trip_spacing)) 

def s8_s_eight(fs, time_per_beat, trip_spacing):
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
    sleep(time_per_beat * (1 - trip_spacing)) 

#---------------------------------------- 8TH BASS DRUM BASS DRUM PHRASES ----------------------------
    
def s8_b_one(fs, time_per_beat, trip_spacing):   
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, BASS_DRUM, 50)
    sleep(time_per_beat * (1 - trip_spacing)) 

    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)
    sleep(time_per_beat * (1 - trip_spacing))  

def s8_b_two(fs, time_per_beat, trip_spacing):
    fs.noteon(0, BASS_DRUM, 15)  
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat) 
  
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)
    fs.noteon(0, BASS_DRUM, 50)
    sleep(time_per_beat * (1 - trip_spacing))  
 
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)
    sleep(time_per_beat * (1 - trip_spacing)) 

def s8_b_three(fs, time_per_beat, trip_spacing):
    fs.noteon(0, BASS_DRUM, 35)    
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, BASS_DRUM, 40)
    sleep(time_per_beat * (1 - trip_spacing)) 

    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)
    sleep(time_per_beat * (1 - trip_spacing)) 

def s8_b_four(fs, time_per_beat, trip_spacing):
    fs.noteon(0, BASS_DRUM, 15)  
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 45)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * trip_spacing)
    fs.noteon(0, RIDE_CYMBAL, 95)
    fs.noteon(0, BASS_DRUM, 40)
    sleep(time_per_beat * (1 - trip_spacing))  

    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 95)
    sleep(time_per_beat * 1/3) 

def s8_b_five(fs, time_per_beat):
    fs.noteon(0, BASS_DRUM, 15)    
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, SNARE_DRUM, 50)
    sleep(time_per_beat * 1/3) 

    fs.noteon(0, SNARE_DRUM, 60)
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 95)
    fs.noteon(0, BASS_DRUM, 50)
    sleep(time_per_beat * 1/3) 
 
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 95)
    sleep(time_per_beat * 1/3) 


def s8_b_six(fs, time_per_beat):
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, BASS_DRUM, 45)
    sleep(time_per_beat * 1/3) 

    fs.noteon(0, BASS_DRUM, 55)
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 95)
    sleep(time_per_beat * 1/3) 


def s8_b_seven(fs, time_per_beat):
    fs.noteon(0, BASS_DRUM, 40)    
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat)

    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 95)
    fs.noteon(0, BASS_DRUM, 45)
    sleep(time_per_beat * 1/3) 
  
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 95)
    sleep(time_per_beat * 1/3) 

def s8_b_eight(fs, time_per_beat):  
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, BASS_DRUM, 45)
    sleep(time_per_beat * 1/3) 

    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 95)
    fs.noteon(0, BASS_DRUM, 50)
    sleep(time_per_beat * 1/3) 
 
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 95)
    sleep(time_per_beat * 1/3) 


#-------------------------------8TH CRASH PHRASES ------------------------------------
    
def s8_crash_one(fs, time_per_beat):
    fs.noteon(0, BASS_DRUM, 15)    
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, SNARE_DRUM, 55)
    sleep(time_per_beat * 1/3) 

    fs.noteon(0, SNARE_DRUM, 70)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, CRASH_SIZ_V2, 115)
    fs.noteon(0, BASS_DRUM, 50)
    sleep(time_per_beat * 1/3) 

    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 95)
    sleep(time_per_beat * 1/3) 

def s8_crash_two(fs, time_per_beat):
    fs.noteon(0, BASS_DRUM, 15)    
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, SNARE_DRUM, 50)
    sleep(time_per_beat * 1/3) 

    fs.noteon(0, BASS_DRUM, 80)
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, CRASH_SIZ_V2, 110)
    fs.noteon(0, SNARE_DRUM, 70)
    sleep(time_per_beat * 1/3) 

    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 95)
    sleep(time_per_beat * 1/3) 




#--------------------------------- TRIP SNARE PHRASES -----------------------------------
def t8_s_one(fs, time_per_beat):
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
    sleep(time_per_beat * 1/3)  

def t8_s_two(fs, time_per_beat):
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
    sleep(time_per_beat * 1/3)  

def t8_s_three(fs, time_per_beat):
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
    sleep(time_per_beat * 1/3)  


def t8_s_four(fs, time_per_beat):
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
    sleep(time_per_beat * 1/3)  


#---------------------------------- TRIP BASS DRUM PHRASES ----------------------
def t8_b_one(fs, time_per_beat):
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
    sleep(time_per_beat * 1/3)  

    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 95)
    sleep(time_per_beat * 1/3) 

def t8_b_two(fs, time_per_beat):
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
    sleep(time_per_beat * 1/3)  

    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 95)
    sleep(time_per_beat * 1/3) 

def t8_b_three(fs, time_per_beat):
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
    sleep(time_per_beat * 1/3)  

def t8_b_four(fs, time_per_beat):
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
    sleep(time_per_beat * 1/3)  
 
    fs.noteon(0, RIDE_CYMBAL, 90)
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 95)
    sleep(time_per_beat * 1/3) 


#---------------- TRIP CRASH PHRASES ----------------------------
    
def t8_crash_one(fs, time_per_beat):
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
    fs.noteon(0, CRASH_SIZ_V2, 110)
    fs.noteon(0, BASS_DRUM, 80)
    sleep(time_per_beat * 1/3)  

    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 95)
    sleep(time_per_beat * 1/3) 

def t8_crash_two(fs, time_per_beat):
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
    fs.noteon(0, CRASH_SIZ_V2, 110)
    fs.noteon(0, BASS_DRUM, 80)
    sleep(time_per_beat * 1/3)  

    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 15)   
    fs.noteon(0, RIDE_CYMBAL, 105)
    fs.noteon(0, HI_HAT_CLOSED, 50)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 95)
    sleep(time_per_beat * 1/3) 


#------------------------------- MISC ----------------------------

def phrase_two(fs, time_per_beat):
    fs.noteon(0, BASS_DRUM, 25)    
    fs.noteon(0, RIDE_CYMBAL, 115)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 30)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 60)
    sleep(time_per_beat * 1/3)

    fs.noteon(0, BASS_DRUM, 90) 
    fs.noteon(0, RIDE_CYMBAL, 127)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 30)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 60)
    fs.noteon(0, RIDE_CYMBAL, 100)
    sleep(time_per_beat * 1/3)  


def phrase_three(fs, time_per_beat):
    fs.noteon(0, BASS_DRUM, 25)    
    fs.noteon(0, RIDE_CYMBAL, 115)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 30)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 60)
    sleep(time_per_beat * 1/3)

    fs.noteon(0, BASS_DRUM, 110) 
    fs.noteon(0, RIDE_CYMBAL, 127)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 100)
    sleep(time_per_beat * 1/3)

def phrase_four(fs, time_per_beat):
    fs.noteon(0, BASS_DRUM, 85)  
    fs.noteon(0, RIDE_CYMBAL, 115)
    sleep(time_per_beat) 
    
    fs.noteon(0, RIDE_CYMBAL, 127)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 2/3)    
    fs.noteon(0, BASS_DRUM, 85) 
    fs.noteon(0, RIDE_CYMBAL, 100)
    sleep(time_per_beat * 1/3)  

def phrase_five(fs, time_per_beat):
    fs.noteon(0, BASS_DRUM, 25)    
    fs.noteon(0, RIDE_CYMBAL, 115)
    sleep(time_per_beat)

    fs.noteon(0, BASS_DRUM, 25)  
    fs.noteon(0, RIDE_CYMBAL, 127)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, SNARE_DRUM, 70)
    fs.noteon(0, RIDE_CYMBAL, 100)
    sleep(time_per_beat * 1/3)  

def phrase_six(fs, time_per_beat):
    fs.noteon(0, RIDE_CYMBAL, 115)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, BASS_DRUM, 80)  
    sleep(time_per_beat * 1/3)


    fs.noteon(0, RIDE_CYMBAL, 127)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 100)
    sleep(time_per_beat * 1/3) 

def phrase_seven(fs, time_per_beat): 
    fs.noteon(0, RIDE_CYMBAL, 115)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 40)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, BASS_DRUM, 70)
    sleep(time_per_beat * 1/3)

    fs.noteon(0, SNARE_DRUM, 40) 
    fs.noteon(0, RIDE_CYMBAL, 127)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 40)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, BASS_DRUM, 70)
    fs.noteon(0, RIDE_CYMBAL, 100)
    sleep(time_per_beat * 1/3)  

def phrase_eight(fs, time_per_beat):
    fs.noteon(0, BASS_DRUM, 40)  
    fs.noteon(0, RIDE_CYMBAL, 115)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 45) 
    sleep(time_per_beat * 2/3)

    fs.noteon(0, BASS_DRUM, 40) 
    fs.noteon(0, SNARE_DRUM, 45) 
    fs.noteon(0, RIDE_CYMBAL, 127)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 100)
    fs.noteon(0, SNARE_DRUM, 90) 
    sleep(time_per_beat * 1/3)  

#-------------------  SLOW PHRASES --------------------------
    

def phrase_nine(fs, time_per_beat):
    fs.noteon(0, BASS_DRUM, 40)  
    fs.noteon(0, RIDE_CYMBAL, 100)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 40)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 50)
    sleep(time_per_beat * 1/3)

    fs.noteon(0, BASS_DRUM, 40) 
    fs.noteon(0, RIDE_CYMBAL, 115)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 75)
    sleep(time_per_beat * 1/3)

def phrase_ten(fs, time_per_beat): 
    fs.noteon(0, BASS_DRUM, 40)  
    fs.noteon(0, RIDE_CYMBAL, 100)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 40)
    sleep(time_per_beat * 1/3) 
    fs.noteon(0, SNARE_DRUM, 50)
    sleep(time_per_beat * 1/3) 

    fs.noteon(0, SNARE_DRUM, 70) 
    fs.noteon(0, RIDE_CYMBAL, 115)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 75)
    fs.noteon(0, BASS_DRUM, 90)
    sleep(time_per_beat * 1/3)  

def phrase_eleven(fs, time_per_beat):
    fs.noteon(0, BASS_DRUM, 40)  
    fs.noteon(0, RIDE_CYMBAL, 100)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 30)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 60)
    sleep(time_per_beat * 1/3)

    fs.noteon(0, BASS_DRUM, 90) 
    fs.noteon(0, RIDE_CYMBAL, 115)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 30)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, BASS_DRUM, 90)
    fs.noteon(0, RIDE_CYMBAL, 75)
    sleep(time_per_beat * 1/3)  

def phrase_twelve(fs, time_per_beat):
    fs.noteon(0, BASS_DRUM, 40)  
    fs.noteon(0, RIDE_CYMBAL, 100)
    fs.noteon(0, SNARE_DRUM, 50)    
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 40)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, BASS_DRUM, 90) 
    sleep(time_per_beat * 1/3)


    fs.noteon(0, RIDE_CYMBAL, 115)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 30)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 45)
    fs.noteon(0, RIDE_CYMBAL, 75)
    sleep(time_per_beat * 1/3)  

#--------------------- FAST PHRASES -----------------------------
    
def f_swing_pattern(fs, time_per_beat):
    fs.noteon(0, BASS_DRUM, 30)  
    fs.noteon(0, RIDE_CYMBAL, 115)
    sleep(time_per_beat) 

    fs.noteon(0, BASS_DRUM, 30) 
    fs.noteon(0, RIDE_CYMBAL, 127)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 7/12)
    fs.noteon(0, RIDE_CYMBAL, 100)
    sleep(time_per_beat * 5/12) 

def f_phrase_one(fs, time_per_beat):
    fs.noteon(0, BASS_DRUM, 30)  
    fs.noteon(0, RIDE_CYMBAL, 115)
    sleep(time_per_beat * 7/12)
    fs.noteon(0, SNARE_DRUM, 60)
    sleep(time_per_beat * 5/12) 

    fs.noteon(0, BASS_DRUM, 110) 
    fs.noteon(0, RIDE_CYMBAL, 127)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 7/12)
    fs.noteon(0, RIDE_CYMBAL, 100)
    sleep(time_per_beat * 5/12)  

def f_phrase_three(fs, time_per_beat):
    fs.noteon(0, BASS_DRUM, 30)  
    fs.noteon(0, RIDE_CYMBAL, 115)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 30)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 60)
    sleep(time_per_beat * 1/3)

    fs.noteon(0, BASS_DRUM, 110) 
    fs.noteon(0, RIDE_CYMBAL, 127)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 7/12)
    fs.noteon(0, RIDE_CYMBAL, 100)
    sleep(time_per_beat * 5/12)

def f_phrase_five(fs, time_per_beat):
    fs.noteon(0, BASS_DRUM, 30)  
    fs.noteon(0, RIDE_CYMBAL, 115)
    sleep(time_per_beat)

    fs.noteon(0, BASS_DRUM, 30)
    fs.noteon(0, RIDE_CYMBAL, 127)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 7/12)
    fs.noteon(0, RIDE_CYMBAL, 100)
    fs.noteon(0, SNARE_DRUM, 70)
    sleep(time_per_beat * 5/12)  

def f_phrase_six(fs, time_per_beat):
    fs.noteon(0, RIDE_CYMBAL, 115)
    sleep(time_per_beat * 7/12)
    fs.noteon(0, BASS_DRUM, 80)  
    sleep(time_per_beat * 5/12)


    fs.noteon(0, RIDE_CYMBAL, 127)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 7/12)
    fs.noteon(0, RIDE_CYMBAL, 100)
    sleep(time_per_beat * 5/12) 
    
def f_phrase_thirteen(fs, time_per_beat): 
    fs.noteon(0, BASS_DRUM, 30)  
    fs.noteon(0, RIDE_CYMBAL, 100)
    sleep(time_per_beat * 7/12)
    fs.noteon(0, SNARE_DRUM, 60)
    sleep(time_per_beat * 5/12) 

    fs.noteon(0, SNARE_DRUM, 70) 
    fs.noteon(0, RIDE_CYMBAL, 115)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 7/12)
    fs.noteon(0, RIDE_CYMBAL, 75)
    fs.noteon(0, BASS_DRUM, 90)
    sleep(time_per_beat * 5/12) 

def f_phrase_fourteen(fs, time_per_beat):
    fs.noteon(0, BASS_DRUM, 30)  
    fs.noteon(0, RIDE_CYMBAL, 100)
    sleep(time_per_beat * 7/12)
    fs.noteon(0, SNARE_DRUM, 60)
    sleep(time_per_beat * 5/12) 

    fs.noteon(0, SNARE_DRUM, 80) 
    fs.noteon(0, RIDE_CYMBAL, 115)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    fs.noteon(0, BASS_DRUM, 30)
    sleep(time_per_beat * 7/12)
    fs.noteon(0, RIDE_CYMBAL, 75)
    sleep(time_per_beat * 5/12)  

def f_phrase_fifteen(fs, time_per_beat):
    fs.noteon(0, BASS_DRUM, 30)  
    fs.noteon(0, RIDE_CYMBAL, 100)
    fs.noteon(0, SNARE_DRUM, 70)
    sleep(time_per_beat * 7/12)
    fs.noteon(0, SNARE_DRUM, 65)
    sleep(time_per_beat * 5/12)

    fs.noteon(0, BASS_DRUM, 30) 
    fs.noteon(0, RIDE_CYMBAL, 115)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 7/12)
    fs.noteon(0, RIDE_CYMBAL, 75)
    sleep(time_per_beat * 5/12)

def f_phrase_sixteen(fs, time_per_beat): 
    fs.noteon(0, RIDE_CYMBAL, 100)
    sleep(time_per_beat * 7/12)
    fs.noteon(0, BASS_DRUM, 80)
    sleep(time_per_beat * 5/12) 

    fs.noteon(0, BASS_DRUM, 100) 
    fs.noteon(0, RIDE_CYMBAL, 115)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 7/12)
    fs.noteon(0, RIDE_CYMBAL, 75)
    sleep(time_per_beat * 5/12) 

#------------------------ LEGATO/BIG PHRASES FOR CRASHING/ACCENTUATION --------------
    
def d_phrase_five(fs, time_per_beat):
    fs.noteon(0, BASS_DRUM, 40)  
    fs.noteon(0, RIDE_CYMBAL, 115)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, SNARE_DRUM, 70)
    sleep(time_per_beat * 1/3)

    fs.noteon(0, RIDE_CYMBAL, 115)
    fs.noteon(0, BASS_DRUM, 90) 
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, SNARE_DRUM, 70)
    fs.noteon(0, CRASH_SIZ_V2, 100)
    sleep(time_per_beat)   

    fs.noteon(0, SNARE_DRUM, 60)
    sleep(time_per_beat * 1/3) 

    fs.noteon(0, SNARE_DRUM, 80) 
    fs.noteon(0, RIDE_CYMBAL, 127)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 100)
    sleep(time_per_beat * 1/3)  


    
def d_phrase_eight(fs, time_per_beat):
    fs.noteon(0, BASS_DRUM, 40)  
    fs.noteon(0, RIDE_CYMBAL, 115)
    sleep(time_per_beat * 1/3)
    fs.noteon(0, SNARE_DRUM, 45) 
    sleep(time_per_beat * 2/3)

    fs.noteon(0, BASS_DRUM, 40) 
    fs.noteon(0, SNARE_DRUM, 45) 
    fs.noteon(0, RIDE_CYMBAL, 127)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, CRASH_SIZ_V2, 100)
    fs.noteon(0, SNARE_DRUM, 90) 
    sleep(time_per_beat * 4/3)

    fs.noteon(0, BASS_DRUM, 40) 
    fs.noteon(0, RIDE_CYMBAL, 127)
    fs.noteon(0, HI_HAT_CLOSED, 80)
    sleep(time_per_beat * 2/3)
    fs.noteon(0, RIDE_CYMBAL, 100)
    sleep(time_per_beat * 1/3)  


