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
from kivy.graphics import Color, Rectangle, Ellipse, InstructionGroup
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.core.text import LabelBase

bar_ready = threading.Event()

from threading import Lock
fs_lock = Lock()

# Import everything from new_app.py
from new_app import *
from bass_blues import *
from piano_comp import *
from sync import stop_event


bar_ready = threading.Event()

class DrumMachineGUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15
        self.running_threads = []
        self.fs = None
        self.output_device = None
        self.input_device = None

        # Set dark mode background
        with self.canvas.before:
            # Dark background (almost black)
            Color(0.12, 0.12, 0.14, 1)  # Very dark gray (nearly black)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        
        # Update rectangles when window size changes
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Title with better fonts and styling
        title_box = BoxLayout(orientation='vertical', size_hint_y=None, height=100)
        
        title_label = Label(
            text='AI JAM BAND',
            font_name='Roboto',
            font_size='42sp',
            bold=True,
            color=(0.9, 0.9, 0.9, 1),  # Light gray text for dark mode
            size_hint_y=None,
            height=80
        )
        title_box.add_widget(title_label)
        
        subtitle_label = Label(
            text='Create music with AI',
            font_name='Roboto',
            font_size='16sp',
            italic=True,
            color=(0.7, 0.7, 0.7, 1),  # Medium gray for subtitle
            size_hint_y=None,
            height=20
        )
        title_box.add_widget(subtitle_label)
        
        self.add_widget(title_box)

        # Create a container for the controls with a slightly lighter background
        controls_container = BoxLayout(
            orientation='vertical',
            padding=[15, 15],
            spacing=15
        )
        
        with controls_container.canvas.before:
            Color(0.18, 0.18, 0.2, 1)  # Slightly lighter dark gray for controls area
            self.controls_bg = Rectangle(pos=controls_container.pos, size=controls_container.size)
        
        controls_container.bind(size=self._update_controls_bg, pos=self._update_controls_bg)

        # Tempo Selection with modern slider
        tempo_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=80, spacing=5)
        
        # Tempo label with icon
        tempo_header = BoxLayout(size_hint_y=None, height=30)
        tempo_icon = Label(
            text='♪',  # Music note icon
            font_name='Roboto',
            font_size='20sp',
            size_hint_x=None,
            width=30,
            color=(0.6, 0.8, 1.0, 1)  # Soft blue for icons
        )
        tempo_header.add_widget(tempo_icon)
        
        self.tempo_label = Label(
            text='Tempo: 120 BPM',
            font_name='Roboto',
            font_size='18sp',
            bold=True,
            color=(0.9, 0.9, 0.9, 1),  # Light gray text
            halign='left',
            valign='middle'
        )
        tempo_header.add_widget(self.tempo_label)
        tempo_layout.add_widget(tempo_header)
        
        # Slider with value display
        tempo_slider_layout = BoxLayout(size_hint_y=None, height=40)
        slow_label = Label(
            text='Slow',
            font_name='Roboto',
            size_hint_x=None,
            width=50,
            color=(0.7, 0.7, 0.7, 1)  # Medium gray
        )
        tempo_slider_layout.add_widget(slow_label)
        
        self.tempo_slider = Slider(
            min=60,
            max=350,
            value=120,
            step=1,
            size_hint_x=0.7
        )
        self.tempo_slider.bind(value=self.on_tempo_change)
        tempo_slider_layout.add_widget(self.tempo_slider)
        
        fast_label = Label(
            text='Fast',
            font_name='Roboto',
            size_hint_x=None,
            width=50,
            color=(0.7, 0.7, 0.7, 1)  # Medium gray
        )
        tempo_slider_layout.add_widget(fast_label)
        tempo_layout.add_widget(tempo_slider_layout)
        
        controls_container.add_widget(tempo_layout)

        # Mode Selection with styled spinner
        mode_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=80, spacing=5)
        
        # Mode label with icon
        mode_header = BoxLayout(size_hint_y=None, height=30)
        mode_icon = Label(
            text='★',  # Star icon
            font_name='Roboto',
            font_size='20sp',
            size_hint_x=None,
            width=30,
            color=(0.6, 0.8, 1.0, 1)  # Soft blue for icons
        )
        mode_header.add_widget(mode_icon)
        
        mode_title = Label(
            text='Playing Mode',
            font_name='Roboto',
            font_size='18sp',
            bold=True,
            color=(0.9, 0.9, 0.9, 1),  # Light gray text
            halign='left',
            valign='middle'
        )
        mode_header.add_widget(mode_title)
        mode_layout.add_widget(mode_header)
        
        # Styled spinner
        self.mode_spinner = Spinner(
            text='Select Mode',
            font_name='Roboto',
            values=('Drums Only', 'Piano with Drums', 'You play Piano, with Bass with Drums', 'Bass with Drums', 'Piano/Bass/Drums', 'You + All AI'),
            size_hint_y=None,
            height=40,
            background_color=(0.25, 0.25, 0.3, 1),  # Dark blue-gray background
            background_normal='',
            color=(0.9, 0.9, 0.9, 1),  # Light gray text
            option_cls=Factory.get('SpinnerOption'),
            sync_height=True
        )
        mode_layout.add_widget(self.mode_spinner)
        
        controls_container.add_widget(mode_layout)

        # Control Buttons with improved styling
        control_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=60,
            spacing=20,
            padding=[10, 10]
        )
        
        self.start_button = Button(
            text='START',
            font_name='Roboto',
            font_size='18sp',
            bold=True,
            background_color=(0.2, 0.5, 0.3, 1),  # Dark green
            background_normal='',
            color=(0.9, 0.9, 0.9, 1),  # Light gray text
            size_hint_x=0.5
        )
        self.start_button.bind(on_press=self.start_performance)
        
        self.stop_button = Button(
            text='STOP',
            font_name='Roboto',
            font_size='18sp',
            bold=True,
            background_color=(0.5, 0.2, 0.2, 1),  # Dark red
            background_normal='',
            color=(0.9, 0.9, 0.9, 1),  # Light gray text
            size_hint_x=0.5,
            disabled=True
        )
        self.stop_button.bind(on_press=self.stop_performance)
        
        control_layout.add_widget(self.start_button)
        control_layout.add_widget(self.stop_button)
        controls_container.add_widget(control_layout)

        # Status Label with improved styling
        status_layout = BoxLayout(size_hint_y=None, height=50, padding=[5, 5])
        
        with status_layout.canvas.before:
            Color(0.15, 0.15, 0.17, 1)  # Very dark gray for status background
            self.status_bg = Rectangle(pos=status_layout.pos, size=status_layout.size)
        
        status_layout.bind(size=self._update_status_bg, pos=self._update_status_bg)
        
        status_icon = Label(
            text='🎵',  # Music note emoji
            font_name='Roboto',
            font_size='20sp',
            size_hint_x=None,
            width=30
        )
        status_layout.add_widget(status_icon)
        
        self.status_label = Label(
            text='Ready to play',
            font_name='Roboto',
            font_size='16sp',
            color=(0.8, 0.8, 0.8, 1),  # Light gray text
            bold=True
        )
        status_layout.add_widget(self.status_label)
        
        controls_container.add_widget(status_layout)
        
        # Add the controls container to the main layout
        self.add_widget(controls_container)
        
        # Initialize FluidSynth and MIDI
        self.initialize_audio()

    def _update_rect(self, instance, value):
        """Update the canvas rectangles with window size"""
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def _update_controls_bg(self, instance, value):
        """Update the controls background rectangle"""
        self.controls_bg.pos = instance.pos
        self.controls_bg.size = instance.size

    def _update_status_bg(self, instance, value):
        """Update the status background rectangle"""
        self.status_bg.pos = instance.pos
        self.status_bg.size = instance.size

    def initialize_audio(self):
        try:
            global fs  # Use the global fs from new_app.py
            
            # Ensure any old instance is properly cleaned up
            if fs is not None:
                try:
                    fs.delete()
                except Exception as e:
                    print(f"Error cleaning up old FluidSynth instance: {e}")
                fs = None
                
            # Initialize FluidSynth with error handling
            fs = fluidsynth.Synth()
            fs.start(driver="coreaudio")
            fs.setting('synth.gain', 1.35)

            # Initialize pygame MIDI
            try:
                if pygame.midi.get_init():
                    pygame.midi.quit()
                pygame.midi.init()
            except Exception as e:
                print(f"Error reinitializing pygame MIDI: {e}")
                # Continue anyway as FluidSynth is more important
            
            # Load SoundFonts with better error handling
            try:
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
            except Exception as e:
                print(f"Error setting up piano/bass: {e}")
                # Continue to try loading drums

            try:
                # Load SoundFont for drum sounds and set up on channel 0
                drum_sfid = fs.sfload("drums_for_ai_v9.sf2")
                if drum_sfid == -1:
                    raise Exception("Failed to load drum SoundFont")
                
                fs.sfont_select(0, drum_sfid)  # Select drum soundfont for channel 0
                fs.program_select(0, drum_sfid, 0, 0)  # Set up drums on channel 0, bank 0, preset 0
                fs.cc(0, 7, 100)  # Set drum volume
            except Exception as e:
                print(f"Error setting up drums: {e}")
                
            print("Audio initialization complete - Drums on ch 0, Bass on ch 9, Piano on ch 10")
        except Exception as e:
            print(f"Critical error in initialize_audio: {e}")
            self.status_label.text = f'Error initializing audio: {str(e)}'
            # Make sure fs is None if initialization failed
            fs = None

    def on_tempo_change(self, instance, value):
        self.tempo_label.text = f'Tempo: {int(value)} BPM'

    def run_drums_wrapper(self, time_per_beat, tempo, players):
        try:
            trip_spacing = get_trip_spacing(tempo)
            comp_choice = 'n'  # Start with swing pattern
            curr_density = '8'
            curr_vol = '0'
            while not stop_event.is_set():
                try:
                    print("clearing")
                    swing_pattern(fs, time_per_beat, trip_spacing)
                    
                    #instrument_sync.set()
                    # Execute the current pattern
                    #instrument_sync.clear()
                    if comp_choice == 'n':  
                        print("clearing")
                        swing_pattern(fs, time_per_beat, trip_spacing)
                    else:
                        if curr_density == '8':
                            if curr_vol == 'l':
                                eigth_phrases = [s8_s_one, s8_s_two, s8_s_three, s8_s_four, s8_s_five, s8_s_six, s8_s_seven, s8_s_eight, s8_b_one, s8_b_two, s8_b_three, s8_b_four, s8_b_five, s8_b_six, s8_b_seven, s8_b_eight]
                                print("clearing")
                                random.choice(eigth_phrases)(fs, time_per_beat, trip_spacing)
                            elif curr_vol == 'm':
                                s8_med_phrases = [s8_s_one, s8_s_two, s8_crash_one, s8_crash_two, s8_b_one]
                                print("clearing")
                                random.choice(s8_med_phrases)(fs, time_per_beat, trip_spacing)
                            else:
                                s8_high_phrases = [s8_crash_one, s8_crash_two]
                                print("clearing")
                                random.choice(s8_high_phrases)(fs, time_per_beat, trip_spacing)
                        elif curr_density == 't8':
                            if curr_vol == 'l':
                                t_eighth_phrases = [t8_s_one, t8_s_two, t8_s_three, t8_s_four, t8_b_one, t8_b_two, t8_b_three, t8_b_four]
                                print("clearing")
                                random.choice(t_eighth_phrases)(fs, time_per_beat)
                            elif curr_vol == 'm': 
                                t_med_phrases = [t8_s_one, t8_s_two, t8_crash_one, t8_crash_two]
                                print("clearing")
                                random.choice(t_med_phrases)(fs, time_per_beat)
                            else:
                                t_high_phrases = [t8_crash_one, t8_crash_two]
                                print("clearing")
                                random.choice(t_high_phrases)(fs, time_per_beat)

                    # Signal that a phrase has completed

                    # Calculate remaining time in bar

                    # Choose next pattern
                    current_state = choose_next_phrase(tempo, players)
                    curr_density = current_state[0]
                    curr_vol = current_state[1]
                    comp_choice = current_state[2]
                    #instrument_sync.clear()
                
                    # Check stop event more frequently
                    if stop_event.is_set():
                        break
                    
                except Exception as e:
                    print(f"Error in drum pattern execution: {e}")
                    # Don't break the entire loop for a single pattern error
                    time.sleep(time_per_beat)
                    if stop_event.is_set():
                        break
                
        except Exception as e:
            print(f"Critical error in drums thread: {e}")
        finally:
            print("Drums thread exiting cleanly")
            # Ensure any active drum notes are off
            if fs is not None:
                try:
                    fs.all_notes_off(0)
                    fs.all_sounds_off(0)
                except Exception as e:
                    print(f"Error cleaning up drum notes: {e}")

    def handle_midi_input_wrapper(self, tempo):
        try:
            print("Starting MIDI input handler using functionality from new_app.py")
            
            # Set up the stop condition for the handle_midi_input function
            # by continuously checking our stop_event
            
            while not stop_event.is_set():
                try:
                    # Call the handle_midi_input function from new_app.py
                    # This passes control to the original implementation
                    handle_midi_input(tempo)
                    
                    # Short sleep to check stop_event frequently
                    time.sleep(0.1)
                except Exception as e:
                    print(f"Error in MIDI handling: {e}")
                    time.sleep(0.5)
                    if stop_event.is_set():
                        break
            
        except Exception as e:
            print(f"Critical error in MIDI input thread: {e}")
        finally:
            print("MIDI input thread exiting cleanly")
            # Ensure any active piano notes are off
            if fs is not None:
                try:
                    fs.all_notes_off(10)
                    fs.all_sounds_off(10)
                except Exception as e:
                    print(f"Error cleaning up piano notes: {e}")

    def run_bass_wrapper(self, time_per_beat, bass_channel=9):
        try:
            while not stop_event.is_set():
                try:
                    # Play bass pattern
                    play_bar(fs, time_per_beat, channel=9)  # Get the current pattern
                    
                    # Check stop event after each pattern
                    if stop_event.is_set():
                        break
                except Exception as e:
                    print(f"Error in bass pattern execution: {e}")
                    time.sleep(time_per_beat)
                    if stop_event.is_set():
                        break
        except Exception as e:
            print(f"Critical error in bass thread: {e}")
        finally:
            print("Bass thread exiting cleanly")
            # Ensure any active bass notes are off
            if fs is not None:
                try:
                    fs.all_notes_off(bass_channel)
                    fs.all_sounds_off(bass_channel)
                except Exception as e:
                    print(f"Error cleaning up bass notes: {e}")

    def run_piano_wrapper(self, time_per_beat, tempo, piano_channel=10):
        try:
            while not stop_event.is_set():
                try:
                    # Play piano pattern
                    bar_start = time.time()
                    
                    # Get current chord and play piano comp with sync points
                    piano_comp(fs, time_per_beat, tempo, piano_channel)
                    
                    # Calculate remaining time in bar
                    elapsed = time.time() - bar_start
                    remaining = (time_per_beat * 4) - elapsed
                    if remaining > 0:
                        # Use smaller sleep intervals to check stop_event more frequently
                        sleep_interval = 0.1
                        for _ in range(int(remaining / sleep_interval)):
                            if stop_event.is_set():
                                break
                            time.sleep(sleep_interval)
                        if stop_event.is_set():
                            break
                        # Sleep the remainder
                        remainder = remaining % sleep_interval
                        if remainder > 0:
                            time.sleep(remainder)
                except Exception as e:
                    print(f"Error in piano pattern execution: {e}")
                    time.sleep(time_per_beat)
                    if stop_event.is_set():
                        break
        except Exception as e:
            print(f"Critical error in piano thread: {e}")
        finally:
            print("Piano thread exiting cleanly")
            # Ensure any active piano notes are off
            if fs is not None:
                try:
                    fs.all_notes_off(piano_channel)
                    fs.all_sounds_off(piano_channel)
                except Exception as e:
                    print(f"Error cleaning up piano notes: {e}")

    def start_performance(self, instance):
        global fs
        global stop_event  # Make sure we're using the global stop_event
        
        # Always reinitialize FluidSynth - make this more robust
        if fs is not None:
            try:
                # First ensure all notes are off
                for channel in [0, 9, 10]:
                    try:
                        fs.all_notes_off(channel)
                        fs.all_sounds_off(channel)
                    except:
                        pass
                
                # Sleep briefly to allow audio to clear
                time.sleep(0.2)
                
                # Now delete the FluidSynth instance
                try:
                    fs.delete()
                except Exception as e:
                    print(f"Error deleting FluidSynth: {e}")
                    pass
            finally:
                fs = None
        
        # Add a small delay before reinitialization
        time.sleep(0.2)
        
        self.initialize_audio()
        if fs is None:
            self.status_label.text = 'Error: Audio not initialized'
            return

        # Reset stop event
        stop_event.clear()

        tempo = self.tempo_slider.value
        mode = self.mode_spinner.text
        
        # Convert mode to player number
        if mode == 'Drums Only':
            players = 1
        elif mode == 'Piano with Drums':
            players = 2
        elif mode == 'You play Piano, with Bass with Drums':
            players = 3
        elif mode == 'Bass with Drums':
            players = 4
        elif mode == 'Piano/Bass/Drums':
            players = 5
        elif mode == 'You + All AI':
            players = 6  # New mode where user plays keyboard with all AI instruments
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
                piano_thread = threading.Thread(
                    target=self.run_piano_wrapper,
                    args=(time_per_beat, tempo, 10)
                )
                drum_thread.daemon = True
                piano_thread.daemon = True
                drum_thread.start()
                piano_thread.start()
                self.running_threads.extend([drum_thread, piano_thread])
            
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
                bass_thread.start()
                drum_thread.start()
                self.running_threads.extend([drum_thread, bass_thread])

            elif players == 5:
                drum_thread = threading.Thread(
                    target=self.run_drums_wrapper,
                    args=(time_per_beat, tempo, players)
                )
                piano_thread = threading.Thread(
                    target=self.run_piano_wrapper,
                    args=(time_per_beat, tempo, 10)
                )
                bass_thread = threading.Thread(
                    target=self.run_bass_wrapper,
                    args=(time_per_beat, 9)
                )
                drum_thread.daemon = True
                piano_thread.daemon = True
                bass_thread.daemon = True
                drum_thread.start()
                piano_thread.start()
                bass_thread.start()
                self.running_threads.extend([drum_thread, piano_thread, bass_thread])
                
            elif players == 6:  # New mode: You play keyboard + all AI instruments
                # Start all AI instruments
                drum_thread = threading.Thread(
                    target=self.run_drums_wrapper,
                    args=(time_per_beat, tempo, players)
                )
                piano_thread = threading.Thread(
                    target=self.run_piano_wrapper,
                    args=(time_per_beat, tempo, 10)
                )
                bass_thread = threading.Thread(
                    target=self.run_bass_wrapper,
                    args=(time_per_beat, 9)
                )
                # Also start MIDI input thread for your keyboard
                midi_thread = threading.Thread(
                    target=self.handle_midi_input_wrapper,
                    args=(tempo,)
                )
                drum_thread.daemon = True
                piano_thread.daemon = True
                bass_thread.daemon = True
                midi_thread.daemon = True
                drum_thread.start()
                piano_thread.start()
                bass_thread.start()
                midi_thread.start()
                # Make sure to track all threads for proper cleanup
                self.running_threads.extend([drum_thread, piano_thread, bass_thread, midi_thread])

            self.status_label.text = f'Playing - {mode}'
            self.start_button.disabled = True
            self.stop_button.disabled = False
            self.mode_spinner.disabled = True
            self.tempo_slider.disabled = True
            
        except Exception as e:
            self.status_label.text = f'Error starting performance: {str(e)}'

    def stop_performance(self, instance):
        print("Stopping performance...")
        stop_event.set() 
        for thread in self.running_threads:
            max_wait_time = 10.0
            try:
                if thread.is_alive():
                    thread.join(timeout=max_wait_time)
            except Exception as e:
                print(f"Error joining thread: {e}")
        
        try:
            global fs
            if fs is not None:
                # Ensure we properly clean up FluidSynth when the app closes
                for channel in [0, 9, 10]:
                    try:
                        fs.all_notes_off(channel)
                        fs.all_sounds_off(channel)
                    except:
                        pass
                
                # Sleep briefly to allow audio to clear
                try:
                    time.sleep(0.1)
                except:
                    pass
                self.running_threads.clear()
                print(f"running threasds: {self.running_threads}")
                
        except Exception as e:
            print(f"Error during cleanup in __del__: {e}")

class DrumMachineApp(App):
    def build(self):
        # Add custom styling to Kivy widgets
        self.apply_styles()
        Window.size = (600, 500)  # Slightly larger window
        Window.clearcolor = (0.12, 0.12, 0.14, 1)  # Very dark gray fallback color
        return DrumMachineGUI()
    
    def apply_styles(self):
        # Set custom global styles for widgets
        
        # Custom styling for SpinnerOption
        Builder.load_string('''
<SpinnerOption>:
    background_color: 0.22, 0.22, 0.25, 1
    background_normal: ''
    color: 0.9, 0.9, 0.9, 1
    font_size: '16sp'
    font_name: 'Roboto'
    height: 40
''')

if __name__ == '__main__':
    DrumMachineApp().run() 