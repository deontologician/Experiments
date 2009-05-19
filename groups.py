"""Experimental work with groups (experimental for me)

A Group is an algebraic structure {S,*} that consists of a nonempty
set S, and a binary operation, *, from S*S -> S

The set and operation must satisfy a few properties:

i.   * must be associative
ii.  there must be an identity element e in S, such that for any x in S, 
     x * e = x and e * x = x
iii. for every x in S, there must be an inverse x^-1 in S such that
     x * x^-1 = e

Additionally, if * is commutative, then the group is called Abelian

Throughout this module, the sets are always sets of strings, and the
operations take a tuple of two strings and return a string.
"""

from itertools import product

class AlgStruct(object):
    "Represents an algebraic structure consisting of a set and an operation"
    def __init__(self, gset, funmap, symbol='*'):
        """gset = the set for the algebraic structure
 
        funmap = dict of tuples from cartesian product of gset to
        members of gset

        symbol = a symbol representing the operation"""
        
        #We must check whether the set and operation satisfy some
        #basic properties
        
        #Check whether the set is non-empty
        if len(gset) == 0:
            raise ValueError("Set must be non-empty")
        #check whether the set and operation have closure 
        if not is_closure(gset, lambda a,b:funmap[(a,b)]):
            raise ValueError("Set and operation are not closed")
        self.S = gset
        self._funmap = funmap
        self.symbol = symbol

    def __repr__(self):
        "Returns a representation of the Algebraic Structure"
        return "{" + repr(self.S) + ", " + self.symbol + "}"

    def op(self,x,y):
        "Carries out the operation by returning the inputs"
        return self._funmap[(x,y)]


def define_funmap(gset):
    "Gets user input to define a function map from a given set of symbols"
    funmap = {}
    for perm in product(gset,gset):
        funmap[perm] = raw_input("%s * %s = " % perm)
    return funmap

def define_elements():
    "Gets user input to define a set of symbols"
    gset = set()
    while True:
        inn = raw_input("next element: ")
        if inn == "":
            break
        else: 
            gset.add(inn)
    return gset

def make_AlgStruct():
    "Makes an algebraic structure using user input"
    gset = define_elements()
    funmap = define_funmap(gset)
    g = AlgStruct(gset, funmap)
    print g
    print funtable(g)
    return g

def is_closure(gset, op):
    """Tests whether a set is closed under an operation"""
    for a,b in product(gset,gset):
        try:
            if op(a, b) not in gset:
                raise ValueError
        except:
            return False
    return True
    
def is_associative((gset,f),p=False):
    """Tests whether an algebraic structure is associative. Optionally
    prints the first non-associative triple if p is True"""

    for x,y,z in product(gset, gset, gset):
        if f(f(x,y), z) != f(x, f(y,z)):
            break
    else:
        return True
    if p:
        print (x, (y, z)), "!=", ((x, y), z)
    return False #some triple caused a break

def funtable(gset, op, symbol="*"):
    """Returns a string representing a full Cayley table for a
    function over a set.  Optional argument symbol is the symbol used
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
            retval += op(i,j) + "\t"
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

def systematic_assoc_test(gset):
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
    positives = []
    for i, fun in enumerate(fun_iter):
        if is_associative((gset,fun)):
            positives.append(i)
    return positives

def main():
    import timeit
    timeit.Timer('systematic_assoc_test(set([1,2,3]))',
                 'gc.enable()').timeit()

if __name__ == '__main__':
    main()
