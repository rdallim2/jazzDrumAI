import time
import random
from time import sleep
import threading
import fluidsynth
import mido
import pygame.midi
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from functools import partial

# Import everything from new_app.py
from new_app import *
from bass_blues import *

class DrumMachineGUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        self.running_threads = []
        self.stop_event = threading.Event()
        self.fs = None
        self.output_device = None
        self.input_device = None

        # Title
        self.add_widget(Label(
            text='JazzDrumAI',
            font_size='32sp',
            size_hint_y=None,
            height=60
        ))

        # Tempo Selection
        tempo_layout = GridLayout(cols=2, size_hint_y=None, height=100)
        self.tempo_label = Label(text='Tempo: 120 BPM')
        tempo_layout.add_widget(self.tempo_label)
        
        self.tempo_slider = Slider(
            min=60,
            max=350,
            value=120,
            step=1,
            size_hint_x=0.8
        )
        self.tempo_slider.bind(value=self.on_tempo_change)
        tempo_layout.add_widget(self.tempo_slider)
        self.add_widget(tempo_layout)

        # Mode Selection
        self.mode_spinner = Spinner(
            text='Select Mode',
            values=('Drums Only', 'Piano with Drums', 'Piano and Bass with Drums', 'Bass with Drums'),
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'center_x': 0.5}
        )
        self.add_widget(self.mode_spinner)

        # Control Buttons
        control_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=50,
            spacing=10,
            padding=10
        )
        
        self.start_button = Button(
            text='Start',
            size_hint_x=0.5
        )
        self.start_button.bind(on_press=self.start_performance)
        
        self.stop_button = Button(
            text='Stop',
            size_hint_x=0.5,
            disabled=True
        )
        self.stop_button.bind(on_press=self.stop_performance)
        
        control_layout.add_widget(self.start_button)
        control_layout.add_widget(self.stop_button)
        self.add_widget(control_layout)

        # Status Label
        self.status_label = Label(
            text='Ready to play',
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.status_label)

        # Initialize FluidSynth and MIDI
        self.initialize_audio()

    def initialize_audio(self):
        try:
            global fs  # Use the global fs from new_app.py
            # Initialize FluidSynth
            fs = fluidsynth.Synth()
            fs.start(driver="coreaudio")
            fs.setting('synth.gain', 1.35)

            # Initialize pygame MIDI
            if not pygame.midi.get_init():
                pygame.midi.init()
            
            # Load SoundFonts
            piano_sfid = fs.sfload("FluidR3_GM.sf2")
            if piano_sfid == -1:
                raise Exception("Failed to load piano SoundFont")
            fs.sfont_select(0, piano_sfid)
            fs.program_select(10, piano_sfid, 0, 0)  # Program 0 for piano sounds
            fs.cc(10, 7, 50)
            fs.cc(9, 7, 60)

            fs.program_select(9, piano_sfid, 0, 32)  # 0 is the channel, 32 is the bank for fingered bass

            # Load SoundFont for drum sounds
            drum_sfid = fs.sfload("drums_for_ai_v10.sf2")  # Replace with the actual drum SoundFont file path
            if drum_sfid == -1:
                raise Exception("Failed to load drum SoundFont")
            fs.sfont_select(0, drum_sfid)
            #THE PARAMS BELOW ARE WHAT MAKE THE AUDIO WORK WITH PIANO
            #First param is inst num in polyphone preset (4), if in two player, set first param to 0
            fs.program_select(0, drum_sfid, 0, 0)  # Program 128 for drum kit
        except Exception as e:
            self.status_label.text = f'Error initializing audio: {str(e)}'

    def on_tempo_change(self, instance, value):
        self.tempo_label.text = f'Tempo: {int(value)} BPM'

    def run_drums_wrapper(self, time_per_beat, tempo, players):
        try:
            trip_spacing = get_trip_spacing(tempo)
            # Initialize state variables outside the loop
            comp_choice = 'n'  # Start with swing pattern
            curr_density = '8'
            curr_vol = '0'
            
            while not self.stop_event.is_set():
                # Execute the current pattern
                if comp_choice == 'n':  
                    swing_pattern(fs, time_per_beat, trip_spacing)
                else:
                    if curr_density == '8':
                        if curr_vol == 'l':
                            eigth_phrases = [s8_s_one, s8_s_two, s8_s_three, s8_s_four, s8_s_five, s8_s_six, s8_s_seven, s8_s_eight, s8_b_one, s8_b_two, s8_b_three, s8_b_four, s8_b_five, s8_b_six, s8_b_seven, s8_b_eight]
                            random.choice(eigth_phrases)(fs, time_per_beat, trip_spacing)
                        elif curr_vol == 'm':
                            s8_med_phrases = [s8_s_one, s8_s_two, s8_crash_one, s8_crash_two, s8_b_one]
                            random.choice(s8_med_phrases)(fs, time_per_beat, trip_spacing)
                        else:
                            s8_high_phrases = [s8_crash_one, s8_crash_two]
                            random.choice(s8_high_phrases)(fs, time_per_beat, trip_spacing)
                    elif curr_density == 't8':
                        if curr_vol == 'l':
                            t_eighth_phrases = [t8_s_one, t8_s_two, t8_s_three, t8_s_four, t8_b_one, t8_b_two, t8_b_three, t8_b_four]
                            random.choice(t_eighth_phrases)(fs, time_per_beat)
                        elif curr_vol == 'm': 
                            t_med_phrases = [t8_s_one, t8_s_two, t8_crash_one, t8_crash_two]
                            random.choice(t_med_phrases)(fs, time_per_beat)
                        else:
                            t_high_phrases = [t8_crash_one, t8_crash_two]
                            random.choice(t_high_phrases)(fs, time_per_beat)

                # Check stop event after pattern execution
                if self.stop_event.is_set():
                    break

                # Choose next pattern
                current_state = choose_next_phrase(tempo, players)
                curr_density = current_state[0]
                curr_vol = current_state[1]
                comp_choice = current_state[2]
                print(f"current_density: {curr_density}, current_volume: {curr_vol}, comp_choice: {comp_choice}")
        except Exception as e:
            print(f"Error in drums thread: {e}")

    def handle_midi_input_wrapper(self, tempo):
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

    def run_bass_wrapper(self, time_per_beat, bass_channel=9):
        try:
            while not self.stop_event.is_set():
                # Simple bass pattern
                if not self.stop_event.is_set():
                    walking_bass_line(fs, time_per_beat, bass_channel)          
        except Exception as e:
            print(f"Error in bass thread: {e}")

    def start_performance(self, instance):
        global fs
        if fs is None:
            self.initialize_audio()
            if fs is None:
                self.status_label.text = 'Error: Audio not initialized'
                return

        # Reset stop event
        self.stop_event.clear()

        tempo = self.tempo_slider.value
        mode = self.mode_spinner.text
        
        # Convert mode to player number
        if mode == 'Drums Only':
            players = 1
        elif mode == 'Piano with Drums':
            players = 2
        elif mode == 'Piano and Bass with Drums':
            players = 3
        elif mode == 'Bass with Drums':
            players = 4
        else:
            self.status_label.text = 'Please select a mode'
            return

        time_per_beat = 60 / tempo

        try:
            # Start appropriate threads based on mode
            if players == 1:
                drum_thread = threading.Thread(
                    target=self.run_drums_wrapper,
                    args=(time_per_beat, tempo, players)
                )
                drum_thread.daemon = True
                drum_thread.start()
                self.running_threads.append(drum_thread)
            
            elif players == 2:
                drum_thread = threading.Thread(
                    target=self.run_drums_wrapper,
                    args=(time_per_beat, tempo, players)
                )
                midi_thread = threading.Thread(
                    target=self.handle_midi_input_wrapper,
                    args=(tempo,)
                )
                drum_thread.daemon = True
                midi_thread.daemon = True
                drum_thread.start()
                midi_thread.start()
                self.running_threads.extend([drum_thread, midi_thread])
            
            elif players == 3:
                drum_thread = threading.Thread(
                    target=self.run_drums_wrapper,
                    args=(time_per_beat, tempo, players)
                )
                midi_thread = threading.Thread(
                    target=self.handle_midi_input_wrapper,
                    args=(tempo,)
                )
                bass_thread = threading.Thread(
                    target=self.run_bass_wrapper,
                    args=(time_per_beat, 9)
                )
                drum_thread.daemon = True
                midi_thread.daemon = True
                bass_thread.daemon = True
                drum_thread.start()
                midi_thread.start()
                bass_thread.start()
                self.running_threads.extend([drum_thread, midi_thread, bass_thread])

            elif players == 4:
                drum_thread = threading.Thread(
                    target=self.run_drums_wrapper,
                    args=(time_per_beat, tempo, players)
                )
                bass_thread = threading.Thread(
                    target=self.run_bass_wrapper,
                    args=(time_per_beat, 9)
                )
                drum_thread.daemon = True
                bass_thread.daemon = True
                drum_thread.start()
                bass_thread.start()
                self.running_threads.extend([drum_thread, bass_thread])

            self.status_label.text = f'Playing - {mode}'
            self.start_button.disabled = True
            self.stop_button.disabled = False
            self.mode_spinner.disabled = True
            self.tempo_slider.disabled = True
            
        except Exception as e:
            self.status_label.text = f'Error starting performance: {str(e)}'

    def stop_performance(self, instance):
        # Signal threads to stop
        self.stop_event.set()
        print("Stop performance toggled")
        
        # Immediate audio cleanup - just stop notes
        try:
            global fs
            if fs is not None:
                # Stop all notes on all channels
                for channel in [0, 4, 10]:
                    for note in range(128):
                        fs.noteoff(channel, note)
                    fs.all_notes_off(channel)
                    fs.all_sounds_off(channel)
        except Exception as e:
            print(f"Error during immediate cleanup: {e}")
        
        # Wait for threads to finish (with shorter timeout)
        for thread in self.running_threads:
            if thread.is_alive():
                thread.join(timeout=0.1)
        
        # Clear the thread list
        self.running_threads.clear()
        
        # Reset UI
        self.status_label.text = 'Ready to play'
        self.start_button.disabled = False
        self.stop_button.disabled = True
        self.mode_spinner.disabled = False
        self.tempo_slider.disabled = False

    def __del__(self):
        try:
            global fs
            if fs is not None:
                for i in range(128):
                    fs.noteoff(0, i)
                    fs.noteoff(4, i)
                    fs.noteoff(10, i)
        except:
            pass

class DrumMachineApp(App):
    def build(self):
        Window.size = (500, 400)
        return DrumMachineGUI()

if __name__ == '__main__':
    DrumMachineApp().run() 