from singleton import singleton

class ilist(object):
    def __init__(self, head, tail=None):
        self._head = head
        if tail:
            self._tail = tail
        else:
            self._tail = None if isinstance(self, nil) else nil()

    @property
    def head(self):
        return self._head

    @property
    def tail(self):
        return self._tail

    def map(self, function):
        """\
Maps the given function to the entire ilist. Essentially, map applies the
given function to the list head, and then call map(function) in the ilist
tail returning, then, a new ilist."""
        return function(self.head) + self.tail.map(function)

    def filter(self, predicate):
        """\
Filters the list with the given predicate. Needless to say, filter creates
a new ilist with only the elements for which the predicate evaluates to \
True."""
        if predicate(self.head):
            # if the predicate for head evals to True, then head should be
            # included in the new list.
            return self.head + self.tail.filter(predicate)
        else: # otherwise, skip it.
            return self.tail.filter(predicate)

    def take(self, howmany):
        """\
take works just like slicing in core python lists: A.take(3) <=> B[:3]
where   B = [1,2,3,4,5]
        A = 1:2:3:4:5:nil"""
        if howmany == 0:
            return nil()
        else:
            return self.head + self.tail.take(howmany-1)

    def take_while(self, predicate):
        """\
take_while works similarly to filter, except that take_while will stop
when the predicate applied to the current element evaluates to False. So,
A.take_while(odd) returns B where
    odd = (x) => x % 2 != 0
    A   = 1:3:5:6:7:9:nil
    B   = 1:3:5:nil"""
        if not predicate(self.head):
            return nil()
        else:
            return self.head + self.tail.take_while(predicate)

    def drop(self, howmany):
        """\
Drop, like take, take, works like slicing in core Python lists.
A.drop(2) <=> B[2:] where
    A = 1:2:3:nil
    B = [1,2,3]"""
        if howmany == 0:
            return self
        else:
            return self.tail.drop(howmany-1)

    def drop_while(self, predicate):
        """\
drop_while will drop elements while the predicate evaluates to True.
A.drop_while(even) returns B where
    even = (x) => x % 2 == 0
    A    = 2:4:6:1:3:5:nil
    B    = 2:4:6:nil"""
        if not predicate(self.head):
            return self
        else:
            return self.tail.drop_while(predicate)

    def reduce(self, function, acc=None):
        """\
Reduce takes a binary function and applies to the whole list,
reducing it to a single value. E.g., A.reduce(add) = 10 where
    add = (a,b) => a + b
    A   = 1:2:3:4:nil"""
        if acc is None:
            return self.tail.reduce(function, self.head)
        else:
            return self.tail.reduce(function, function(self.head, acc))

    @property
    def to_list(self):
        """Returns the current ilist object as a core Python list."""
        if self:
            return [self.head] + self.tail.to_list
        else:
            return []

    @staticmethod
    def from_list(a_list):
        """Returns an ilist from a core Python list."""
        if not a_list:
            return nil()
        else:
            return a_list[0] + ilist.from_list(a_list[1:])

    def __repr__(self):
        return repr(self._head)+':'+repr(self._tail)

    def __nonzero__(self):
        return True

    # prepend
    def __radd__(self, other):
        return ilist(other, self)

    # append & concatenate
    def __add__(self, other):
        return self.head + (self.tail + other)

    def __getitem__(self, index):
        l = len(self)
        while index < 0:
            index += l
        return self.drop(index).head

    @property
    def length(self):
        return len(self)
    def __len__(self):
        return 1 + len(self.tail)

class nil(ilist):
    __metaclass__ = singleton

    def __init__(self):
        ilist.__init__(self, None)

    def __repr__(self):
        return 'nil'

    def __nonzero__(self):
        return False

    @property
    def head(self):
        raise ValueError("head of nil")

    def map(self, function):
        return self

    def filter(self, predicate):
        return self

    def take(self, howmany):
        return self

    def take_while(self, predicate):
        return self

    def drop(self, howmany):
        return self

    def drop_while(self, predicate):
        return self

    def reduce(self, function, acc):
        return acc

    def __add__(self, other):
        if not isinstance(other, ilist):
            return ilist(other)
        else:
            return other

    def __eq__(self, other):
        return other is nil()

    def __getitem__(self, index):
        raise ValueError("nil[{0}] <=> [][{0}]".format(index))

    def __len__(self):
        return 0

a = ilist.from_list(range(10))
