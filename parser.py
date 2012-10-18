"""
Parser modules.

>>> list(parse("a b"))
['a', 'b']

>>> list(parse("1 2"))
[1, 2]
"""

from collections import defaultdict

# : + ( x y -- x ) x y opplus

def make_binary(op, binary):
    def bb_binary(op, blast, last):
        return binary(blast, last)
    def bb_op(op, stack):
        last = stack.pop()
        blast = stack.pop()
        try:
            new_stack = stack + bb_stack(bb_binary(op, blast, last))
        except:
            print("Error evaluating '%(op)s' in: " \
                "%(blast)r %(last)r %(op)s" % locals())
            print("Restoring stack")
            new_stack = stack \
                + bb_stack(blast) + bb_stack(last) \
                + bb_stack(op)
        return new_stack
    return bb_op

def bb_pop(op, stack):
    stack.pop()
    return stack

def bb_end(op, stack):
    import sys
    sys.exit(0)

def tokens(text):
    """
    >>> tokens("a b")
    ['a', 'b']

    >>> tokens("1 2")
    ['1', '2']
    """
    return text.split(" ")

# TODO: this should be value, not symbol
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

def identity(op, stack):
    return stack + bb_stack(op)

operator = defaultdict(lambda : identity)
operator['+'] = make_binary('+', lambda bl, l: bl + l)
operator['-'] = make_binary('-', lambda bl, l: bl - l)
operator['*'] = make_binary('*', lambda bl, l: bl * l)
operator['/'] = make_binary('/', lambda bl, l: bl / l)
operator['pop'] = bb_pop
operator['end'] = bb_end

def _eval(stack):
    if stack:
        if stack[len(stack) - 1] == '.':
            stack.pop() # pops .
            if not stack:
                raise "Can't evaluate empty stack"
            op = stack.pop()
            return operator[op](op, stack)
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
    stack = ['end']
    bb_print(stack)
    while True:
        stack = bb_eval(stack, bb_read())
        bb_print(stack)

if __name__ == "__main__":
    # import doctest
    # doctest.testmod()

    repl()
