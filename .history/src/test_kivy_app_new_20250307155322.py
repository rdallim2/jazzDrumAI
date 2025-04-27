import time
import random
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

from sync_utils_new import clock as music_clock
from drum_phrases import *
from piano_comp import piano_chords
from bass_blues import *

from kivy.cache import Cache
Cache.remove('all')

class DrumMachineGUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        self.stop_event = threading.Event()
        self.fs = None
        self.current_pattern = swing_pattern
        self.current_chord = None
        self.current_bass_notes = [36, 43, 48]  # C2, G2, C3

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

    def on_beat(self, beat_time, beat_position):
        """Handle all instrument beats"""
        if self.stop_event.is_set():
            return
            
        # Start of bar
        if beat_position == 0:
            # Choose new patterns/chords
            self.current_pattern = random.choice([swing_pattern, s8_s_one, s8_s_two])
            self.current_chord = random.choice(list(piano_chords.values()))[0]
            
        # Drums on every beat
        if 'Drums' in self.mode_spinner.text:
            self.current_pattern(fs, 60.0 / music_clock.tempo, 0)
            
        # Bass on every beat
        if 'Bass' in self.mode_spinner.text:
            note = random.choice(self.current_bass_notes)
            fs.noteon(1, note, 80)
            time.sleep(0.1)
            fs.noteoff(1, note)
            
        # Piano comping on beats 2 and 4
        if 'Piano' in self.mode_spinner.text and 'play Piano' not in self.mode_spinner.text:
            if beat_position in [1, 3]:
                for note in self.current_chord:
                    fs.noteon(0, note, 80)
                time.sleep(0.1)
                for note in self.current_chord:
                    fs.noteoff(0, note)

    def start_performance(self, instance):
        if fs is None:
            self.initialize_audio()
            if fs is None:
                self.status_label.text = 'Error: Audio not initialized'
                return

        self.stop_event.clear()
        music_clock.set_tempo(self.tempo_slider.value)
        music_clock.subscribe(self.on_beat)
        music_clock.start()
        
        self.start_button.disabled = True
        self.stop_button.disabled = False
        self.mode_spinner.disabled = True
        self.status_label.text = f'Playing - {self.mode_spinner.text}'

    def stop_performance(self, instance):
        self.stop_event.set()
        music_clock.stop()
        music_clock.subscribers.clear()
        
        # Stop all notes
        for channel in [0, 1, 9]:
            for note in range(128):
                fs.noteoff(channel, note)
            fs.all_notes_off(channel)
            fs.all_sounds_off(channel)
        
        self.start_button.disabled = False
        self.stop_button.disabled = True
        self.mode_spinner.disabled = False
        self.status_label.text = 'Ready to play'

    def __del__(self):
        try:
            if fs is not None:
                for channel in [0, 1, 9]:
                    for note in range(128):
                        fs.noteoff(channel, note)
        except:
            pass

class DrumMachineApp(App):
    def build(self):
        Window.size = (500, 400)
        return DrumMachineGUI()

if __name__ == '__main__':
    DrumMachineApp().run() 