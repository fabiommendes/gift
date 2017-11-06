import ox
import re
import io
from random import shuffle

class Gift:
    """
    Represents the result of parsing an Gift string.
    """
    def __init__(self):
        self.question = ""
        self.options = []
        self.answer = ""
        self._token_list = []

    def lexer(self, string):
        lexer = ox.make_lexer([
                ('ANSWER', r'=.+?(?=~)'),
                ('OPTION', r'~.+?(?=[~}])'),
                ('QUESTION', r'.+?(?={)'),
                ('LBRACKET', r'{'),
                ('RBRACKET', r'}'),
        ])

        return lexer(string)

    def parse(self, string):

        self.lexer(string)

        self._token_list = ['ANSWER', 'OPTION', 'QUESTION', 'LBRACKET', 'RBRACKET']
        
        parser = ox.make_parser([
            ('question : cmd LBRACKET answer options RBRACKET', lambda x, a, y , z, b: (x , y ,z)),
            ('cmd : QUESTION', lambda x: x),
            ('options : options option', lambda x,y: x + [y]),
            ('options : option', lambda x: [x]),
            ('option : OPTION', lambda x: x[1:].rstrip()),
            ('answer : ANSWER', lambda x: x[1:].rstrip()),
        ], self._token_list)
        
        ast = parser(self.lexer(string))
        
        return ast

    def append(self, s):
        self.options.append(s)

    def __str__(self):
        s = self.question + '\n'

        for option in self.options:
            s += option + '\n'

        s += "ANSWER: " + self.answer

        return s

def load(file_or_string):
    """
    Load a file or string in the Gift format and return a parsed object.

    Args:
        file_or_string:
            A file object containing the Gift source or a string.

    Returns:
        An :cls:`Gift` instance.
    """
    gift = Gift()
    try:
        file_obj = open(file_or_string)
        content = file_obj.read()
        file_obj.close()
    except:
        content = file_or_string
    ast = gift.parse(content)

    gift.answer = ast[1]

    for option in ast[2]:
        gift.options += [option]

    gift.options += [gift.answer];
    shuffle(gift.options)

    gift.question = ast[0]

    return gift

def dump(gift, file=None):
    """
    Writes gift object in the given file. If no file is given, return a string
    with the file contents.
    """ 
    gift_content = str(gift)

    if file is not None:
        file = open(file, "w")
        file.write(gift_content)
        file.close() 
        return ""
    else:
        print(gift_content)
        return gift_content

    return gift_content

gift = Gift()

dump(load("Who's buried in Grant's tomb?{=Grant ~no one ~Napoleon ~Churchill ~Mother Teresa }"))

