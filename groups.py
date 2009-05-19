"""Experimental work with groups (experimental for me)

A Group is Groupoid {S,*} that consists of a nonempty
set S, and a binary operation, *, from S*S -> S

The set and operation must satisfy a few properties:

i.   * must be associative
ii.  there must be an identity element e in S, such that for any x in S, 
     x * e = x and e * x = x
iii. for every x in S, there must be an inverse x^-1 in S such that
     x * x^-1 = e

Additionally, if * is commutative, then the group is called Abelian

Throughout this module, the sets are always sets of strings, and the
operations take a tuple of two strings and return a string."""

from itertools import product

def define_funmap(gset):
    "Gets user input to define a function map from a given set of symbols"
    funmap = {}
    for perm in product(gset,gset):
        funmap[perm] = raw_input("%s * %s = " % perm)
    return funmap

def define_elements():
    "Gets user input to define a set of symbols"
    gset = []
    while True:
        inn = raw_input("next element: ")
        if inn == "" or inn in gset:
            break
        else: 
            gset.append(inn)
    return gset

def make_Groupoid():
    "Makes an groupoid using user input"
    gset = define_elements()
    funmap = define_funmap(gset)
    g = (gset, funmap)
    print g
    print funtable(g)
    return g

def is_closed((gset, f)):
    """Tests whether a set is closed under an operation"""
    for a,b in product(gset,gset):
        try:
            if f(a, b) not in gset:
                raise Exception
        except:#a keyerror may be raised by the function
            return False
    return True
    
def is_associative((gset,f)):
    """Tests whether a groupoid is associative."""

    for x,y,z in product(gset, gset, gset):
        if f(f(x,y), z) != f(x, f(y,z)):
            return False
    return True

def is_commutative((gset,f)):
    """Tests whether a groupoid is associative"""
    for x,y in product(gset,gset):
        if f(x,y) != f(y,x):
            return False
    return True

def is_idempotent((gset,f)):
    """Tests whether a groupoid is idempotent"""
    for x in gset:
        if f(x,x) != x:
            return False
    return True
            

def funtable((gset, f), symbol="*"):
    """Returns a string representing a full Cayley table for a
    groupoid.  Optional argument symbol is the symbol used
    to represent the function. This is not done particularly
    efficiently, but if your table is huge enough for this to matter,
    the rest of this module will be fairly useless to you."""

    retval = symbol + "\t"
    for i in gset:
        retval += i + "\t"
    retval += "\n"
    for i in gset:
        retval += i + "\t"
        for j in gset:
            retval += f(i,j) + "\t"
        retval += "\n"
    return retval + "\n"

def fun_generator(gset):
    """Generates successive binary functions from a given set of input
    symbols.

    Warning: The total number of binary functions generated is
    astronomical.  If s is the size of the set, then there are
    s**(s**2) possible functions for the set.

    For example: for a set of size 3, there are 19,683 functions, for a
    set of size 4 there are 4,294,967,296 functions"""

    power = len(gset)**2
    for f in product(*((gset,)*power)):
        funmap = {}
        for i,p in enumerate(product(gset, gset)):
            funmap[p] = f[i]
        yield (lambda x,y: funmap[(x,y)])


def systematic_test(gset):
    """Tests each possible function over a set for associativity,
    returns a list of the numbers of the positive functions (from
    which the functions can be regenerated given the set). This test
    is sufficiently general that it need only be executed once ever
    for a given set size, since the results extend to all sets the
    same size as the input set. Unfortunately, while this is true, it
    is not advised that anyone use this function on a set larger than
    4 elements. (See the docstring for fun_generator)

    When attempting to run this on my laptop, a set with 3 elements
    took 301 milliseconds to execute. This means a set with 4 elements
    should run in about 18 hours and a set with 5 elements should run in 
    about 144,516 years"""
    
    fun_iter = fun_generator(gset)

    a = [] #associative functions
    c = [] #commutative functions
    i = [] #idempotent functions

    for index, f in enumerate(fun_iter):
        if is_associative((gset, f)):
            a.append(index)
        if is_commutative((gset, f)):
            c.append(index)
        if is_idempotent((gset, f)):
            i.append(index)
    return (a, c, i)

def str_num(n, gset, width=0):
    """Returns the nth string when the strings from gset are
    lexicographically ordered. Optionally, the minimum width can be
    specified."""
    radix = len(gset)
    
    
