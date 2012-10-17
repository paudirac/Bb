"""
Parser modules.

>>> list(parse("a b"))
['a', 'b']

>>> list(parse("1 2"))
[1, 2]
"""

from collections import defaultdict

# : + ( x y -- x ) x y opplus
def bb_plus(stack):
    last = stack.pop()
    blast = stack.pop()
    return stack + bb_stack(blast + last)

def bb_minus(stack):
    last = stack.pop()
    blast = stack.pop()
    return stack + bb_stack(blast - last)

def tokens(text):
    """
    >>> tokens("a b")
    ['a', 'b']

    >>> tokens("1 2")
    ['1', '2']
    """
    return text.split(" ")

def symbol(token):
    """
    >>> symbol("abracadabra")
    'abracadabra'

    >>> symbol("42")
    42
    """
    import re
    num_int = re.compile('\d+')
    return int(token) if num_int.match(token) else token

def parse(text):
    return [symbol(token) for token in tokens(text)]

def bb_read(prompt="Bb> "):
    readed = raw_input(prompt).strip()
    return parse(readed) if readed else None

def bb_stack(value): return [value]

def identity(s): return s

operator = defaultdict(lambda : identity)
operator['+'] = bb_plus
operator['-'] = bb_minus

def _eval(stack):
    if stack:
        if stack[len(stack) - 1] == '.':
            stack.pop() # pops .
            if not stack:
                print "Can't evaluate empty stack"
                return stack
            op = stack.pop()
            return operator[op](stack)
        else:
            return stack
    else:
        return []

def bb_eval(stack, new_stack, env=None):
    if new_stack:
        return _eval(stack + new_stack)
    else:
        return _eval(stack)

def bb_print(result):
    for i, r in enumerate(result):
        print i, r

def repl(prompt="Bb> "):
    stack = []
    while True:
        stack = bb_eval(stack, bb_read())
        bb_print(stack)

if __name__ == "__main__":
    # import doctest
    # doctest.testmod()

    repl()
