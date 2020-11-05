import collections
import itertools
import operator
import sys
from typing import Callable, Generic, Iterable, Optional, Tuple, TypeVar

T = TypeVar('T')
R = TypeVar('R')


class LazyIterable(Generic[T]):
    """ Create a lazily-evaluated iterable, bridging the gap between an iterable and an iterator.
    LazyIterable objects have higher overhead than generators, but far less than storing all of their
    items in memory (like a list). They also have the benefit of being iterable more than once. """

    def __init__(self, items: Optional[Iterable[T]] = None):
        self._items, self.reserve = None, None

        if items:
            self.update(items)

    def accumulate(
        self, accumulator: Callable[[T, T], T] = operator.add,
        *, initial: Optional[T] = None
    ) -> 'LazyIterable[T]':
        if sys.version_info >= (3, 8):
            items = itertools.accumulate(iter(self), accumulator, initial=initial)
        else:
            # manually handle initial value
            items = itertools.accumulate(
                itertools.chain((initial,), iter(self)),
                accumulator
            )

        return self.__class__(items)

    def append(self, item: T):
        """ Add the item to the end of this iterable, in place. """
        self += [item]

    def combinations(self, r: int, replacement: bool = False) -> 'LazyIterable[Tuple[T]]':
        """ Return length-r subsequences of elements from the LazyIterable. """
        func = itertools.combinations_with_replacement if replacement else itertools.combinations
        items = func(iter(self))

        return self.__class__(items)

    def consume(self, n: Optional[int] = None):
        """ Adcance the iterable n steps ahead (remove the first n items). If n is None, consume entirely. """
        s = iter(self)
        if n is None:
            collections.deque(s)
        else:
            next(itertools.islice(s, n, n), None)

        self.update(s)

    def cycle(self, n: Optional[int] = None) -> 'LazyIterable[T]':
        """ Return a new LazyIterable whose contents are the elements of this iterable, repeated n times. """
        def _gen():
            if n is None:
                # repeat indefinitely
                while True:
                    yield from self
            else:
                # repeat only n times
                for _ in range(n):
                    yield from self

        items = _gen()
        return self.__class__(items)

    def dropwhile(self, key: Callable[[T], bool] = bool) -> 'LazyIterable[T]':
        items = itertools.dropwhile(key, iter(self))
        return self.__class__(items)

    def groupby(self, key: Callable[[T], R]) -> 'LazyIterable[Tuple[R, LazyIterable[T]]]':
        """ Return a LazyIterable whose contents are consecutive groups and keys from the iterable. """
        items = (
            (k, self.__class__(g))
            for k, g in itertools.groupby(iter(self), key)
        )

        return self.__class__(items)

    def get_at(self, index: int, default: Optional[T] = None) -> T:
        """ Return the value at position #index, or default. """
        s = itertools.islice(iter(self), index, None)
        return next(s, default)

    def get_slice(self, *args: int) -> 'LazyIterable[T]':
        """ Return items over a range. """
        items = itertools.islice(iter(self), *args)
        return self.__class__(items)

    def head(self, n: int) -> 'LazyIterable[T]':
        """ Return the first n items of the iterable """
        return self.get_slice(n)

    def insert(self, index: int, item: T):
        """ Insert the item at the given index. """
        items = self.get_slice(index) + [item] + self.get_slice(index, None)
        self.update(items)

    def length(self, cap: Optional[int] = None) -> int:
        if cap is None:
            return len(self)

        i = iter(self)
        for k in range(cap):
            try:
                next(i)
            except StopIteration:
                return k
        return cap

    def permutations(self, r: Optional[int] = None) -> 'LazyIterable[Tuple[T]]':
        """ Return length-r permutations """
        items = itertools.permutations(iter(self))
        return self.__class__(items)

    def prepend(self, item: T):
        """ Add the element to the start of this iterable """
        items = [item] + self
        self.update(items)

    def tail(self, n: int) -> 'LazyIterable[T]':
        """ Return the last n items """
        items = collections.deque(self, maxlen=n)
        return self.__class__(items)

    def takewhile(self, key: Callable[[T], bool] = bool) -> 'LazyIterable[T]':
        """ Return elements as long as key(x) is true. """
        items = itertools.takewhile(key, iter(self))
        return self.__class__(items)

    def update(self, items: Iterable[T]):
        """ Set the item pointer to this new iterable of items """
        self._items, self._reserve = itertools.tee(items, 2)

    def __add__(self, other: Iterable[T]) -> 'LazyIterable[T]':
        """ Return a new LazyIterable whose contents are the chain of left and right """
        items = itertools.chain(iter(self), other)
        return self.__class__(items)

    def __radd__(self, other: Iterable[T]) -> 'LazyIterable[T]':
        items = itertools.chain(other, iter(self))
        return self.__class__(items)

    def __iadd__(self, other: Iterable[T]) -> 'LazyIterable[T]':
        """ Extend this LazyIterable with the elements from other. """
        items = itertools.chain(iter(self), other)
        self.update(items)
        return self

    def __len__(self) -> int:
        i = iter(self)
        for k in itertools.count():
            try:
                next(i)
            except StopIteration:
                return k

    def __iter__(self):
        i = iter(self._items)
        self.update(self._reserve)

        return i

    def __contains__(self, value: T) -> bool:
        """ Return True if value is in this LazyIterable; False otherwise. """
        return value in iter(self)

    def __bool__(self) -> bool:
        """ Return True if nonempty. """
        return self.length(cap=1) == 1
