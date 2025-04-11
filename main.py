from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label

class HelloWorldApp(App):
    def build(self):
        return Builder.load_file("main.kv")
    
if __name__ == "__main__":
    HelloWorldApp().run()

