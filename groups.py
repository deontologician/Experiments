"""Experimental work with groups (experimental for me)

A Group is an algebraic structure {S,*} that consists of a nonempty
set S, and a binary operation, *, from S*S -> S

The set and operation must satisfy a few properties:

i.   * must be associative
ii.  there must be an identity element e in S, such that for any x in S, 
     x * e = x
iii. for every x in S, there must be an inverse x^-1 in S such that
     x * x^-1 = e

Additionally, if * is commutative, then the group is called Abelian

"""

from itertools import product

class Group(object):
    "Represents a group"
    def __init__(self, gset, funmap, symbol='*'):
        """gset = the set for the group 
        funmap = map of tuples from
         cartesian product of gset to members of gset,
        symbol = a symbol representing the operation"""
        self.S = gset
        self._funmap = funmap
        self.symbol = symbol

    def __len__(self):
        "Returns size of set S"
        return len(self.S)

    def __repr__(self):
        "Returns a representation of the Group"
        return "Group{"+repr(self.S) + "," + self.symbol+ "}"

    def op(self,x,y):
        try:
            retval = self._funmap[(x,y)]
        except:
            raise ValueError('Operation not defined for values')
        return retval

def define_funmap(gset):
    "Gets user input to define a function map from a given gset"
    funmap = {}
    for perm in product(gset,gset):
        funmap[perm] = raw_input("%s * %s = " % perm)
    return funmap

def define_elements():
    "Gets user input to define set"
    gset = set()
    while True:
        inn = raw_input("next element: ")
        if inn == "":
            break
        else: 
            gset.add(inn)
    return gset
    
def test_assoc(G,p=False):
    """Tests whether a potential group is associative. Optionally
    prints the first non-associative triple if p is True"""
    f = G.op # for clarity
    for x,y,z in product(G.S, G.S, G.S):#triple cartesian product
        if f(f(x,y), z) != f(x, f(y,z)):
            break
    else:# if break is not encountered i.e. always associative
        return True
    if p:
        print (x, (y, z)), "!=", ((x, y), z)
    return False #some triple caused a break

def funtable(grp):
    "Print out a full Cayley table for a group's operation'"
    print grp.symbol, "\t",
    for i in grp.S:
        print i, "\t",
    print ""
    for i in grp.S:
        print i, "\t",
        for j in grp.S:
            print grp.op(i,j), "\t",
        print ""

def fun_generator(gset):
    """Generates funmaps of successive functions from a given set of
    input symbols

    Warning: The total number of functions generated is astronomical,
    if s is the size of the set, then there are s**(s**2) possible
    functions for this set.

    For example: for a set of size 3, there are 19,683 functions, for a
    set of size 4 there are 4,294,967,296 functions"""

    power = len(gset)**2
    for f in product(*((gset,)*power)):
        funmap = {}
        for i,p in enumerate(product(gset, gset)):
            funmap[p] = f[i]
        yield funmap
           
        

def make_group():
    "Makes a group using user input"
    gset = define_elements()
    funmap = define_funmap(gset)
    g = Group(gset, funmap)
    print g
    print funtable(g)
    return g
    

    
