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

    #get all the nums of thirds and 7ths, put in a list
    
    #select the num from the list which is closest to current left pinky,

    #if 7th, build 3rd and 5th on top
    #else (3rd), build 7 and 9 on top, 

    # for right hand, if 735, build 9, 6 or root on top
    #if 379, build 5, root, 6 on top 
    