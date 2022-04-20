from kivy.app import App

from widgets.file_upload_layout import FileUploadLayout


class FileUploadApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = None

    def build(self):
        self.layout = FileUploadLayout()
        return self.layout

    def on_stop(self):
        self.layout.exit()


if __name__ == "__main__":
    FileUploadApp().run()
