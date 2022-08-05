import io
import requests
import pytesseract
from PIL import Image
import re
from urllib.request import Request, urlopen
from googletrans import Translator


class XDTranslation:

    # Methods For Getting Image Text
    @classmethod
    def image_translation_korean(cls, path, lang):
        img_resp = requests.get(path)
        img = Image.open(io.BytesIO(img_resp.content))
        pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'
        text = pytesseract.image_to_string(img, lang="ko", config='--psm 6')
        # print(text)
        translator = Translator()
        translated_text = translator.translate(text, src='ko', dest=lang)
        return translated_text.text

    @classmethod
    def image_translation_japanese(cls, path, lang):
        img_resp = requests.get(path)
        img = Image.open(io.BytesIO(img_resp.content))
        pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'
        text = pytesseract.image_to_string(img, lang="jp", config='--psm 6')
        # print(text)
        translator = Translator()
        translated_text = translator.translate(text, src='jp', dest=lang)
        return translated_text.text

    @classmethod
    def image_translation_chinese(cls, path, lang):
        img_resp = requests.get(path)
        img = Image.open(io.BytesIO(img_resp.content))
        pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'
        text = pytesseract.image_to_string(img, lang="zh-cn", config='--psm 6')
        # print(text)
        translator = Translator()
        translated_text = translator.translate(text, src='zh-cn', dest=lang)
        return translated_text.text

    @classmethod
    def image_translation_hindi(cls, path, lang):
        img_resp = requests.get(path)
        img = Image.open(io.BytesIO(img_resp.content))
        pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'
        text = pytesseract.image_to_string(img, lang="hi", config='--psm 6')
        # print(text)
        translator = Translator()
        translated_text = translator.translate(text, src='hi', dest=lang)
        return translated_text.text

    # Method For Getting List Of Image From Url
    @classmethod
    def get_images(cls, path):
        req = Request(path, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'})
        # req.set_proxy('http://113.160.218.14:8888', 'http')
        webpage = urlopen(req).read()
        # print(webpage.decode('utf8'))
        a = webpage.decode('utf8')
        data = {}
        if re.search('src="([^"]+)"', a):
            data['src'] = re.findall('src="(.*?)"', a, re.DOTALL)

        return data.get('src')

    # Method For Translating
    @classmethod
    def translate(cls, url, from_lang, to_lang="en"):
        img_list = cls.get_images(url)
        txt = ""
        for img in img_list:
            if img.endswith('.jpg'):
                print('Translating...')
                if from_lang == 'ko':
                    v = cls.image_translation_korean(img, to_lang)
                elif from_lang == 'jp':
                    v = cls.image_translation_japanese(img, to_lang)
                elif from_lang == 'ch':
                    v = cls.image_translation_chinese(img, to_lang)
                else:
                    v = cls.image_translation_hindi(img, to_lang)
                txt = txt + "\n"
                txt = txt + v

        with open('ch.txt', 'w', encoding="utf-8") as file:
            file.write(txt)

        print(txt)


def main():
    XDTranslation.translate("https://booktoki147.com/novel/766053?spage=1", "ko", "en")


if __name__ == '__main__':
    main()
