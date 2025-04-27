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

from sync_utils import MusicClock
from new_app import *
from bass_blues import *
from kivy_funcs import *
from piano_comp import *

from kivy.cache import Cache
Cache.remove('all')

# Create global clock instance
music_clock = MusicClock()

bar_ready = threading.Event()

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
        self.bar_sync = None
        self.beat_count = 0

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
            values=('Drums Only', 'Piano with Drums', 'You play Piano, with Bass with Drums', 'Bass with Drums', 'Piano/Bass/Drums'),
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
            
            # Set up piano on channel 10
            fs.sfont_select(10, piano_sfid)
            fs.program_select(10, piano_sfid, 0, 0)  # Piano on channel 10
            fs.cc(10, 7, 45)  # Set piano volume
            
            # Set up bass on channel 9
            fs.sfont_select(9, piano_sfid)
            fs.program_select(9, piano_sfid, 0, 32)  # Bass on channel 9
            fs.cc(9, 7, 60)  # Set bass volume

            # Load SoundFont for drum sounds and set up on channel 0
            drum_sfid = fs.sfload("drums_for_ai_v10.sf2")
            if drum_sfid == -1:
                raise Exception("Failed to load drum SoundFont")
            
            fs.sfont_select(0, drum_sfid)  # Select drum soundfont for channel 0
            fs.program_select(0, drum_sfid, 0, 0)  # Set up drums on channel 0, bank 0, preset 0
            fs.cc(0, 7, 100)  # Set drum volume
            
            print("Audio initialization complete - Drums on ch 0, Bass on ch 9, Piano on ch 10")
        except Exception as e:
            self.status_label.text = f'Error initializing audio: {str(e)}'

    def on_tempo_change(self, instance, value):
        self.tempo_label.text = f'Tempo: {int(value)} BPM'
        if music_clock.running:
            music_clock.set_tempo(value)

    def on_drum_beat(self, beat_time):
        """Handle drum beats"""
        if self.stop_event.is_set():
            return
            
        # Every 4 beats is a new bar
        bar_position = self.beat_count % 4
        if bar_position == 0:
            # Choose next pattern at start of bar
            self.current_pattern = random.choice([swing_pattern, s8_s_one, s8_s_two])
            
        # Play the current pattern
        self.current_pattern(fs, 60.0 / music_clock.tempo, 0)
        self.beat_count += 1

    def on_bass_beat(self, beat_time):
        """Handle bass beats"""
        if self.stop_event.is_set():
            return
            
        # Play bass note on each beat
        note = random.choice([36, 43, 48])  # C2, G2, C3
        fs.noteon(9, note, 80)
        time.sleep(0.1)  # Short duration
        fs.noteoff(9, note)

    def on_piano_beat(self, beat_time):
        """Handle piano beats"""
        if self.stop_event.is_set():
            return
            
        # Every 4 beats is a new bar
        bar_position = self.beat_count % 4
        if bar_position == 0:
            # Choose new chord at start of bar
            self.current_chord = random.choice(list(piano_chords.values()))[0]
            
        # Play chord on beats 2 and 4 (jazz comping)
        if bar_position in [1, 3]:
            for note in self.current_chord:
                fs.noteon(10, note, 80)
            time.sleep(0.1)
            for note in self.current_chord:
                fs.noteoff(10, note)

    def run_drums_wrapper(self, time_per_beat, tempo, players):
        try:
            sync = BarSync(time_per_beat)
            trip_spacing = get_trip_spacing(tempo)
            comp_choice = 'n'  # Start with swing pattern
            curr_density = '8'
            curr_vol = '0'
            
            while not self.stop_event.is_set():
                sync.start_bar()  # Signal start of new bar
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

                elapsed, expected = sync.get_bar_timing()
                print(f"Drums bar timing: elapsed={elapsed:.3f}s, expected={expected:.3f}s")

                # Choose next pattern
                current_state = choose_next_phrase(tempo, players)
                curr_density = current_state[0]
                curr_vol = current_state[1]
                comp_choice = current_state[2]
                
        except Exception as e:
            print(f"Error in drums thread: {e}")

    def handle_midi_input_wrapper(self, tempo):
        with mido.open_input(available_ports[3]) as port:
            print("Listening for Keyboard MIDI input... Press Ctrl+C to exit.")
            try:
                for msg in port:
                    if msg.type == "note_on":
                        if msg.note >= 35 and msg.note <= 81:  
                            fs.noteon(10, msg.note, msg.velocity)  # Changed to channel 10 for piano
                        timestamp = time.time() * 1000
                        note_events.append(timestamp)
                        note_volumes.append((time.time() * 1000, msg.velocity))
                    elif msg.type == "note_off":
                        if msg.note >= 35 and msg.note <= 81:  
                            fs.noteoff(10, msg.note)  # Changed to channel 10 for piano
                    analyze_density(tempo)
            except KeyboardInterrupt:
                print("\nExiting MIDI listener.")
                pygame.midi.quit()

    def run_bass_wrapper(self, time_per_beat, bass_channel=9):
        try:
            while not self.stop_event.is_set():
                # Simple bass pattern
                if not self.stop_event.is_set():
                    walking_bass_line(fs, time_per_beat, bass_channel)          
        except Exception as e:
            print(f"Error in bass thread: {e}")

    def run_piano_wrapper(self, time_per_beat, tempo, piano_channel=10):
        try:
            while not self.stop_event.is_set():
                # Simple piano pattern
                if not self.stop_event.is_set():
                    piano_comp(fs, time_per_beat, tempo, piano_channel)  # Fixed parameter order          
        except Exception as e:
            print(f"Error in piano thread: {e}")

    def start_performance(self, instance):
        if fs is None:
            self.initialize_audio()
            if fs is None:
                self.status_label.text = 'Error: Audio not initialized'
                return

        self.stop_event.clear()
        tempo = self.tempo_slider.value
        mode = self.mode_spinner.text
        
        # Set up clock and callbacks
        music_clock.set_tempo(tempo)
        
        if 'Drums' in mode:
            music_clock.subscribe(self.on_drum_beat)
        if 'Bass' in mode:
            music_clock.subscribe(self.on_bass_beat)
        if 'Piano' in mode and 'play Piano' not in mode:
            music_clock.subscribe(self.on_piano_beat)
            
        # Start the clock
        music_clock.start()
        
        # Update UI
        self.start_button.disabled = True
        self.stop_button.disabled = False
        self.status_label.text = 'Playing...'

    def stop_performance(self, instance):
        self.stop_event.set()
        music_clock.stop()
        
        # Clear subscribers
        music_clock.subscribers.clear()
        
        # Reset beat counter
        self.beat_count = 0
        
        # Update UI
        self.start_button.disabled = False
        self.stop_button.disabled = True
        self.status_label.text = 'Stopped'

    def __del__(self):
        try:
            global fs
            if fs is not None:
                for i in range(128):
                    fs.noteoff(0, i)
                    fs.noteoff(9, i)
                    fs.noteoff(10, i)
        except:
            pass

class DrumMachineApp(App):
    def build(self):
        Window.size = (500, 400)
        return DrumMachineGUI()

if __name__ == '__main__':
    DrumMachineApp().run() 