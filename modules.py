import re
import unicodedata

from cleanco import basename
from transliterate.decorators import transliterate_function

a = ord('а') # кириллическая "А"
RUS_ALPHABET = ''.join([chr(i) for i in range(a, a+6)] + [chr(a+33)] + [chr(i) for i in range(a+6, a+32)])

def preprocessing(x: str) -> str:
    def rus_preprocess(x: str) -> str:
        forms_of_ownership = [
            'ооо',
            'оао',
            'общество с ограниченной ответственностью',
            'открытое акционерное общество',
            'филиал компании'
        ]

        for form in forms_of_ownership:
            pattern = re.compile(form)
            x = pattern.sub('', x)

        return x

    @transliterate_function(language_code='ru', reversed=True)
    def translit(x: str) -> str:
        return x

    x = x.strip().lower()
    x = basename(x) if not bool(set(RUS_ALPHABET).intersection(set(x.lower()))) else rus_preprocess(x)
    x = unicodedata.normalize('NFKD', x).encode('ASCII', 'ignore').decode() if not bool(
        set(RUS_ALPHABET).intersection(set(x.lower()))) else translit(x)
    x = basename(x)
    x = re.sub(r'[^\w\s]', ' ', x)

    return ' '.join([s for s in x.split()]) if len(x.split()) != 0 else '-' * 5
