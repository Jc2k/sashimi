
import random

from sashimi.node import Node
from sashimi.generators.registry import registry


class Character(Node):
    name = "Ch"

    def __init__(self, character):
        super(Character, self).__init__()
        self.character = character

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
                if regex[ccpos] == "s":
                    pass
                elif regex[ccpos] == "S":
                    pass
                elif regex[ccpos] == "d":
                    pass
                elif regex[ccpos] == "w":
                    pass
                elif regex[ccpos] == "W":
                    pass
                elif regex[ccpos] == "b":
                    pass
                elif regex[ccpos] == "B":
                    pass
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
        self.last_leaf = self.last_branch.parent
        self.last_branch = self.last_branch.parent.parent

    def repetition(self, min=0, max=-1):
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
        return False

    def fuzz(self, field):
        return

registry.register(RegexFuzzer)


