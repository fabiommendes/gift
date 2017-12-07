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
            ('ANSWER', r'=.+?(?=[~\#])'),
            ('OPTION', r'~.+?(?=[~}\#])'),
            ('FEEDBACK', r'\#.+?(?=[~}])'),
            ('QUESTION', r'.+?(?={)'),
            ('TRUE_VALUE', r'T|TRUE'),
            ('FALSE_VALUE', r'F|FALSE'),
            ('LBRACKET', r'{'),
            ('RBRACKET', r'}'),
        ])

        return lexer(string)

    def parse(self, string):

        self.lexer(string)

        self._token_list = [
            'ANSWER', 'OPTION', 'QUESTION',
            'TRUE_VALUE', 'FALSE_VALUE',
            'LBRACKET', 'RBRACKET', 'FEEDBACK'
        ]
        
        print(self.lexer(string))

        parser = ox.make_parser([
            ('question : statement', lambda x: x),
            ('statement : cmd LBRACKET TRUE_VALUE RBRACKET', lambda x1,x2,x3,x4: (x1, x3)),
            ('statement : cmd LBRACKET FALSE_VALUE RBRACKET', lambda x1,x2,x3,x4: (x1, x3)),
            ('statement : cmd LBRACKET answer options RBRACKET', lambda x, a, y , z, b: (x , y ,z)),
            ('cmd : QUESTION', lambda x: x),
            ('options : options option', lambda x,y: x + [y]),
            ('options : option', lambda x: [x]),
            ('option : option FEEDBACK', lambda x,y: (x, y)),
            ('option : OPTION', lambda x: x[1:].rstrip()),
            ('option : TRUE_VALUE', lambda x: x),
            ('option : FALSE_VALUE', lambda x: x),
            ('answer : answer FEEDBACK', lambda x,y: (x, y)),
            ('answer : ANSWER', lambda x: x[1:].rstrip()),
        ], self._token_list)
        
        ast = parser(self.lexer(string))
        
        return ast

    def append(self, s):
        self.options.append(s)

    def __str__(self):
        s = self.question + '\n'

        for option in self.options:
            if(type(option) == tuple):
                s += option[0] + ' Feedback: ' + option[1] + '\n'
            else:
                s += str(option) + '\n'

        if(type(self.answer) == tuple):
            s += "ANSWER" + self.answer[0]
        else:
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

    if len(ast) > 2:
        for option in ast[2]:
            gift.options += [option]
    else:
        # Do nothing 
        pass
        
    
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
print('\n')
dump(load("TestQ{=Test # You're right! ~OtherTest # You're wrong! ~AnotherTest}"))
print('\n')
dump(load("1+1=2 {T}"))
print('\n')
dump(load("1+1=3 {F}"))

