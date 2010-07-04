
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

    def can_fuzz(cls, field):
        return False

    def fuzz(self, field):
        paragraphs = []
        for i in range(self.num_paragraphs):
            type = random.randint(0, 2)
            if type == 0:
                sentence_size = random.randint(2, 4)
            elif type == 1:
                sentence_size = random.randint(3, 6)
            else:
                sentence_size = random.randint(4, 9)
            paragraphs.append(self._getparagraph(sentence_size))
        return "\n\n".join(paragraphs)

    def _getword(self):
        return self.words[random.randint(0, self.words_len-1)]

    def _getsentence(self):
        length = random.randint(3,15)
        raw = ' '.join([ self._getword() for i in range(length)])
        return raw[0].upper() + raw[1:] + '. '

    def _getparagraph(self, sentences):
        return ''.join([ self._getsentence() for i in range(sentences)])


class UpsideDownIpsum(Ipsum):

    wordfile = sibpath("udipsum.txt")


registry.register(Ipsum)
registry.register(UpsideDownIpsum)


