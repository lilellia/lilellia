# lilellia.iteration

## `class iteration.LazyIterable(items: Optional[Iterable[T]] = None)`

A class designed as a bridge between lazy generators (iterators) and more persistent iterables. LazyIterable objects do not store their items in memory (thus reducing memory footprint) but also maintaining the ability to be looped through more than once.

If *items* is provided and truthy, then the LazyIterable is created with those items as its contents. Otherwise, an empty LazyIterable is created. Raises `TypeError` if *items* is given and not iterable.

&nbsp;

### `LazyIterable` methods

LazyIterable objects provide the following public methods:

#### `LazyIterable.accumulate(accumulator: Callable[[T, T], T] = operator.add, *, initial: Optional[T] = None) -> LazyIterable[T]`

Return a new `LazyIterable` object whose contents are the accumulated sums (or accumulated results of other binary functions as specified by the optional `accumulator` argument).

If `accumulator` is supplied, it should be a function of two arguments. Elements of the LazyIterable may be any type that can be accepted as arguments to `accumulator`. (Example: with `operator.sum`, elements may be any addable type, such as `int`, `float`, `decimal.Decimal`, etc.)

Usually, the length of the output `LazyIterable` matches that of the input. However, if the keyword-only argument `initial` is supplied, the accumulation leads off with this value so that the output has one additional element.

Defers to `itertools.accumulate`, though the initial value is handled manually in Python versions prior to 3.8.

#### `LazyIterable.combinations(r: int, replacement: bool = False) -> LazyIterable[Tuple[T]]`

Return a new `LazyIterable` object whose contents are the length-`r` subsequences from the original LazyIterable.

- If `replacement` is False (the default):
  
    The length of the output is `n! / r! / (n - r)!` when `0 <= r <= n` or zero when `r > n`.

    Defers to `itertools.combinations`.

- If `replacement` is True:

    Allow individual elements from the input to be used more than once.

    The length of the output is `(n + r - 1)! / r! / (n - 1)!` when `n > 0`.

    Defers to `itertools.combinations_with_replacement`.

The yielded tuples are emitted in lexicographic ordering according to the order of the original. So, if the original LazyIterable is sorted, the combination tuples will also be produced in sorted order.

Elements are treated as unique based on their position, not on their value. So if the input elements are unique, the results will also be unique.

#### `LazyIterable.cycle(n: Optional[int] = None) -> LazyIterable[T]`

Return a new `LazyIterable` whose contents are the elements of the input, repeated when the input is exhausted. If `n` is None, repeat indefinitely.

```python
>>> li = LazyIterable('ABC')

# li.cycle(4) -> A B C A B C A B C A B C
# li.cycle()  -> A B C A B C A B C A B C A B C ...
```

Unlike `itertools.cycle`, this does not require significant auxiliary storage.

#### `LazyIterable.dropwhile(key: Callable[[T], bool] = bool) -> LazyIterable[T]`

Return a new `LazyIterable` that drops elements from the original as long as the key function is true; afterwards, returns every element. Note, the result does not produce any output until the key first becomes false, so it may have a lengthy start-up time.

Defers to `itertools.dropwhile` but renames the argument and allows it to be optional (defaulting to `bool`).

#### `LazyIterable.length(cap: Optional[int] = None) -> int`

Return the length of the iterable (the number of elements contained in it).

This method must count each of the elements in turn, which can be quite costly in terms of time—and, when the object is fed by an infinite generator, will not terminate. Thus, *cap* can be provided, which gives an upper bound on the returned size:

```python
>>> li = LazyIterable(range(10))
>>> li.length()
10
>>> li.length(cap=3)
3
>>> li.length(cap=1000)
10
```

In other words, if `li.length(cap=n)` returns `n`, then `li` contains *at least* `n` items.

#### `LazyIterable.update(items: Iterable[T])`

Set the contents of the LazyIterable to the given items.

**Note:** Because `foo is iter(foo)` for iterators, if an iterator is passed, iterating through the LazyIterable will consume that iterator:

```python
>>> gen = iter(range(10))
>>> li = LazyIterable(gen)
>>> tuple(li)
(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
>>> tuple(gen)
()
>>> tuple(li)
(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
```

Similarly, advancing the generator will also affect the values stored in the LazyIterable:

```python
>>> gen = iter(range(10))
>>> li = LazyIterable(gen)      # passed the values 0, 1, 2, ..., 8, 9
>>> next(gen, None)
0
>>> next(gen, None)
1
>>> tuple(li)                   # now only contains 2, 3, ..., 8, 9
(2, 3, 4, 5, 6, 7, 8, 9)
```

### `LazyIterable` magic methods

For these examples, assume that `li: LazyIterable[T]`, `other: Iterable[T]`, `value: T`.

`LazyIterable` implements the following operations:

- Addition (`__add__`):  
    `li + other`  
    Return a new `LazyIterable` object that iterates over the elements of `li`, then of `other`.

- Right Addition (`__radd__`):  
    `other + li`  
    Return a new `LazyIterable` object that iterates over the elements of `other`, then of `li`.

- In-place Addition (`__iadd__`):  
    `li += other`  
    Append the elements of `other` to the end of `li` in place.  
    Similar to `list.__iadd__` delegating to `list.extend`.

- Truthiness testing (`__bool__`):  
    `bool(li)`  
    Return `True` if `li` contains at least one item; `False` otherwise.

- Containment (`__contains__`):  
    `value in li`  
    Return True if `li` contains `value`; False otherwise.  
    **WARNING:** This iterates through `li` until it finds `value` (and returns `True`) or reaches the end of `li` (and returns `False`). If `li` is long and `value` appears only toward the end (or, indeed, not at all), this can be quite costly in terms of time (and won't terminate if `li` is fed by an infinite generator and `value` is not contained by it). In that case, it may be more advantageous to check on just a filtered region. For example, if `li` represents a list of prime numbers in ascending order and you wish to use `value in li` to check primality, this will not return if `value` is composite; instead, using `value in li.takewhile(lambda p: p <= value)` will mean that only the primes <= *value* are checked (which is sufficient in this case).

- Length (`__len__`):  
    `len(li)`  
    Returns the number of elements in `li`.  
    **WARNNG:** This must iterate through the entire iterable to count the items. In particular, it is of `O(n)` time, where `n` is the number of items in `li`. When `li` contains infinitely many items, this operation will not halt. See `LazyIterable.length` for an alternative.
