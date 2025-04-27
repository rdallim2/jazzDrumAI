import time
import random
from time import sleep
import threading
import fluidsynth
import mido
import pygame.midi

from drum_phrases import *
# Initialize the synthesizer
fs = fluidsynth.Synth()
fs.start(driver="coreaudio")
fs.setting('synth.gain', 1.35)

pygame.midi.init()
pygame.midi.init()

# List available MIDI devices
device_count = pygame.midi.get_count()
for i in range(device_count):
    info = pygame.midi.get_device_info(i)
    name = info[1].decode("utf-8")  # Decode bytes to string for better readability
    is_input = "Input" if info[2] else "Output"  # Use info[2] to determine input/output
    print(f"Device {i}: {name} - {is_input}")

#3 if input
input_device_id = 2
input_device = pygame.midi.Input(input_device_id)

#comment these out if using one player
##output_device_id = 12

#output_device_id = 0
#output_device = pygame.midi.Output(output_device_id)

#output_device.set_instrument(10)  

try:
    # Load SoundFont for piano sounds
    piano_sfid = fs.sfload("FluidR3_GM.sf2")
    if piano_sfid == -1:
        raise Exception("Failed to load piano SoundFont")
    fs.sfont_select(0, piano_sfid)
    fs.program_select(10, piano_sfid, 0, 0)  # Program 0 for piano sounds

    # Load SoundFont for drum sounds
    drum_sfid = fs.sfload("drums_for_ai_v10.sf2")  # Replace with the actual drum SoundFont file path
    if drum_sfid == -1:
        raise Exception("Failed to load drum SoundFont")
    fs.sfont_select(0, drum_sfid)
    #THE PARAMS BELOW ARE WHAT MAKE THE AUDIO WORK WITH PIANO
    #First param is inst num in polyphone preset (4), if in two player, set first param to 0
    fs.program_select(0, drum_sfid, 0, 0)  # Program 128 for drum kit
except Exception as e:
    print(f"Error loading soundfonts: {e}")

available_ports = mido.get_input_names()
print(available_ports)
if not available_ports:
    print("No MIDI devices found. Please connect your MIDI keyboard and try again.")
    exit()


drum_transition_matrix = [
[0.7,0.0545,0.0273,0.0273,0.0164,0.0709,0.0382,0.0327,0.0327],
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
def choose_next_pattern(current_state, tempo, player_count):
    if player_count == 1:
        return random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8], drum_transition_matrix[current_state])[0]
    else:
        den_vol = analyze_density(tempo)
        print("den_vol: ", den_vol)
        if den_vol[0] == 0:
            return random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8], drum_transition_matrix[current_state])[0]
        elif den_vol[0] == 1:
            if den_vol[1] == 0:
                return random.choice([0, 1, 2, 3, 4, 5])
            elif den_vol[1] == 1: 
                return random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8], drum_transition_matrix[current_state])[0]
            else:
                return random.choice([4, 5, 6, 7, 8])
        elif den_vol[0] == 2:
            if den_vol[1] == 0:
                return random.choice([0, 1, 2, 3, 4, 5])

            elif den_vol[1] == 1:
                return random.choices([0, 1, 2, 3, 4, 5, 6, 7, 8], drum_transition_matrix[current_state])[0]
            else:
                return random.choice([5, 6, 8])  


choose_phrase_matrix = [    
    [.3, .25, .2],    
    [.35, .3, .25],
    [.4, .35, .3]
]

phrase_volume_matrix = [    
    [.05, .08, .1],
    [.1, .15, .2],
    [.4, .5, .6]
]

drum_phrase_type_matrix = [
    [.4, .2, .3, .1],
    [.2, .4, .1, .3],
    [.4, .2, .3, .1],
    [.2, .4, .1, .3] 
]

drum_comp_vs_time_matrix = [
    [.2, .3, .4],
    [.3, .4, .5],
    [.4, .6, .7]
]

def choose_next_phrase(tempo, player_count):
    if player_count == 1:
        density = ['8', 't8']
        volume = ['l', 'h']
        comp = ['y', 'n']
        d = random.choices(density)[0]
        v = random.choices(volume)[0]
        c = random.choices(comp)[0]
        return [d, v, c]
    if player_count == 2:
        den_vol = analyze_density(tempo)
        den = den_vol[0]
        vol = den_vol[1]
        #create density/volume matrix
        adjusted_tempo = tempo - 50 #tempo as proportion of available tempos 50-350
        p = choose_phrase_matrix[vol][den]
        new_p = p + (1.0 - p) * (adjusted_tempo // 300)

        print(f"equation: {p} + {1.0 - p} * {adjusted_tempo // 300}")
        #percent play 8th based ideas over trip
        print(f"volume: {vol}, density: {den}")
        print(f"p: {p}")
        
        print("new_p: ", new_p)

        #percent of time to play more crashes
        vol = phrase_volume_matrix[vol][den]
        print(f"vol: {vol}")
        density = ['8', 't8']
        density_probs = [new_p, 1.0 - new_p]
        density_choice = random.choices(density, density_probs)[0]
        volume = ['l', 'h']
        volume_probs = [vol, 1.0 - vol]
        volume_choice = random.choices(volume, volume_probs)[0]

        comp_amount_choice = drum_comp_vs_time_matrix[int(den)][int(vol)]
        comp = ['y', 'n']
        comp_prob = [comp_amount_choice, 1.0 - comp_amount_choice]
        comp_choice = random.choices(comp, comp_prob)[0]
        print(f"Comping: {comp_choice}")

        return [density_choice, volume_choice, comp_choice]
        #REMEMBER- NOW NEED TO ACCOUNT FOR HOW MUCH TIME YOU NEED TO LAY OUT



def run_drums(time_per_beat, tempo, player_count):
    comp_choice = 'n'  # Start with swing pattern
    curr_density = '8'
    curr_vol = '0'
    while True:
        if comp_choice == 'n':  
            swing_pattern(fs, time_per_beat)
        else:
            if curr_density == '8':
                if curr_vol == 'l':
                    eigth_phrases = [s8_s_one, s8_s_two, s8_s_three, s8_s_four, s8_s_five, s8_s_six, s8_s_seven, s8_s_eight, s8_b_one, s8_b_two, s8_b_three, s8_b_four, s8_b_five, s8_b_six, s8_b_seven, s8_b_eight]
                    random.choice(eigth_phrases)(fs, time_per_beat)
                elif curr_vol == 'h':
                    s8_crash_phrases = [s8_crash_one, s8_crash_two]
                    random.choice(s8_crash_phrases)(fs, time_per_beat)
            elif curr_density == 't8':
                if curr_vol == 'l':
                    t_eighth_phrases = [t8_s_one, t8_s_two, t8_s_three, t8_s_four, t8_b_one, t8_b_two, t8_b_three, t8_b_four]
                    random.choice(t_eighth_phrases)(fs, time_per_beat)
                elif curr_vol == 'h': 
                    t_crash_phrases = [t8_crash_one, t8_crash_two]
                    random.choice(t_crash_phrases)(fs, time_per_beat)

        # After each pattern, choose the next pattern based on the Markov Chain
        current_state = choose_next_phrase(tempo, player_count)
        curr_density = current_state[0]
        curr_vol = current_state[1]
        comp_choice = current_state[2]
        print(f"current_density: {curr_density}, current_volume: {curr_vol}, comp_choice: {comp_choice}")

note_events = []
note_volumes = []

def analyze_density(bpm):
    curr_time = time.time() * 1000
    beat_duration = 60000 / bpm
    two_beat_window = beat_duration * 2
    threshold = 15
    ret = []
    recent_density = sorted([timestamp for timestamp in note_events if (curr_time - timestamp) <= two_beat_window])
    recent_volumes = [volume for timestamp, volume in note_volumes if (curr_time - timestamp) <= two_beat_window]

    unique_rhythms = []
    last_event_time = None
    for timestamp in recent_density:
        if last_event_time is None or (timestamp - last_event_time > threshold):
            unique_rhythms.append(timestamp)
            last_event_time = timestamp
    density = len(unique_rhythms)

    avg_volume = sum(recent_volumes) / len(recent_volumes) if recent_volumes else 0
    print("Average volume in last two beats: ", avg_volume)

    print(f"Density in the last two beats: {density} notes")    
    ret_den = 0 
    ret_vol = 0
    if density > 6:  # Example threshold for high density (adjust as needed)
        ret_den = 2
    elif 3 < density <= 6:
        ret_den = 1
    elif density <= 3:
        ret_den = 0

    if avg_volume >= 90:
        ret_vol = 2
    elif 30 < avg_volume <= 89:
        ret_vol = 1
    else:
        ret_vol = 0

    return [ret_den, ret_vol]
    


# Function for handling MIDI input
def handle_midi_input(tempo):
    with mido.open_input(available_ports[3]) as port:
        print("Listening for Keyboard MIDI input... Press Ctrl+C to exit.")
        try:
            for msg in port:
                if msg.type == "note_on":
                    if msg.note >= 35 and msg.note <= 81:  
                        fs.noteon(10, msg.note, msg.velocity) 
                    timestamp = time.time() * 1000
                    note_events.append(timestamp)
                    note_volumes.append((time.time() * 1000, msg.velocity))
                elif msg.type == "note_off":
                    if msg.note >= 35 and msg.note <= 81:  
                        fs.noteoff(10, msg.note)
                analyze_density(tempo)
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

    output_device_id = 9 if players != 1 else 7
    print("output device id: ", output_device_id)
    output_device = pygame.midi.Output(output_device_id)
    output_device.set_instrument(0) if players != 1 else output_device.set_instrument(0)
    
    time_per_beat = 60 / tempo

    # Start the drum pattern and MIDI listener concurrently using threads
    if players == 0:
        while True:
            s8_crash_one(fs, time_per_beat)
            print("Playing swing")
    elif players == 1:
        drum_thread = threading.Thread(target=run_drums, args=(time_per_beat, tempo, players))
        drum_thread.start()
        
    else:
        port_name = available_ports[3]
        
        drum_thread = threading.Thread(target=run_drums, args=(time_per_beat, tempo, players))
        drum_thread.start()
    
        midi_thread = threading.Thread(target=handle_midi_input, args=(tempo,))
        midi_thread.start()
        
        drum_thread.join()
        midi_thread.join()
    
if __name__ == "__main__":
    main()