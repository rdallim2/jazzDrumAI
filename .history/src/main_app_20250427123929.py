"""
main_app.py - Main application entry point
Initializes and connects all components of the MVC architecture
"""
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from app_controller import appController
from app_ui import appUI

class DrumMachineApp(App):
    def build(self):
        # Initialize controller
        controller = appController()
        
        # Create UI with reference to controller
        ui = appUI(controller)
        
        # Set reference to view in controller
        controller.set_view(ui)
        
        # Apply styling
        self.apply_styles()
        Window.size = (600, 500)  # Slightly larger window
        Window.clearcolor = (0.12, 0.12, 0.14, 1)  # Very dark gray fallback color
        
        return ui
    
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
