import time
import random
from time import sleep
import fluidsynth

from drum_phrases import swing_pattern, phrase_one, phrase_two, phrase_three, phrase_four, phrase_five, phrase_six, phrase_seven, phrase_eight
# Initialize the synthesizer
fs = fluidsynth.Synth()
fs.start(driver="coreaudio")

try:
    sfid = fs.sfload("FluidR3_GM.sf2")
    if sfid == -1:
        raise Exception("Failed to load soundfont")
    fs.sfont_select(0, sfid)
    fs.program_select(0, sfid, 128, 0)
except Exception as e:
    print(f"Error loading soundfont: {e}")

    

# Start the synthesizer
#fs.start()
#soundfont = "FluidR3_GM.sf2"

#fs.sfload(soundfont)

# Function to play the ride cymbal at regular intervals
def play_ride_cymbal(tempo):
    time_per_beat = 60 / tempo  # Time per quarter note in seconds

    while True:    
        phrase_two(fs, time_per_beat)

transition_matrix = [
    [0.45, 0.1, 0.05, 0.05, 0.03, 0.13, 0.07, 0.06, 0.06],
    [0.4, 0.01, 0.19, 0.03, 0.1, 0.08, 0.04, 0.09, 0.06],
    [0.3, 0.03, 0.04, 0.1, 0.01, 0.08, 0.06, 0.18, 0.2],
    [0.4, 0.02, 0.08, 0.07, 0.16, 0.04, 0.03, 0.12, 0.08],
    [0.5, 0.07, 0.04, 0.05, 0.02, 0.15, 0.08, 0.06, 0.03],
    [0.2, 0.08,  0.03, 0.1, 0.1, 0.3, 0.2, 0.02, 0.06],
    [0.2, 0.08, 0.03, 0.1, 0.04, 0.3, 0.2, 0.04, 0.01],
    [0.30, 0.08,  0.1, 0.06, 0.01, 0.2, 0.19, 0.02, 0.04],
    [0.3, 0.01, 0.09, 0.06, 0.01, 0.14, 0.17, 0.2, 0.02]
]

# Function to choose the next pattern using the Markov Chain
def choose_next_pattern(current_state):
    return random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8], transition_matrix[current_state])[0]

# Main function
def main():
    try:
        tempo = float(input("Enter tempo (BPM): "))
        if tempo <= 0:
            print("Please enter a valid positive tempo.")
            return
    except ValueError:
        print("Invalid input. Please enter a valid number for tempo.")
        return
    
    time_per_beat = 60 / tempo


    # Start playing the ride cymbal pattern
    current_state = 0  # Start at Pattern 1

    while True:
        if current_state == 0:
            swing_pattern(fs, time_per_beat)
        elif current_state == 1:
            phrase_one(fs, time_per_beat)
        elif current_state == 2:
            phrase_two(fs, time_per_beat)
        elif current_state == 3:
            phrase_three(fs, time_per_beat)
        elif current_state == 4:
            phrase_four(fs, time_per_beat)
        elif current_state == 5:
            phrase_five(fs, time_per_beat)
        elif current_state == 6:
            phrase_six(fs, time_per_beat)
        elif current_state == 7:
            phrase_seven(fs, time_per_beat)
        elif current_state == 8:
            phrase_eight(fs, time_per_beat)
 

        # After each pattern, choose the next pattern based on the Markov Chain
        current_state = choose_next_pattern(current_state)


if __name__ == "__main__":
    main()