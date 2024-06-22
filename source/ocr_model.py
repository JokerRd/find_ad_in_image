from paddleocr import PaddleOCR

en_rus_dict = {
    'e': 'е',
    't': 'т',
    'o': 'о',
    'p': 'р',
    'a': 'а',
    'h': 'н',
    'k': 'к',
    'x': 'х',
    'c': 'с',
    'b': 'б',
    'm': 'м'
}


def transform_to_rus(text: str) -> str:
    text = text.lower()
    result = ''
    for char in text:
        if char in en_rus_dict:
            result += en_rus_dict[char]
        else:
            result += char
    return result


class OCRModel:

    def __init__(self, lang):
        self.lang = lang
        self.model = PaddleOCR(lang=lang, det_db_score_mode='slow',
                               enable_mkldnn=True,
                               det_max_side_len=1500, use_gpu=False,
                               ocr_version='PP-OCRv4')

    def image_to_text(self, image: bytes) -> [str]:
        results = self.model.ocr(image, cls=False)
        try:
            texts = list(map(lambda result: result[1][0], results[0]))
        except TypeError:
            texts = ""
        if self.lang == 'ru':
            texts = list(map(transform_to_rus, texts))
        return texts
