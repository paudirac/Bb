"""
Parser modules.

>>> list(parse("a b"))
['a', 'b']

>>> list(parse("1 2"))
[1, 2]
"""

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
    return (symbol(token) for token in tokens(text))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
