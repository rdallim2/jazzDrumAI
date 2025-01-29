import time
from time import sleep
import fluidsynth

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

# MIDI note for Ride Cymbal (General MIDI standard)
RIDE_CYMBAL = 51
BASS_DRUM = 35
SNARE_DRUM = 38
HI_HAT_CLOSED = 42


# Function to play the ride cymbal at regular intervals
def play_ride_cymbal(tempo):
    time_per_beat = 60 / tempo  # Time per quarter note in seconds

    swing_beat = [
        (BASS_DRUM, 112),   # Bass Drum on 1st beat
        (HI_HAT_CLOSED, 80),  # Hi-Hat on 1st beat
        (SNARE_DRUM, 100),  # Snare Drum on 2nd beat
        (RIDE_CYMBAL, 100) 
    ]

    while True:
        # Send a MIDI "note on" message to trigger the ride cymbal sound
        print("Note on")
        fs.noteon(0, RIDE_CYMBAL_NOTE, 112)  # 0x90 is note-on, 112 is velocity

        # Wait for the time per quarter note
        sleep(time_per_beat)

        # Send a MIDI "note off" message to stop the sound
        fs.noteoff(0, RIDE_CYMBAL_NOTE)  # 0x80 is note-off, velocity 0

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

    print(f"Playing ride cymbal at {tempo} BPM. Type 'exit' to stop.")

    # Start playing the ride cymbal pattern
    try:
        play_ride_cymbal(tempo)
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()