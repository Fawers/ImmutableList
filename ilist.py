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
        if self:
            return function(self.head) + self.tail.map(function)
        else:
            return self

    def filter(self, predicate):
        if self:
            if predicate(self.head):
                return self.head + self.tail.filter(predicate)
            else:
                return self.tail.filter(predicate)
        else:
            return self

    def take(self, howmany):
        if not self or howmany == 0:
            return nil()
        else:
            return self.head + self.tail.take(howmany-1)

    def take_while(self, predicate):
        if not self or not predicate(self.head):
            return nil()
        else:
            return self.head + self.tail.take_while(predicate)

    def drop(self, howmany):
        if not self or howmany == 0:
            return self
        else:
            return self.tail.drop(howmany-1)

    def drop_while(self, predicate):
        if not self or not predicate(self.head):
            return self
        else:
            return self.tail.drop_while(predicate)

    def reduce(self, function, acc=None):
        if not self:
            return acc
        elif acc is None:
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

    @staticmethod
    def from_values(*values):
        return ilist.from_list(values)

    def __repr__(self):
        return repr(self._head)+':'+repr(self._tail)

    def __nonzero__(self):
        return True

    # prepend
    def __radd__(self, other):
        return ilist(other, self)

    # append & concatenate
    def __add__(self, other):
        # append
        if not isinstance(other, ilist):
            if not self: # self is nil
                return other + self
            else:
                return self.head + (self.tail + other)
        # concatenate
        else:
            if not self.tail: # tail is nil
                return self.head + other
            else:
                return self.head + (self.tail + other)

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
