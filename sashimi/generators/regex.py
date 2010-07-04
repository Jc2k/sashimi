
class Character(object):

    def __init__(self, character):
        self.character = character


class Sequence(object):

    def __init__(self, *sequence):
        self.sequence = sequence


class Alternative(object):

    def __init__(self, *alternatives):
        self.alternatives = alternatives


class Repetition(object):

    def __init__(self, node, min=0, max=-1):
        self.node = node
        self.min = min
        self.max = max


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

    def character(self, character):
        c = Character(character)

    def start_group(self):
        pass

    def end_group(self):
        pass

    def repetition(self, min=0, max=-1):
        node = None
        r = Repetition(node, min, max)


