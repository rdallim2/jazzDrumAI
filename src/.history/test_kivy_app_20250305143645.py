from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window

class TestLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        # Add a label
        self.label = Label(
            text='Welcome to JazzDrumAI',
            font_size='24sp',
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.label)

        # Add a test button
        self.button = Button(
            text='Click Me!',
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': 0.5}
        )
        self.button.bind(on_press=self.on_button_press)
        self.add_widget(self.button)

    def on_button_press(self, instance):
        self.label.text = 'Button Pressed!'

class TestApp(App):
    def build(self):
        # Set window size
        Window.size = (400, 300)
        return TestLayout()

if __name__ == '__main__':
    TestApp().run() 