
import random
import unicodedata
from string import printable

from sashimi.node import Node
from sashimi.generators.registry import registry


class Character(Node):
    name = "Ch"

    def __init__(self, character):
        super(Character, self).__init__()
        self.character = character

    def all(self):
        yield self.character

    def random(self):
        return self.character

class Sequence(Node):
    name = "Sq"

    def random(self):
        return "".join(n.random() for n in self.children)


class Alternative(Node):
    name = "Al"

    def random(self):
        return random.choice(self.children).random()


class Repetition(Node):
    name = "Re"

    def __init__(self, node, min=0, max=-1):
        super(Repetition, self).__init__()
        node.parent.reparent_child(node, self)
        self.min = min
        self.max = max

    def random(self):
        if self.max < 0:
            max = 100
        else:
            max = self.max
        return "".join(self.children[0].random() for i in range(self.min, max))


class CharacterClass(Node):
    name = "Cc"

    def __init__(self, negated, characters=None):
        super(CharacterClass, self).__init__()
        self.negated = negated
        self.characters = []
        if characters:
            self.characters.extend(characters)

        if self.negated:
            self.name += "^"

    def all(self):
        for char in self.characters:
            yield char
        for child in self.children:
            for char in child.all():
                yield char

    def random(self):
        characters = set(list(self.all()))
        if self.negated:
            negation = set(all_chars)
            characters = negation - characters

        retval = random.choice(list(characters))
        return retval

#swap these round for spammy unicode fun
#all_chars = (unichr(i) for i in xrange(0x110000))
all_chars = [unicode(c) for c in printable if c not in "\x0b\x0c"]
digits = [str(x) for x in range(10)]
words = [c for c in all_chars if unicodedata.category(c).startswith("L")] + digits + ["_"]
spaces = [" ", "\t", "\n", "\r"]


class Tokenizer(object):

    def __init__(self):
        self.pos = 0

    def visit(self, regex, visitor):
        self.pos = 0

        if regex[0:1] == "^":
            self.pos += 1

        while self.pos < len(regex):
            if regex[self.pos] == "\\":
                ccpos = self.pos + 1

                # Switch table of all "\F" type escapes we support
                if regex[ccpos] in ("s", "S", "w", "W", "d", "D"):
                    visitor.builtin_class(regex[ccpos])
                elif regex[ccpos] == "r":
                    visitor.character("\r")
                elif regex[ccpos] == "n":
                    visitor.character("\n")
                elif regex[ccpos] == "\\":
                    visitor.character("\\")
                elif regex[ccpos] == "(":
                    visitor.character("(")
                elif regex[ccpos] == ")":
                    visitor.character(")")
                else:
                    raise ValueError("Incorrect or unsupported regex expression: \%s" % regex[ccpos])

                # Advance pointer
                self.pos = ccpos + 1
            elif regex[self.pos] == "(":
                visitor.start_group()
                self.pos += 1
            elif regex[self.pos] == ")":
                visitor.end_group()
                self.pos += 1
            elif regex[self.pos] == "|":
                visitor.alternative()
                self.pos += 1
            elif regex[self.pos] == "?":
                visitor.repetition(0, 1)
                self.pos += 1
            elif regex[self.pos] == "*":
                visitor.repetition(0, -1)
                self.pos += 1
            elif regex[self.pos] == "+":
                visitor.repetition(1, -1)
                self.pos += 1
            elif regex[self.pos] == "{":
                endpos = self.pos + regex[self.pos:].find("}")
                min, max = regex[self.pos+1:endpos].split(",")
                try:
                    min, max = int(min), int(max)
                except:
                    raise ValueError("Error in regex, and i need a better error message")
                visitor.repetition(min, max)
                self.pos = endpos + 1
            elif regex[self.pos] == "[":
                if regex[self.pos+1] == "^":
                    visitor.start_class(True)
                    self.pos += 2
                else:
                    visitor.start_class(False)
                    self.pos += 1
            elif regex[self.pos] == "]":
                visitor.end_class()
                self.pos += 1
            else:
                visitor.character(regex[self.pos])
                self.pos += 1


class TreeGenerator(object):

    def __init__(self):
        self.root = Sequence()
        self.last_branch = self.root
        self.last_leaf = self.last_branch

    def character(self, character):
        c = Character(character)
        self.last_branch.append_child(c)
        self.last_leaf = c

    def start_group(self):
        if isinstance(self.last_branch, CharacterClass):
            raise ValueError("Cannot have a group inside a character class")
        group = Alternative()
        child = Sequence()
        group.append_child(child)

        self.last_branch.append_child(group)
        self.last_branch = child
        self.last_leaf = child

    def alternative(self):
        self.last_branch = self.last_branch.parent
        child = Sequence()
        self.last_branch.append_child(child)
        self.last_branch = child
        self.last_leaf = child

    def end_group(self):
        #FIxME: I don't trust this, see end_class()
        self.last_leaf = self.last_branch.parent
        self.last_branch = self.last_branch.parent.parent

    def builtin_class(self, cls):
        cc = {
            "s": CharacterClass(False, spaces),
            "S": CharacterClass(True, spaces),
            "w": CharacterClass(False, words),
            "W": CharacterClass(True, words),
            "d": CharacterClass(False, digits),
            "D": CharacterClass(True, digits),
            }[cls]

        self.last_branch.append_child(cc)
        self.last_leaf = cc

    def start_class(self, negated):
        cc = CharacterClass(negated)
        self.last_branch.append_child(cc)
        self.last_branch = cc
        self.last_leaf = cc

    def end_class(self):
        self.last_leaf = self.last_branch
        self.last_branch = self.last_branch.parent

    def repetition(self, min=0, max=-1):
        if isinstance(self.last_branch, CharacterClass):
            raise ValueError("Cannot have a repetition inside a character class")
        r = Repetition(self.last_leaf, min, max)
        self.last_branch.append_child(r)
        self.last_leaf = r


def get_regex_tree(regex):
    visitor = TreeGenerator()
    tokenizer = Tokenizer()
    tokenizer.visit(regex, visitor)
    return visitor.root


class RegexFuzzer(object):

    @classmethod
    def can_fuzz(cls, field):
        if "regex" in field:
            return True
        return False

    def fuzz(self, field, content_types):
        return get_regex_tree(field['regex']).random()

registry.register(RegexFuzzer)


