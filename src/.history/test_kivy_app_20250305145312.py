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

# Import your drum functions here
from drum_phrases import *
from new_app.py import * 
class DrumMachineGUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        self.running_threads = []

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
            max=400,
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
            values=('Drums Only', 'Piano with Drums', 'Piano and Bass with Drums'),
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
            # Initialize FluidSynth
            self.fs = fluidsynth.Synth()
            self.fs.start(driver="coreaudio")
            self.fs.setting('synth.gain', 0.5)

            # Initialize pygame MIDI
            pygame.midi.init()
            
            # Load SoundFonts
            piano_sfid = self.fs.sfload("FluidR3_GM.sf2")
            if piano_sfid == -1:
                self.status_label.text = 'Error: Failed to load piano SoundFont'
                return
            self.fs.sfont_select(0, piano_sfid)
            self.fs.program_select(10, piano_sfid, 0, 0)

            drum_sfid = self.fs.sfload("drums_for_ai_v10.sf2")
            if drum_sfid == -1:
                self.status_label.text = 'Error: Failed to load drum SoundFont'
                return
            self.fs.sfont_select(0, drum_sfid)
            self.fs.program_select(4, drum_sfid, 0, 0)

            self.status_label.text = 'Audio initialized successfully'
        except Exception as e:
            self.status_label.text = f'Error initializing audio: {str(e)}'

    def on_tempo_change(self, instance, value):
        self.tempo_label.text = f'Tempo: {int(value)} BPM'

    def start_performance(self, instance):
        if not hasattr(self, 'fs'):
            self.status_label.text = 'Error: Audio not initialized'
            return

        tempo = self.tempo_slider.value
        mode = self.mode_spinner.text
        
        # Convert mode to player number
        if mode == 'Drums Only':
            players = 1
        elif mode == 'Piano with Drums':
            players = 2
        elif mode == 'Piano and Bass with Drums':
            players = 3
        else:
            self.status_label.text = 'Please select a mode'
            return

        time_per_beat = 60 / tempo

        try:
            # Start appropriate threads based on mode
            if players == 1:
                drum_thread = threading.Thread(
                    target=run_drums,
                    args=(time_per_beat, tempo, players)
                )
                drum_thread.daemon = True
                drum_thread.start()
                self.running_threads.append(drum_thread)
            
            elif players == 2:
                drum_thread = threading.Thread(
                    target=run_drums,
                    args=(time_per_beat, tempo, players)
                )
                midi_thread = threading.Thread(
                    target=handle_midi_input,
                    args=(tempo,)
                )
                drum_thread.daemon = True
                midi_thread.daemon = True
                drum_thread.start()
                midi_thread.start()
                self.running_threads.extend([drum_thread, midi_thread])
            
            elif players == 3:
                drum_thread = threading.Thread(
                    target=run_drums,
                    args=(time_per_beat, tempo, players)
                )
                midi_thread = threading.Thread(
                    target=handle_midi_input,
                    args=(tempo,)
                )
                bass_thread = threading.Thread(
                    target=run_bass,
                    args=(time_per_beat, 9)
                )
                drum_thread.daemon = True
                midi_thread.daemon = True
                bass_thread.daemon = True
                drum_thread.start()
                midi_thread.start()
                bass_thread.start()
                self.running_threads.extend([drum_thread, midi_thread, bass_thread])

            self.status_label.text = f'Playing - {mode}'
            self.start_button.disabled = True
            self.stop_button.disabled = False
            self.mode_spinner.disabled = True
            
        except Exception as e:
            self.status_label.text = f'Error starting performance: {str(e)}'

    def stop_performance(self, instance):
        # Stop all running threads
        for thread in self.running_threads:
            thread.daemon = False
        self.running_threads.clear()
        
        self.status_label.text = 'Ready to play'
        self.start_button.disabled = False
        self.stop_button.disabled = True
        self.mode_spinner.disabled = False

class DrumMachineApp(App):
    def build(self):
        Window.size = (500, 400)
        return DrumMachineGUI()

if __name__ == '__main__':
    DrumMachineApp().run() 