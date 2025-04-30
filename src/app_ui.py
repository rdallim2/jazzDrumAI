from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class MyLayout(BoxLayout):
    pass

class MyApp(App):
    def build(self):
        return MyLayout()

    def play_pause(self):
        print("Play/Pause button pressed")

if __name__ == '__main__':
    MyApp().run()