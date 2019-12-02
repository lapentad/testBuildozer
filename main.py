'''
Basic camera example
Default picture is saved as
/sdcard/org.test.cameraexample/enter_file_name_here.jpg
'''
from __future__ import unicode_literals

from os import getcwd
from os.path import exists
from os.path import splitext

import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.logger import Logger

from plyer import camera
from plyer import filechooser

from textwrap import dedent


class FileChoose(Button):
    '''
    Button that triggers 'filechooser.open_file()' and processes
    the data response from filechooser Activity.
    '''

    selection = ListProperty([])

    def choose(self):
        '''
        Call plyer filechooser API to run a filechooser Activity.
        '''
        filechooser.open_file(on_selection=self.handle_selection)

    def handle_selection(self, selection):
        '''
        Callback function for handling the selection response from Activity.
        '''
        self.selection = selection

    def on_selection(self, *a, **k):
        '''
        Update TextInput.text after FileChoose.selection is changed
        via FileChoose.handle_selection.
        '''
        App.get_running_app().root.ids.result.text = str(self.selection)
		
class ChooserApp(App):
    '''
    Application class with root built in KV.
    '''

    def build(self):
        return Builder.load_string(dedent('''
		<FileChoose>:
		BoxLayout:
			BoxLayout:
				orientation: 'vertical'
				TextInput:
					id: result
					text: ''
					hint_text: 'selected path'
				FileChoose:
					size_hint_y: 0.1
					on_release: self.choose()
					text: 'Select a file'
        '''))

class CameraDemo(FloatLayout):
    def __init__(self):
        super(CameraDemo, self).__init__()
        self.cwd = getcwd() + "/"
        self.ids.path_label.text = self.cwd

    def do_capture(self):
        filepath = self.cwd + self.ids.filename_text.text
        ext = splitext(filepath)[-1].lower()

        if(exists(filepath)):
            popup = MsgPopup("Picture with this name already exists!")
            popup.open()
            return False

        try:
            camera.take_picture(filename=filepath,
                                on_complete=self.camera_callback)
        except NotImplementedError:
            popup = MsgPopup(
                "This feature has not yet been implemented for this platform.")
            popup.open()

    def camera_callback(self, filepath):
        if(exists(filepath)):
            popup = MsgPopup("Picture saved!")
            popup.open()
        else:
            popup = MsgPopup("Could not save your picture!")
            popup.open()


class CameraDemoApp(App):
    def __init__(self):
        super(CameraDemoApp, self).__init__()
        self.demo = None

    def build(self):
        self.demo = CameraDemo()
        return self.demo

    def on_pause(self):
        return True

    def on_resume(self):
        pass


class MsgPopup(Popup):
    def __init__(self, msg):
        super(MsgPopup, self).__init__()
        self.ids.message_label.text = msg


if __name__ == '__main__':
    CameraDemoApp().run()