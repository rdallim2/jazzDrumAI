import random
import time

from piano_phrases import *
from chord_scale_maps import * 

def next_voicing(last_voicing, next_chord):
    #get the key number of the left pinky
    l_pinky = last_voicing[0]
    
    #get third and 7th of upcoming chord
    third = next_chord[1]
    seventh = next_chord[3]

    
    