import sys
import os
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, GObject, Adw
from PIL import Image
import pytesseract
from libretranslatepy import LibreTranslateAPI

tl = LibreTranslateAPI("http://127.0.0.1:5000")

IMAGE_PATH = "/home/marius/Projects/translate/image.png"

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(512, 512)
        self.set_title("Translate")

        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)

        # form and attach grid to window
        self.grid = Gtk.Grid(column_spacing=15, row_spacing=15)
        self.set_child(self.grid)
        
        # image frame object
        self.img_frame = Gtk.Frame()
        self.img = Gtk.Image()
        
        # text frame object
        self.text_frame = Gtk.Frame()
        self.text_view = Gtk.TextView()
        self.text_buffer = self.text_view.get_buffer()
        scroll_win = Gtk.ScrolledWindow()
        scroll_win.set_child(self.text_view)

        # reikia copy mygtuko viduje text frame
        #self.copy = Gtk.Image.new_from_icon_name("copy", 20)   

        #self.text_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        #self.text_box.append(self.text_frame)
        #self.text_box.append(self.copy)

        # translation frame object
        self.translation_frame = Gtk.Frame()
        self.translation_view = Gtk.TextView()
        self.translation_buffer = self.translation_view.get_buffer()
        scroll_win2 = Gtk.ScrolledWindow()
        scroll_win2.set_child(self.translation_view)

        # open file button
        self.open_button = Gtk.Button(label="Open")
        self.header.pack_start(self.open_button)

        self.open_button.set_icon_name("document-open-symbolic")
        self.open_dialog = Gtk.FileChooserNative.new(title="Choose a file",
                                                     parent=self, action=Gtk.FileChooserAction.OPEN)
        f = Gtk.FileFilter()
        f.set_name("Image files")
        f.add_mime_type("image/jpeg")
        f.add_mime_type("image/png")
        self.open_dialog.add_filter(f)
        self.open_dialog.connect("response", self.open_response)
        self.open_button.connect("clicked", self.show_open_dialog)

        # button objects
        self.button = Gtk.Button(label="Selection")
        self.button.connect('clicked', self.Selection)
        self.button1 = Gtk.Button(label="Window")
        self.button1.connect('clicked', self.Window)
        self.translate = Gtk.Button(label="Translate")
        self.translate.connect('clicked', self.Translate)
        self.text_buffer.connect('changed', self.Text_Change)

        # entry objects
        self.entry_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.entry = Gtk.Entry()
        self.entry2 = Gtk.Entry()
        # entry object box
        self.entry_box.append(self.entry)
        self.entry_box.append(self.entry2)

        # entry completion
        self.langs = ['English','Spanish','Deutch']
        self.list = Gtk.ListStore(str)
        self.list2 = Gtk.ListStore(str)
        for x in self.langs:
            self.list.append([x])
            self.list2.append([x])

        self.comp = Gtk.EntryCompletion()
        self.comp.set_text_column(0)
        self.comp.set_model(self.list)
        self.comp.set_inline_completion(True)
        self.comp.set_inline_selection(True)

        self.comp2 = Gtk.EntryCompletion()
        self.comp2.set_text_column(0)
        self.comp2.set_model(self.list2)
        self.comp2.set_inline_completion(True)
        self.comp2.set_inline_selection(True)

        self.entry.set_completion(self.comp)
        self.entry2.set_completion(self.comp2)
        self.entry.set_placeholder_text('From')
        self.entry2.set_placeholder_text('To')

        # attach objects to grid
        self.grid.attach(self.button, 0, 0, 1, 1)
        self.grid.attach(self.button1, 0, 1, 1, 1)
        self.grid.attach(self.translate, 0, 2, 1, 1)
        self.grid.attach(self.entry_box, 0, 11, 18, 1)

        # grid.attach(object, column, row, width, height)
        self.grid.attach(self.img_frame, 18, 0, 24, 12)
        self.grid.attach(self.text_frame, 0, 12, 18, 16)
        self.grid.attach(self.translation_frame, 18, 12, 24, 16)
        self.img_frame.set_child(self.img)
        self.text_frame.set_child(scroll_win)
        self.translation_frame.set_child(scroll_win2)

    # open file dialog
    def show_open_dialog(self, button):
        self.open_dialog.show()

    def open_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            file = dialog.get_file()
            filename = file.get_path()
            self.img.set_from_file(filename)

    # button click events
    def Selection(self, button):
        os.system('gnome-screenshot -a -f /home/$USER/Projects/translate/image.png')
        self.img.set_from_file(IMAGE_PATH)
        text = str(self.extract_text())
        self.text_buffer.set_text(text)
        self.Translate()

    def Window(self, button):
        os.system('gnome-screenshot -w -f /home/$USER/Projects/translate/image.png')
        self.img.set_from_file(IMAGE_PATH)
        self.extract_text()
        self.Translate()

    def Translate(self, button):
        lang_from = self.entry.get_text()
        lang_to = self.entry2.get_text()

        match lang_from:
            case 'English':
                lang_from = 'en'
            case 'Spanish':
                lang_from = 'es'
            case 'Deutch':
                lang_from = 'de'
        
        match lang_to:
            case 'English':
                lang_to = 'en'
            case 'Spanish':
                lang_to = 'es'
            case 'Deutch':
                lang_to = 'de'

        tl_text = tl.translate(self.text, "en", "es")
        self.translation_buffer.set_text(tl_text)

    def Text_Change(self, button):
        start_iter = self.text_buffer.get_start_iter()
        end_iter = self.text_buffer.get_end_iter()
        self.text = self.text_buffer.get_text(start_iter, end_iter, True)  
        self.Translate()

    def extract_text(self):
        img = Image.open(IMAGE_PATH)
        self.text = pytesseract.image_to_string(img) #, lang = "chi_sim"
        return self.text

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

app = MyApp(application_id="com.example.GtkApplication")
app.run(sys.argv)

# take a screenshot of the screen and store it in memory, then
# convert the PIL/Pillow image to an OpenCV compatible NumPy array
# and finally write the image to memory

#image = pyautogui.screenshot()
# convert the image to a NumPy array and swap color channels from RGB (PIL/Pillow) to BGR (OpenCV)
#image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
#cv2.imwrite("in_memory_to_disk.png", image)
