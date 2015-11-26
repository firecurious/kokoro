import regex as re
from textblob import TextBlob

class Words(object):

    def __init__(self):
        """So many words."""

        _file = "/usr/share/dict/words"
        with open(_file, 'r') as f:
            data = [word.replace("\n", "") for word in f]

        self.data = data

class Translate(object):
    """Translates things that are not in English."""

    def __init__(self):
        self.commands = {}
        self.passive = [self._translate]

        self.words = Words().data

    def _german(self, text):
        blob = TextBlob(text)

        try:
            return str(blob.translate(to="en"))
        except:
            return text

    def _rot13(self, text):
        """Translates rot13."""

        try:
            return text.encode("rot13")
        except: #unicode error; garbage characters
            return text

    def _doublefrench(self, text):
        """Not passive. Translates Double French."""

        if "os" in text.lower():
            print "os detected"
            text = text.replace("os", "").replace("Os", "").replace("OS", "")

        return text

    def _strip(self, text):
        """Strips the punctuation from a given string and returns as a list."""

        text = re.sub(ur"\p{P}+", "", text) #strip punctuation
        text = text.split()
        return text

    def _garbage(self, text):
        """Checks if some text does not seem to be in English."""

        text = self._strip(text)
        garbage_words = [word for word in text if word.lower() not in self.words]

        if len(garbage_words) >= (len(text) - len(garbage_words)):
            return True
        else:
            return False

    def _better(self, original_text, translation):
        """Compares two strings to see which one has more English words and
        returns True or False.
        """

        original_text = self._strip(original_text)
        translation = self._strip(translation)

        orig_n = len([w for w in original_text if w.lower() in self.words])
        trans_n = len([w for w in translation if w.lower() in self.words])

        if trans_n > orig_n:
            return True
        else:
            return False

    def _translate(self):
        """passive"""

        translations = [self._doublefrench, self._rot13, self._german]

        text = self.message.Body

        if self._garbage(text):
            for method in translations:
                translation = method(text)

                if self._better(text, translation):
                    self.chat.SendMessage("Translation: " + translation)

Class = Translate
