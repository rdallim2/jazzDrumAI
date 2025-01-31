import time
import random
from time import sleep
import threading
import fluidsynth
import mido
import pygame.midi

from drum_phrases import swing_pattern, phrase_one, phrase_two, phrase_three, phrase_four, phrase_five, phrase_six, phrase_seven, phrase_eight
# Initialize the synthesizer
fs = fluidsynth.Synth()
fs.start(driver="coreaudio")

pygame.midi.init()

# Open MIDI output (synth)
player = pygame.midi.Output(5)
player.set_instrument(10)  # 0 = Acoustic Grand Piano 🎹

try:
    # Load SoundFont for piano sounds
    piano_sfid = fs.sfload("FluidR3_GM.sf2")
    if piano_sfid == -1:
        raise Exception("Failed to load piano SoundFont")
    fs.sfont_select(10, piano_sfid)
    fs.program_select(10, piano_sfid, 0, 0)  # Program 0 for piano sounds

    # Load SoundFont for drum sounds
    drum_sfid = fs.sfload("FluidR3_GM.sf2")  # Replace with the actual drum SoundFont file path
    if drum_sfid == -1:
        raise Exception("Failed to load drum SoundFont")
    fs.sfont_select(0, drum_sfid)
    fs.program_select(0, drum_sfid, 128, 0)  # Program 128 for drum kit
except Exception as e:
    print(f"Error loading soundfonts: {e}")



available_ports = mido.get_input_names()
if not available_ports:
    print("No MIDI devices found. Please connect your MIDI keyboard and try again.")
    exit()

#port_name = available_ports[3]
#print(f"Using MIDI device: {port_name}")


drum_transition_matrix = [
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
    return random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8], drum_transition_matrix[current_state])[0]

def run_drums(time_per_beat):
    current_state = 0  # Start with swing pattern
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

# Function for handling MIDI input
def handle_midi_input():
    with mido.open_input(port_name) as port:
        print("Listening for Keyboard MIDI input... Press Ctrl+C to exit.")
        try:
            for msg in port:
                if msg.type == "note_on":
                    if msg.note >= 35 and msg.note <= 81:  # Drum note range
                        fs.noteon(10, msg.note, msg.velocity)  # Trigger drum synth on channel 10
                elif msg.type == "note_off":
                    if msg.note >= 35 and msg.note <= 81:  # Drum note range
                        fs.noteoff(10, msg.note)  # Stop drum synth
        except KeyboardInterrupt:
            print("\nExiting MIDI listener.")
            player.close()
            pygame.midi.quit()



# Main function
def main():

    tempo = None
    
    while tempo is None:
        try:
            tempo = float(input("Enter tempo (BPM): "))
            if tempo <= 0:
                print("Please enter a valid positive tempo.")
                tempo = None  # reset tempo if invalid
            players = int(input("1: hear drums, 2: play piano along with drums"))
        
        except ValueError:
            print("Invalid input. Please enter a valid number for tempo.")
    
    time_per_beat = 60 / tempo

    # Start the drum pattern and MIDI listener concurrently using threads

    if players == 1:
        drum_thread = threading.Thread(target=run_drums, args=(time_per_beat,))
        drum_thread.start()
        
    else:
        port_name = available_ports[3]
        
        drum_thread = threading.Thread(target=run_drums, args=(time_per_beat,))
        drum_thread.start()
    
        midi_thread = threading.Thread(target=handle_midi_input)
        midi_thread.start()
        
        drum_thread.join()
        midi_thread.join()
    
if __name__ == "__main__":
    main()