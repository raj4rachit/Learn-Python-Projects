import kivy
from kivy.app import App
from kivy.uix.label import Label

class SpartanApp(App):
    def build(self):
        return Label(text='Hello Rachit!!!!,')


if __name__ == '__main__':
    SpartanApp().run()