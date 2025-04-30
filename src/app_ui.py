import kivy
kivy.require('2.2.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, BooleanProperty, NumericProperty, StringProperty
from kivy.clock import Clock
from kivy.resources import resource_add_path
import os
import sys
import time

# Add the fonts directory to resource path
resource_add_path(os.path.join(os.path.dirname(__file__), '../fonts'))

# Import the MusicEngine class
from music_engine import MusicEngine

class MyLayout(BoxLayout):
    slider = ObjectProperty(None)
    dropdown = ObjectProperty(None)

    is_playing = BooleanProperty(False)  # Track if music is playing
    tempo = NumericProperty(120)        # Default tempo
    band_mode = StringProperty("Drums/Bass")  # Default band mode
    
    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)

        # Set up the music engine
        self.music_engine = MusicEngine()
        
        # Initialize variables for button highlighting
        self.current_measure = 0
        self.measure_buttons = []
        
        # Set up dropdown options
        if hasattr(self, 'my_dropdown'):
            self.my_dropdown.values = ["Drums/Bass", "Drums/Bass/Piano"]
            
        # Find all buttons after the UI is fully loaded
        Clock.schedule_once(self.find_buttons, 0.5)
        
        # Register the music engine with bass_blues module
        from bass_blues import set_music_engine
        set_music_engine(self.music_engine)
        
        # Bind to the bar change event
        self.music_engine.bind(on_bar_change=self.on_measure_change)
        
    def find_buttons(self, dt):
        """Find all the buttons in the GridLayout to use for measure highlighting"""
        for widget in self.walk(restrict=True):
            if isinstance(widget, GridLayout):
                # Get all buttons from the GridLayout
                self.measure_buttons = [btn for btn in widget.children 
                                      if isinstance(btn, Button)]
                # Buttons are in reverse order in Kivy - fix the order
                self.measure_buttons.reverse()
                print(f"Found {len(self.measure_buttons)} measure buttons")
                return
                
        print("Could not find GridLayout with buttons")

    def on_tempo(self, instance, value):
        self.tempo = value

    def on_measure_change(self, instance, measure_num):
        if not self.is_playing or not self.measure_buttons:
            return
            
        print(f"Measure {measure_num}: Updating button highlighting")

        for btn in self.measure_buttons:
            btn.background_color = [0.16, 0.19, 0.25, 1]  #default color
        
        button_index = measure_num % len(self.measure_buttons)
        if 0 <= button_index < len(self.measure_buttons):
            self.measure_buttons[button_index].background_color = [235/255, 145/255, 65/255, 1.0] #orange
            
        self.current_measure = button_index

    def on_mode_selected(self, spinner, text):
        """Update band mode when dropdown selection changes"""
        self.band_mode = text
        
    def start_playback(self):
        """Start the music with current settings"""
        # Initialize the audio system
        success, error_msg = self.music_engine.initialize_audio()
        if not success:
            print(f"Failed to initialize audio: {error_msg}")
            return
            
        # Start the performance
        success, status = self.music_engine.start_performance(self.tempo, self.band_mode)
        if not success:
            print(f"Failed to start performance: {status}")
            return
            
        print(f"Started {self.band_mode} at tempo {self.tempo}")
    
    def stop_playback(self):
        """Stop the music and reset UI"""
        if self.music_engine:
            # Stop the music engine
            self.music_engine.stop_performance()
            
            # Reset all buttons to default color
            for btn in self.measure_buttons:
                btn.background_color = [0.16, 0.19, 0.25, 1]  # Dark blue
                
            print("Performance stopped")

class MyApp(App):
    def build(self):
        # Load kv file
        return MyLayout()

    def play_pause(self):
        # Toggle play/pause state
        layout = self.root
        
        # If already playing, stop it
        if layout.is_playing:
            print("Stopping playback")
            layout.stop_playback()
            layout.is_playing = False
        else:
            # If starting playback, reset the form to the beginning
            from bass_blues import reset_bar_count
            reset_bar_count()  # Reset to start of the musical form
            
            # Reset button highlighting
            layout.current_measure = 0
            for btn in layout.measure_buttons:
                btn.background_color = [0.16, 0.19, 0.25, 1]  # Reset to default color
            
            # Start playback
            print(f"Starting playback: Tempo={layout.tempo}, Mode={layout.band_mode}")
            layout.is_playing = True
            layout.start_playback()
    
    def on_stop(self):
        # Clean up resources when app closes
        if hasattr(self.root, 'stop_playback'):
            self.root.stop_playback()

if __name__ == '__main__':
    MyApp().run()