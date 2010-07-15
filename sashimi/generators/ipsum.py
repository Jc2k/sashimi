
import os, random, codecs
from sashimi.generators.registry import registry

def sibpath(file):
    dir, p = os.path.split(__file__)
    return os.path.join(dir, file)

class Ipsum(object):

    num_paragraphs = 3
    wordfile = sibpath("ipsum.txt")

    def __init__(self):
        self.words = codecs.open(self.wordfile, 'r', 'utf-8').read().split()
        self.words_len = len(self.words)

    def get_paragraphs(self):
        paragraphs = []
        for i in range(self.num_paragraphs):
            type = random.randint(0, 2)
            if type == 0:
                sentence_size = random.randint(2, 4)
            elif type == 1:
                sentence_size = random.randint(3, 6)
            else:
                sentence_size = random.randint(4, 9)
            paragraphs.append(self.get_paragraph(sentence_size))
        return "\n\n".join(paragraphs)

    def get_word(self):
        return self.words[random.randint(0, self.words_len-1)]

    def get_sentence(self):
        length = random.randint(3,15)
        raw = ' '.join([ self.get_word() for i in range(length)])
        return raw[0].upper() + raw[1:] + '. '

    def get_paragraph(self, sentences):
        return ''.join([ self.get_sentence() for i in range(sentences)])


class TextFuzzer(object):

    ipsum = Ipsum()

    @classmethod
    def can_fuzz(cls, field):
        if field["type"] == "text":
            if not "regex" in field and not "vocabulary" in field:
                return True
        return False

    def fuzz(self, field):
        return self.ipsum.get_paragraphs()


class StringFuzzer(object):

    ipsum = Ipsum()

    @classmethod
    def can_fuzz(cls, field):
        if field["type"] == "string":
            if not "regex" in field and not "vocabulary" in field:
                return True
        return False

    def fuzz(self, field):
        return self.ipsum.get_sentence()


class LinesFuzzer(object):

    ipsum = Ipsum()

    @classmethod
    def can_fuzz(cls, field):
        if field["type"] == "lines":
            if not "regex" in field and not "vocabulary" in field:
                return True
        return False

    def fuzz(self, field):
        return "\n".join(self.ipsum.get_sentence() for x in range(random.randint(3, 10)))


registry.register(TextFuzzer)
registry.register(StringFuzzer)
registry.register(LinesFuzzer)

