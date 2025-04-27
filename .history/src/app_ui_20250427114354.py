"""
drum_machine_ui.py - The View component
Contains the UI elements and view logic separated from the business logic
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from functools import partial
from kivy.graphics import Color, Rectangle
from kivy.factory import Factory

class DrumMachineUI(BoxLayout):
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller  # Reference to the controller
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15
        self.current_bar = 0  # Track current bar for chord display
        self.measure_buttons = []
        
        # Register for bar updates from the model
        self.controller.register_bar_change_listener(self.on_bar_changed)
        
        # Set dark mode background
        with self.canvas.before:
            # Dark background (almost black)
            Color(0.12, 0.12, 0.14, 1)  # Very dark gray (nearly black)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        
        # Update rectangles when window size changes
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Build the UI components
        self._build_title_area()
        
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

        # Add various UI components to the controls container
        self._build_lead_sheet(controls_container)
        self._build_tempo_control(controls_container)
        self._build_mode_selection(controls_container)
        self._build_control_buttons(controls_container)
        self._build_status_area(controls_container)
        
        # Add the controls container to the main layout
        self.add_widget(controls_container)

    def _build_title_area(self):
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

    def _build_lead_sheet(self, parent_container):
        # Add 12-bar blues lead sheet display
        lead_sheet_title = Label(
            text='12-Bar Blues in C - Lead Sheet',
            font_name='Roboto',
            font_size='20sp',
            bold=True,
            color=(0.4, 0.8, 1.0, 1),  # Bright baby blue
            size_hint_y=None,
            height=40
        )
        parent_container.add_widget(lead_sheet_title)
        
        # Create a lead sheet style display
        lead_sheet = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=190,
            spacing=5,
            padding=[5, 5]
        )
        
        with lead_sheet.canvas.before:
            Color(0.15, 0.15, 0.17, 1)  # Slightly darker background for lead sheet
            self.lead_sheet_bg = Rectangle(pos=lead_sheet.pos, size=lead_sheet.size)
        
        lead_sheet.bind(size=self._update_lead_sheet_bg, pos=self._update_lead_sheet_bg)
        
        # Title and notation
        notation_box = BoxLayout(size_hint_y=None, height=30)
        notation_label = Label(
            text='Traditional 12-Bar Blues Pattern (4/4 Time)',
            font_name='Roboto',
            font_size='16sp',
            italic=True,
            color=(0.8, 0.8, 0.8, 1)
        )
        notation_box.add_widget(notation_label)
        lead_sheet.add_widget(notation_box)
        
        # Create measure grid - 3 rows of 4 measures each
        measure_style = {
            'background_color': (0.22, 0.22, 0.25, 1),
            'background_normal': '',
            'color': (0.9, 0.9, 0.9, 1),
            'font_name': 'Roboto',
            'font_size': '22sp',
            'bold': True,
            'disabled': True,
            'size_hint_y': None,
            'height': 45
        }
        
        # First line (bars 1-4)
        line1 = BoxLayout(size_hint_y=None, height=45)
        chords1 = ['C7', 'F7', 'C7', 'C7']
        for i, chord in enumerate(chords1):
            bar_num = Label(
                text=f"{i+1}",
                font_name='Roboto',
                font_size='12sp',
                color=(0.6, 0.6, 0.6, 1),
                size_hint_x=None,
                width=20
            )
            line1.add_widget(bar_num)
            
            measure = Button(
                text=chord,
                **measure_style
            )
            line1.add_widget(measure)
        lead_sheet.add_widget(line1)
        
        # Second line (bars 5-8)
        line2 = BoxLayout(size_hint_y=None, height=45)
        chords2 = ['F7', 'F7', 'C7', 'C7']
        for i, chord in enumerate(chords2):
            bar_num = Label(
                text=f"{i+5}",
                font_name='Roboto',
                font_size='12sp',
                color=(0.6, 0.6, 0.6, 1),
                size_hint_x=None,
                width=20
            )
            line2.add_widget(bar_num)
            
            measure = Button(
                text=chord,
                **measure_style
            )
            line2.add_widget(measure)
        lead_sheet.add_widget(line2)
        
        # Third line (bars 9-12)
        line3 = BoxLayout(size_hint_y=None, height=45)
        chords3 = ['G7', 'F7', 'C7', 'G7']
        for i, chord in enumerate(chords3):
            bar_num = Label(
                text=f"{i+9}",
                font_name='Roboto',
                font_size='12sp',
                color=(0.6, 0.6, 0.6, 1),
                size_hint_x=None,
                width=20
            )
            line3.add_widget(bar_num)
            
            measure = Button(
                text=chord,
                **measure_style
            )
            line3.add_widget(measure)
        lead_sheet.add_widget(line3)
        
        # Store references to all measure buttons for highlighting
        # Extract all actual measure buttons (not the bar numbers)
        for row in [line1, line2, line3]:
            measures = [child for child in row.children if isinstance(child, Button)]
            # Reverse because Kivy stores children in reverse order
            measures.reverse()
            self.measure_buttons.extend(measures)
            
        # Add the lead sheet to the controls container
        parent_container.add_widget(lead_sheet)

    def _build_tempo_control(self, parent_container):
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
        
        parent_container.add_widget(tempo_layout)

    def _build_mode_selection(self, parent_container):
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
        
        parent_container.add_widget(mode_layout)

    def _build_control_buttons(self, parent_container):
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
        self.start_button.bind(on_press=self.on_start_pressed)
        
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
        self.stop_button.bind(on_press=self.on_stop_pressed)
        
        control_layout.add_widget(self.start_button)
        control_layout.add_widget(self.stop_button)
        parent_container.add_widget(control_layout)

    def _build_status_area(self, parent_container):
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
            color=(1.0, 1.0, 1.0, 1),  # Pure white text
            bold=True
        )
        status_layout.add_widget(self.status_label)
        
        parent_container.add_widget(status_layout)

    # Update canvas elements
    def _update_rect(self, instance, value):
        """Update the canvas rectangles with window size"""
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def _update_controls_bg(self, instance, value):
        """Update the controls background rectangle"""
        self.controls_bg.pos = instance.pos
        self.controls_bg.size = instance.size
        
    def _update_lead_sheet_bg(self, instance, value):
        """Update the lead sheet background rectangle"""
        self.lead_sheet_bg.pos = instance.pos
        self.lead_sheet_bg.size = instance.size

    def _update_status_bg(self, instance, value):
        """Update the status background rectangle"""
        self.status_bg.pos = instance.pos
        self.status_bg.size = instance.size

    # Event handlers
    def on_tempo_change(self, instance, value):
        """Update the tempo label when slider value changes"""
        self.tempo_label.text = f'Tempo: {int(value)} BPM'

    def on_start_pressed(self, instance):
        """Handle start button press"""
        tempo = self.tempo_slider.value
        mode = self.mode_spinner.text
        
        success, message = self.controller.start_performance(tempo, mode)
        
        if success:
            self.status_label.text = f'Playing - {message}'
            self.start_button.disabled = True
            self.stop_button.disabled = False
            self.mode_spinner.disabled = True
            self.tempo_slider.disabled = True
        else:
            self.status_label.text = message

    def on_stop_pressed(self, instance):
        """Handle stop button press"""
        self.controller.stop_performance()
        self.status_label.text = 'Ready to play'
        self.start_button.disabled = False
        self.stop_button.disabled = True
        self.mode_spinner.disabled = False
        self.tempo_slider.disabled = False

    def update_chord_display(self, bar_index):
        """Update the chord display to highlight the current bar"""
        # Need to run this on the main thread
        def update_ui(dt):
            # Reset all measure buttons in the lead sheet
            for measure in self.measure_buttons:
                measure.background_color = (0.22, 0.22, 0.25, 1)  # Default dark blue-gray
                measure.color = (0.9, 0.9, 0.9, 1)  # Reset to default light gray text
                
            # If bar_index is -1, just reset all measures and return
            if bar_index == -1:
                return
                
            # Calculate current index (0-11)
            current_index = bar_index % 12
            
            # Highlight the current bar in the lead sheet
            if 0 <= current_index < len(self.measure_buttons):
                # Highlight the entire button with bright blue
                self.measure_buttons[current_index].background_color = (0.4, 0.8, 1.0, 1)  # Bright baby blue
                self.measure_buttons[current_index].color = (1.0, 0.6, 0.0, 1)  # Bright orange text
            
            # Save the current bar for future reference
            self.current_bar = bar_index
        
        # Schedule the UI update on the main thread
        Clock.schedule_once(update_ui, 0)

    def on_bar_changed(self, bar_index):
        """Callback that gets called when the bar changes in bass_blues.py"""
        print(f"Bar changed to {bar_index}")
        # Update the UI to reflect the current bar
        self.update_chord_display(bar_index)
        
        # Schedule the chord to dim after the bar duration has passed
        # This ensures it only stays highlighted while being played
        tempo = self.tempo_slider.value
        time_per_bar = (60 / tempo) * 4  # 4 beats per bar
        
        # Schedule the reset to happen at the end of the bar
        # We'll use a slightly shorter time to ensure smooth transitions
        reset_time = max(0.1, time_per_bar * 0.95)  # 95% of bar duration
        Clock.schedule_once(lambda dt: self.update_chord_display(-1), reset_time)
