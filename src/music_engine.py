"""
music_engine.py - The Model component
Contains the core music generation logic separated from the UI
"""
import time
import random
import threading
import fluidsynth
import pygame.midi
import mido
from kivy.event import EventDispatcher
from new_app import *
from bass_blues import *
from piano_comp import *
from sync import stop_event, instrument_sync

class MusicEngine(EventDispatcher):
    def __init__(self):
        super(MusicEngine, self).__init__()
        # Register the bar change event
        self.register_event_type('on_bar_change')
        
        self.fs = None
        self.running_threads = []
        self.output_device = None
        self.input_device = None
        
    def initialize_audio(self):
        try:
            global fs
            if fs is not None:
                try:
                    fs.delete()
                except Exception as e:
                    print(f"Error cleaning up old FluidSynth instance: {e}")
                fs = None
                
            fs = fluidsynth.Synth()
            fs.start(driver="coreaudio")
            #gain at 1.99 for proper balancing with drums
            fs.setting('synth.gain', 1.99)

            try:
                if pygame.midi.get_init():
                    pygame.midi.quit()
                pygame.midi.init()
            except Exception as e:
                print(f"Error reinitializing pygame MIDI: {e}")
                # Continue anyway as FluidSynth is more important
            
            try:
                piano_sfid = fs.sfload("FluidR3_GM.sf2")
                if piano_sfid == -1:
                    raise Exception("Failed to load piano SoundFont")
                
                # Set up piano on channel 10
                fs.sfont_select(10, piano_sfid)
                fs.program_select(10, piano_sfid, 0, 0)  # Piano on channel 10
                fs.cc(10, 7, 40)  # Set piano volume
                
                # Set up bass on channel 9
                fs.sfont_select(9, piano_sfid)
                fs.program_select(9, piano_sfid, 0, 32)  # Bass on channel 9
                fs.cc(9, 7, 60)  # Set bass volume
            except Exception as e:
                print(f"Error setting up piano/bass: {e}")
                # Continue to try loading drums

            try:
                # Load SoundFont for drum sounds and set up on channel 0
                drum_sfid = fs.sfload("drums_for_ai_v10.sf2")
                if drum_sfid == -1:
                    raise Exception("Failed to load drum SoundFont")
                
                fs.sfont_select(0, drum_sfid)  # Select drum soundfont for channel 0
                fs.program_select(0, drum_sfid, 0, 0)  # Set up drums on channel 0, bank 0, preset 0
                fs.cc(0, 7, 120)  # Set drum volume
            except Exception as e:
                print(f"Error setting up drums: {e}")
                
            print("Audio initialization complete - Drums on ch 0, Bass on ch 9, Piano on ch 10")
            return True, None
        except Exception as e:
            print(f"Critical error in initialize_audio: {e}")
            # Make sure fs is None if initialization failed
            fs = None
            return False, str(e)
            
    def run_drums(self, time_per_beat, tempo, players):
        try:
            trip_spacing = get_trip_spacing(tempo)
            comp_choice = 'n'  # Start with swing pattern
            curr_density = '8'
            curr_vol = '0'
            while not stop_event.is_set():
                try:
                    if comp_choice == 'n':  
                        swing_pattern(fs, time_per_beat, trip_spacing)
                    else:
                        if curr_density == '8':
                            if curr_vol == 'l':
                                eigth_phrases = [s8_s_one, s8_s_two, s8_b_one]
                                random.choice(eigth_phrases)(fs, time_per_beat, trip_spacing)
                            elif curr_vol == 'm':
                                s8_med_phrases = [s8_s_one, s8_s_two, s8_b_one, s8_s_two, s8_s_three, s8_s_four, s8_s_five, s8_s_six, s8_s_seven, s8_s_eight, s8_b_one, s8_b_two, s8_b_three, s8_b_four, s8_b_five, s8_b_six, s8_b_seven, s8_b_eight]
                                random.choice(s8_med_phrases)(fs, time_per_beat, trip_spacing)
                            else:
                                s8_high_phrases = [s8_crash_one, s8_crash_two, s8_s_eight, s8_s_two, s8_b_four, s8_s_two]
                                random.choice(s8_high_phrases)(fs, time_per_beat, trip_spacing)
                        elif curr_density == 't8':
                            if curr_vol == 'l':
                                t_eighth_phrases = [t8_s_one, t8_s_two, t8_s_three, t8_s_four, t8_b_one, t8_b_two, t8_b_three, t8_b_four]
                                random.choice(t_eighth_phrases)(fs, time_per_beat)
                            elif curr_vol == 'm': 
                                t_med_phrases = [t8_s_one, t8_s_two, t8_s_three, t8_s_four, t8_b_one, t8_b_two, t8_b_three, t8_b_four, t8_crash_one, t8_crash_two]
                                random.choice(t_med_phrases)(fs, time_per_beat)
                            else:
                                t_high_phrases = [t8_crash_one, t8_crash_two, t8_crash_three, t8_b_one, t8_s_two, t8_s_three]
                                random.choice(t_high_phrases)(fs, time_per_beat)

                    # Choose next pattern
                    current_state = choose_next_phrase(tempo, players)
                    curr_density = current_state[0]
                    curr_vol = current_state[1]
                    comp_choice = current_state[2]
                
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
                    
    def handle_midi_input(self, tempo):
        """Safely handle MIDI input with proper error checking and stop_event handling"""
        with mido.open_input(available_ports[3]) as port:
            print("Listening for Keyboard MIDI input... Press Ctrl+C to exit.")
            try:
                for msg in port:
                    if msg.type == "note_on":
                        if msg.note >= 35 and msg.note <= 88:  
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
                
    def run_bass(self, time_per_beat, bass_channel=9):
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
                    
    def run_piano(self, time_per_beat, tempo, piano_channel=10):
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
                    
    def start_performance(self, tempo, mode):
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
        
        success, error = self.initialize_audio()
        if not success:
            return False, f'Error: {error}'

        # Reset stop event
        stop_event.clear()
        
        # Convert mode to player number
        if mode == 'Drums/Bass':
            players = 1
        elif mode == 'Drums/Bass/Piano':
            players = 2
        else:
            return False, 'Please select a mode'

        time_per_beat = 60 / tempo
        self.running_threads = []

        try:
            if players == 1:
                drum_thread = threading.Thread(
                    target=self.run_drums,
                    args=(time_per_beat, tempo, players)
                )
                midi_thread = threading.Thread(
                    target=self.handle_midi_input,
                    args=(tempo,)
                )
                bass_thread = threading.Thread(
                    target=self.run_bass,
                    args=(time_per_beat, 9)
                )
                drum_thread.daemon = True
                midi_thread.daemon = True
                bass_thread.daemon = True
                drum_thread.start()
                midi_thread.start()
                bass_thread.start()
                self.running_threads.extend([drum_thread, midi_thread, bass_thread])

            elif players == 2:  # New mode: You play keyboard + all AI instruments
                # Start all AI instruments
                drum_thread = threading.Thread(
                    target=self.run_drums,
                    args=(time_per_beat, tempo, players)
                )
                piano_thread = threading.Thread(
                    target=self.run_piano,
                    args=(time_per_beat, tempo, 10)
                )
                bass_thread = threading.Thread(
                    target=self.run_bass,
                    args=(time_per_beat, 9)
                )
                # Also start MIDI input thread for your keyboard
                midi_thread = threading.Thread(
                    target=self.handle_midi_input,
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

            return True, mode  # Success
            
        except Exception as e:
            return False, str(e)  # Error occurred
            
    def stop_performance(self):
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
                print(f"running threads: {self.running_threads}")
                
        except Exception as e:
            print(f"Error during cleanup in __del__: {e}")
            
    def on_bar_change(self, bar_num):
        # Default handler (does nothing, will be overridden by bindings)
        pass
