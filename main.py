import threading

from kivy.base import EventLoop
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.utils import escape_markup
import pyperclip
from kivy.clock import Clock, mainthread
import time

from XDTranslator import XDTranslation
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from fpdf import FPDF

isTaskDone = False


# main app function
class WebImageTranslator(App):
    # Main Build function
    def __init__(self):
        super().__init__()
        self.textLayout = None
        self.imageLayout = None
        self.window = None
        self.loading = None
        self.homeLayout = None

    def build(self):
        Window.clearcolor = (1, 1, 1, 1)

        self.window = GridLayout()
        self.window.cols = 2
        self.window.size_hint = (0.9, 0.9)

        self.homeLayout = GridLayout()
        self.homeLayout.cols = 1
        self.homeLayout.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.homeLayout.rows = 2

        self.imageLayout = GridLayout()
        self.imageLayout.cols = 1

        self.textLayout = GridLayout()
        self.textLayout.cols = 1
        self.textLayout.rows = 1

        self.buttonLayout = GridLayout()
        self.buttonLayout.row_force_default = True
        self.buttonLayout.row_default_height = 70
        self.buttonLayout.spacing = [7, 7]
        self.buttonLayout.cols = 2
        self.buttonLayout.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.buttonLayout.rows = 2

        self.imageLayout.add_widget(Image(source='slid1.webp'))

        self.ask_name = Label(
            text='[b]' + escape_markup("Select The Language That\nYou Want To Translate From 👇") + '[/b]',
            font_size=21,
            color="#000000",
            markup=True,
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        self.korean = Button(text="Korean",
                             bold=True,
                             font_size=18,
                             background_color="#4585F5",
                             background_normal=""
                             )
        self.korean.bind(on_press=self.call_back)

        self.japanese = Button(text="Japanese",
                               bold=True,
                               font_size=18,
                               background_color="#4585F5",
                               background_normal=""
                               )
        self.japanese.bind(on_press=self.call_back)

        self.chines = Button(text="Chines",
                             bold=True,
                             font_size=18,
                             background_color="#4585F5",
                             background_normal=""
                             )
        self.chines.bind(on_press=self.call_back)

        self.hindi = Button(text="Hindi",
                            bold=True,
                            font_size=18,
                            background_color="#4585F5",
                            background_normal=""
                            )
        self.hindi.bind(on_press=self.call_back)

        self.buttonLayout.add_widget(self.korean)
        self.buttonLayout.add_widget(self.japanese)
        self.buttonLayout.add_widget(self.hindi)
        self.buttonLayout.add_widget(self.chines)

        self.textLayout.add_widget(self.ask_name)

        self.homeLayout.add_widget(self.textLayout)
        self.homeLayout.add_widget(self.buttonLayout)

        self.window.add_widget(self.imageLayout)
        self.window.add_widget(self.homeLayout)

        return self.window

    def PopupOk(self, text):
        Window.clearcolor = (1, 1, 1, 1)
        btnclose = Button(text="Translate",
                          size_hint_y=None,
                          height='50sp',
                          bold=True,
                          font_size=18,
                          background_color="#4585F5",
                          background_normal=""
                          )
        content = BoxLayout(orientation='vertical')
        p = Popup(title="Webpage Translator", title_color='#000000', content=content, size=('700dp', '200dp'),
                  size_hint=(None, None),
                  background='#FFFFFF')
        ti = TextInput(font_size='14sp',
                       multiline=False,
                       input_type='text', hint_text="Enter Your Webpage URL")
        content.add_widget(ti)

        def _on_d(*args):
            p.is_visable = False

        p.bind(on_dismiss=_on_d)
        p.is_visable = True

        content.add_widget(btnclose)

        btnclose.bind(on_press=lambda event: self.show_loading(ti.text.strip(), text, p))
        p.open()
        while not p.is_visable:
            EventLoop.idle()
        return ti.text

    def call_back(self, event):
        self.PopupOk(event.text)

    def PopupToSave(self):
        Window.clearcolor = (1, 1, 1, 1)
        btn_pdf = Button(text="Save As PDF",
                         size_hint_y=None,
                         height='50sp',
                         bold=True,
                         font_size=18,
                         background_color="#4585F5",
                         background_normal=""
                         )
        btn_pdf.bind(on_press=lambda event: self.save("pdf", ti.text, p))

        btn_text = Button(text="Save As Txt",
                          size_hint_y=None,
                          height='50sp',
                          bold=True,
                          font_size=18,
                          background_color="#4585F5",
                          background_normal=""
                          )
        btn_text.bind(on_press=lambda event: self.save("txt", ti.text, p))

        btn_copy = Button(text="Close",
                          size_hint_y=None,
                          height='50sp',
                          bold=True,
                          font_size=18,
                          background_color="#4585F5",
                          background_normal=""
                          )
        btn_copy.bind(on_press=lambda event: self.save("copy", ti.text, p))
        content = BoxLayout(orientation='vertical')
        p = Popup(title="Save Translation As Txt, Pdf or Copy Text", title_color='#000000', content=content,
                  size=('700dp', '300dp'),
                  size_hint=(None, None),
                  background='#FFFFFF')
        ti = TextInput(font_size='14sp',
                       multiline=False,
                       input_type='text', hint_text="Enter File Name You Want To Save")

        def _on_d(*args):
            p.is_visable = False

        p.bind(on_dismiss=_on_d)
        p.is_visable = True

        content.add_widget(ti)
        content.add_widget(btn_pdf)
        content.add_widget(btn_text)
        content.add_widget(btn_copy)

        p.open()
        while not p.is_visable:
            EventLoop.idle()

    def show_loading(self, url, text, p):
        if url != "":
            p.dismiss()
            self.PopupToSave()
            self.showLoadingPopUp()
            try:
                threading.Thread(target=lambda : self.statTranslation(url, text, 'en')).start()
            except:
                print("Error: unable to start thread")

    def save(self, type, name, p):
        if name != "":
            if type == "pdf":
                pdf = FPDF()
                pdf.add_page()
                pdf.add_font("Arial", "", "font/Arialn.ttf", uni=True)
                pdf.set_font("Arial", size=18)
                with open('ch.txt', 'r', encoding="utf8") as file:
                    for x in file.readlines():
                        pdf.cell(200, 10, txt=x, ln=1, align='C')
                pdf.output("Output/" + name + ".pdf")
                p.dismiss()
            elif type == "txt":
                text = ""
                with open('ch.txt', 'r', encoding="utf8") as file:
                    for x in file:
                        text = text + x
                with open("Output/" + name + ".txt", "w", encoding="utf8") as file:
                    file.write(text)
                    p.dismiss()
            else:
               p.dismiss()

    def showLoadingPopUp(self):
        Window.clearcolor = (1, 1, 1, 1)
        content = BoxLayout(orientation='vertical')
        self.loading = Popup(title="Translating", title_color='#000000', content=content, size=('700dp', '200dp'),
                             size_hint=(None, None),
                             auto_dismiss=False,
                             background='#FFFFFF')
        content.add_widget(Label(text="Translating...", color="#000000"))

        def _on_d(*args):
            self.loading.is_visable = False

        self.loading.bind(on_dismiss=_on_d)
        self.loading.is_visable = True

        self.loading.open()

        while not self.loading.is_visable:
            EventLoop.idle()

    def statTranslation(self, url, from_lang, to_lang='en'):
        img_list = XDTranslation.get_images(url)
        txt = ""
        for img in img_list:
            if img.endswith('.jpg'):
                print('Translating...')
                if from_lang == 'Korean':
                    v = XDTranslation.image_translation_korean(img, to_lang)
                elif from_lang == 'Japanese':
                    v = XDTranslation.image_translation_japanese(img, to_lang)
                elif from_lang == 'Chines':
                    v = XDTranslation.image_translation_chinese(img, to_lang)
                else:
                    v = XDTranslation.image_translation_hindi(img, to_lang)
                txt = txt + "\n"
                txt = txt + v

        with open('ch.txt', 'w', encoding="utf-8") as file:
            file.write(txt)
            print("Done")
            self.loading.dismiss()


if __name__ == '__main__':
    WebImageTranslator().run()
