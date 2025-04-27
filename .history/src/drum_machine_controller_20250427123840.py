"""
drum_machine_controller.py - The Controller component
Connects the UI (View) with the music engine (Model)
"""
from music_engine import MusicEngine

class appController:
    def __init__(self):
        self.engine = MusicEngine()
        self.view = None
        
    def set_view(self, view):
        """Set a reference to the view"""
        self.view = view
        
    def initialize_audio(self):
        """Initialize the audio system"""
        return self.engine.initialize_audio()
    
    def start_performance(self, tempo, mode):
        """Start a performance with the given tempo and mode"""
        return self.engine.start_performance(tempo, mode)
    
    def stop_performance(self):
        """Stop the current performance"""
        self.engine.stop_performance()
        
    def register_bar_change_listener(self, callback):
        """Register a callback to be notified of bar changes"""
        self.engine.register_bar_change_listener(callback)
    
    def unregister_bar_change_listener(self, callback):
        """Unregister a bar change callback"""
        self.engine.unregister_bar_change_listener(callback)
