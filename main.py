from kivy.app import App

from widgets.file_upload_layout import FileUploadLayout


class FileUploadApp(App):
    def build(self):
        return FileUploadLayout()


if __name__ == "__main__":
    FileUploadApp().run()
