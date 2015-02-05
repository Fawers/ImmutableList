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
        return function(self.head) + self.tail.map(function)

    def filter(self, predicate):
        if predicate(self.head):
            return self.head + self.tail.filter(predicate)
        else:
            return self.tail.filter(predicate)

    def take(self, howmany):
        if howmany == 0:
            return nil()
        else:
            return self.head + self.tail.take(howmany-1)

    def take_while(self, predicate):
        if not predicate(self.head):
            return nil()
        else:
            return self.head + self.tail.take_while(predicate)

    def drop(self, howmany):
        if howmany == 0:
            return self
        else:
            return self.tail.drop(howmany-1)

    def drop_while(self, predicate):
        if not predicate(self.head):
            return self
        else:
            return self.tail.drop_while(predicate)

    def reduce(self, function, acc=None):
        if acc is None:
            return self.tail.reduce(function, self.head)
        else:
            return self.tail.reduce(function, function(self.head, acc))

    @property
    def to_list(self):
        if self:
            return [self.head] + self.tail.to_list
        else:
            return []

    @staticmethod
    def from_list(a_list):
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
