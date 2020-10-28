# lilellia.lmath

Much of this module is a combination/wrapper around Python's stdlib `math` and `cmath` modules. However, the following functions are not copied over:

- Any `math.*` function with a `cmath` counterpart.
- `math.copysign`
- `math.fabs`
- `math.fmod`
- `math.frexp`
- `math.fsum`
- `math.is*` (`isclose`, `isfinite`, `isinf`, `isnan`) and their `cmath` counterparts
- `math.ldexp`
- `math.nextafter` (3.9+)
- `math.prod` (used instead as `lilellia.utils.product`)
- `math.remainder`
- `math.trunc`
- `math.ulp` (3.9+)
- `math.hypot`
- `math.degrees`
- `math.radians`
- `math.log1p` and `math.log2`, though their behavior is absorbed into `lmath.log`
- `math.log10` and `cmath.log10`, though their behavior is absorbed into `lmath.log`
- `math.pow`
- `math.lgamma`

In addition, the following functions are renamed:

- `math.comb` (3.8+) → `lmath.choose`
- `math.perm` (3.8+) → `lmath.permutations`
- `cmath.rect` → `lmath.cartesian`
- `cmath.acos` → `lmath.arccos`
- `cmath.asin` → `lmath.arcsin`
- `cmath.atan` → `lmath.arctan` (Though `lmath.arctan` acts as both `cmath.arctan` and `math.atan2`.)
- `math.dist` (3.8+) → `lmath.distance` (Though `lmath.distance` also has slightly different behavior: see below.)

The following functions have different behavior:

- GENERAL:
  - `lmath` functions which can reasonably expect complex numbers are affected by `lmath.realcast`, meaning that they will output real numbers when possible. Their `cmath` counterparts always output a complex number.
  - `lmath` functions which deal with angles (as either inputs or outputs) are affected by `lmath.accept_angle` or `lmath.output_angle`, meaning they will parse their input as degrees or radians according to `lmath.ANGLE_MODE`.

- `cmath.phase` vs. `lmath.phase`: The former outputs angles on [-π, π]; the latter outputs angles on [0, 2π).
- `math.atan2` vs. `lmath.arctan(z: Real, a: Real)`: The former outputs angles on [-π, π]; the latter outputs angles on [0, 2π).
- `math.dist` vs. `lmath.distance`: The former requires the two points to have the same dimension; the latter allows points with mismatched dimensions by right-padding the shorter vector with zeros.
- `cmath.log` vs. `lmath.log`: The latter delegates to `math.log1p`, `math.log2`, `cmath.log10`, or `cmath.log` depending on the arguments. This is in an effort to maintain precision while also maintaining generality.

There are a few new functions:

- `lmath.realcast`
- `lmath.ANGLE_MODE` (a string) and `lmath.force_angle_mode` (a function/context manager)
- `lmath.accept_angle` and `lmath.output_angle`, which use `ANGLE_MODE` to accept/output angles of the desired type (degrees vs. radians)
- `lmath.roots_of_unity`
- `lmath.normdist_pdf` and `lmath.normdist_cdf`, which give the PDF and CDF for the normal distribution

## Constants

Note that, unlike `math` and `cmath`, these names are capitalized.

### `lmath.PI`

The mathematical constant π = 3.14159..., to available precision.

### `lmath.TAU`

The mathematical constant τ = 6.28318..., to available precision. Tau is a circle constant defined as the ratio of a circle's diameter to its radius, making it equal to 2π.

### `lmath.E`

The mathematical constant e = 2.71828..., to available precision.

### `lmath.INF`

A floating-point positive infinity. Equivalent to `float('inf')`. For -∞, use `-lmath.INF`.

### `lmath.NAN`

A floating-point "not a number" (NaN) value. Equivalent to `float('nan')`.

### `lmath.INFI` and `lmath.INFJ`

A complex number with zero real part and positive infinity imaginary part. Equivalent to `complex(0.0, float('inf'))`.

### `lmath.NANI` and `lmath.NANJ`

A complex number with zero real part and NaN imaginary part. Equivalent to `complex(0.0, float('nan'))`.

&nbsp;

## Number-theoretic and representation functions

### `lmath.ceil(x: Real) -> Integral`

Return the ceiling of *x*, the smallest integer greater than or greater than *x*. If *x* is not a `float`, this delegates to `x.__ceil__()`, which should return an `Integral` value.

Defers to `math.ceil`.

### `lmath.choose(n: int, k: int) -> int`

Return the number of ways to choose k items from n without repetition and without order. This is also called the binomial coefficient because it is the coefficient of the kth term in the expansion of `(1 + x) ** n`.

Evaluates to `n! / (k! * (n-k)!)` when `0 <= k <= n` and to zero when `k > n`.

Raises `TypeError` is either of the arguments is not an integer; raises `ValueError` if either of the arguments is negative.

Defers to `math.comb` in Python versions 3.8+.

### `lmath.factorial(x: Union[int, float]) -> int`

Return *x!* when *x* is an integer (or an integral float).

Raises `ValueError` if *x* is negative or not an integer. Python 3.9+ deprecates `math.factorial` with floats with an integral value (e.g., `x = 5.0`). This distinction is not maintained here, and `lmath.factorial(5.0)` will happily return 120.

Defers to `math.factorial`.

### `lmath.floor(x: Real) -> Integral`

Return the floor of *x*, the largest ineger less than *x*. If *x* is not a float, this delegates to `x.__floor__()`, which should return an `Integral` value.

Defers to `math.floor`.

### `lmath.gcd(*values: int) -> int`

Return the greatest common divisor of the specified integer arguments. If any of the arguments is nonzero, then the returned value is the largest positive integer which is a divisor of all arguments. If all arguments are zero, then the returned value is zero. `lmath.gcd()` without arguments returns zero.

Raises `TypeError` is any of the arguments is a `float`.

Defers to `math.gcd` with its behavior in Python 3.9+.

### `lmath.lcm(*values: int) -> int`

Return the least common multiple of the specified integer arguments. If all arguments are nonzero, then the returned value is the smallest positive integer which is a multiple of all arguments. If any of the arguments is zero, then the returned value is 0. `lmath.lcm()` with no arguments returns 1.

Defers to `math.lcm` in Python versions 3.9+.

### `lmath.modf(x: Real) -> Tuple[float, int]`

Return the fractional and integer parts of *x* in a `namedtuple` with names `(fpart, ipart)`. Both results carry the sign of *x*; the fractional part is a `float`, the integer part is an `int`.

Defers to `math.modf` (but makes the integer part an `int`).

```python
>>> lmath.modf(3.2)
ModF(fpart=0.2, ipart=3)

>>> lmath.modf(3.2)[0]
0.2

>>> lmath.modf(3.2).fpart
0.2

>>> lmath.modf(-3.2)
ModF(fpart=-0.2, ipart=-3)
```

### `lmath.permutations(n: int, k: Optional[int] = None) -> int`

Return the number of ways to choose *k* items from *n* without repetition but with order.

Evaluates to `n! / (n - k)!` when `0 <= k <= n` and to zero when `k > n`.

If *k* is `None`, then it defaults to *n* and the function returns *n!*.

Raises `TypeError` if either of the arguments is not an integer; raises `ValueError` if either of the arguments is negative.

Defers to `math.perm` in Python versions 3.8+.

## Complex representation functions

### `lmath.realcast(func: Callable[..., Complex]) -> Callable[..., Union[Real, Complex]]`

A decorator which casts the output of a function as a real number when the imaginary part is sufficiently small. This allows a function to output real numbers when its result is real but defer to a complex result when necessary.

As an example, consider these functions:

```python
def sqrt_real(x: Real) -> Real:
    return math.sqrt(x)

def sqrt_complex(z: Complex) -> Complex:
    return cmath.sqrt(z)

@lmath.realcast
def sqrt_cast(z: Complex) -> Union[Real, Complex]"
    return cmath.sqrt(z)


>>> sqrt_real(4)
2.0
>>> sqrt_complex(4)
(2+0j)
>>> sqrt_cast(4)
2.0

>>> sqrt_real(-4)
ValueError: math domain error
>>> sqrt_complex(-4)
2j
>>> sqrt_cast(-4)
2j
```

This decorator allows `sqrt_cast` to always have the "power" of `cmath.sqrt` but without the inconvenience of always gettign complex numbers out.

### `lmath.phase(z: Complex) -> float`

Return the phase (a.k.a. the argument) of z, as a float.

Defers to `cmath.phase`, except the result of `lmath.phase` lies on [0, 2π) instead of [-π, π].

Even on systems with support for signed zeros, `lmath.phase(complex(1.0, -0.0)) == 0.0`.

### `lmath.polar(z: Complex) -> Tuple[float, float]`

Return the representation of *z* in polar coordinates. Returns a namedtuple pair `Polar(modulus, phase)`, where *modulus* is the modulus (absolute value) of *z* and *phase* is its phase. As with `lmath.phase(z)`, this phase is reported on [0, 2π).

### `lmath.cartesian(modulus: float, phase: float, *, angle_mode: str = 'radians') -> Complex`

Return the complex number with polar coordinates *(modulus, phase)*. This is equivalent to `complex(modulus*cos(phase), modulus*sin(phase))`.

## Trigonometric utilities

### `lmath.accept_angle(func: Callable[[Real], Any]) -> Callable[[Real], Any]`

A decorator which allows for the wrapped function to utilize `lmath.ANGLE_MODE` to parse its input angle (as degrees or radians). Currently, only one-argument callables are supported.

The wrapped function's logic should expect the angle to be in radians:

```python
@lmath.realcast
@lmath.accept_angle
def sin(z):
    return cmath.sin(z)

>>> lmath.ANGLE_MODE = "RADIANS"
>>> sin(90)
0.8939966636005579

>>> lmath.ANGLE_MODE = "DEGREES"
>>> sin(90)
1.0
```

### `lmath.ANGLE_MODE: str = "RADIANS"`

A string that determines which angle mode is used for any trigonometric calculation. It should be one of `"RADIANS"` and `"DEGREES"` (though capitalization is ignored). It can also be temporarily set using `lmath.force_angle_mode`.

### `lmath.force_angle_mode(temp_mode: str)`

A context manager that locally overrides/forces the angle mode to the given mode.

```python
print(lmath.ANGLE_MODE, lmath.sin(90))

with lmath.force_angle_mode("DEGREES"):
    print(lmath.ANGLE_MODE, lmath.sin(90))

print(lmath.ANGLE_MODE, lmath.sin(90))
```

prints

```text
RADIANS 0.8939966636005579
DEGREES 1.0
RADIANS 0.8939966636005579
```

Also aliased as `lmath.fam` for brevity.

### `lmath.output_angle(func: Callable[..., Real]) -> Callable[..., Real]`

A decorator which allows for the wrapped function to utilize `lmath.ANGLE_MODE` to parse its output angle (as degrees or radians). Currently, only functions which return a single number as an output are supported.

The wrapped function's logic should return the result in radians:

```python
@lmath.realcast
@lmath.output_angle
def arcsin(z):
    return cmath.asin(z)


>>> lmath.ANGLE_MODE = "RADIANS"
>>> arcsin(1)
1.5707963267948966

>>> lmath.ANGLE_MODE = "DEGREES"
>>> arcsin(1)
90.0
```

## Trigonometric functions

### `lmath.arccos(z: Complex) -> Union[Real, Complex]`

Return the arc cosine of *z*. The result is real when *-1 <= z <= 1* and complex otherwise. In the complex case, there are two branch cuts: One extends right from 1 along the real axis to ∞, continuous from below. The other extends left from -1 along the real axis to -∞, continuous from above.

Defers to `cmath.acos` but is affected by `lmath.realcast` (outputs real values when possible) and `lmath.output_angle` (outputs angles according to `lmath.ANGLE_MODE`).

### `lmath.arcsin(z: Complex) -> Union[Real, Complex]`

Return the arc sine of *x*. The result is real when *-1 <= z <= 1* and complex otherwise. In the complex case, this has the same branch cuts as arccos().

Defers to `cmath.acos` but is affected by `lmath.realcast` (outputs real values when possible) and `lmath.output_angle` (outputs angles according to `lmath.ANGLE_MODE`).

### `lmath.arctan(z: Complex, a: Optional[Real] = None) -> Union[Real, Complex]`

This function has two behaviors depending on the value of `a`:

1. When `a is None`: i.e., when this is called as `arctan(z)`: Return the arctangent of *z*. The result is real when *z* is real and complex otherwise. In the complex case, there are two branch cuts: One extends from 1j along the imaginary axis to ∞j, continuous from the right. The other extends from -1j along the imaginary axis to -∞j, continuous from the left.

    Here, the function defers to `cmath.atan` but is affected by `lmath.realcast` (outputs real values when possible) and `lmath.output_angle` (outputs angles according to `lmath.ANGLE_MODE`).

2. When `a is not None`: Return the angle θ in the quadrant determined by the point (a, z) satisfying tan(θ) = z/a.  In this way, it resembles `math.atan2(z, a)`, though the result is between 0 and 2π. The vetor in the plane from the origin to the point (a, z) makes this angle with the positive X axis. The point of this mode of the function is that the signs of both inputs are known, so it can compute the correct quadrant for the angle. For example, `arctan(1)` and `arctan(1, 1)` are both `pi/4`, but `arctan(-1, -1)` is `5*pi/4`. Affected by `lmath.output_angle`, this function outputs angles according to `lmath.ANGLE_MODE`.

    Raises `ValueError` if *a* is not None and either argument is nonreal. Raises `ZeroDivisionError` if *a* is zero.

### `lmath.cos(z: Complex) -> Union[Real, Complex]`

Return the cosine of *z*. The result is real if *z* is real and complex otherwise.

Defers to `cmath.cos` but is affected by `lmath.realcast` (outputs real values when possible) and `lmath.accept_angle` (interprets angles according to `lmath.ANGLE_MODE`).

### `lmath.sin(z: Complex) -> Union[Real, Complex]`

Return the sin of *z*. The result is real if *z* is real and complex otherwise.

Defers to `cmath.sin` but is affected by `lmath.realcast` (outputs real values when possible) and `lmath.accept_angle` (interprets angles according to `lmath.ANGLE_MODE`).

### `lmath.tan(z: Complex) -> Union[Real, Complex]`

Return the tangent of *z*. The result is real if *z* is real and complex otherwise.

Defers to `cmath.tan` but is affected by `lmath.realcast` (outputs real values when possible) and `lmath.accept_angle` (interprets angles according to `lmath.ANGLE_MODE`).

## Hyperbolic trigonometric functions

### `lmath.arccosh(z: Complex) -> Union[Real, Complex]`

Return the inverse hyperbolic cosine of *z*. The result is real when possible. There is one branch cut, extending left from 1 along the real axis to -∞, continuous from above.

Defers to `cmath.acosh` but is affected by `lmath.realcast` (outputs real values when possible) and `lmath.output_angle` (outputs angles according to `lmath.ANGLE_MODE`).

### `lmath.arcsinh(z: Complex) -> Union[Real, Complex]`

Return the inverse hyperbolic sine of *z*. The result is real when possible. There are two branch cuts: One extends from 1j along the imaginary axis to ∞j, continuous from the right. The other extends from -1j along the imaginary axis to -∞j, continuous from the left.

Defers to `cmath.asinh` but is affected by `lmath.realcast` (outputs real values when possible) and `lmath.output_angle` (outputs angles according to `lmath.ANGLE_MODE`).

### `lmath.arctanh(z: Complex) -> Union[Real, Complex]`

Return the inverse hyperbolic tangent of *z*. The result is real when possible. There are two branch cuts: One extends from 1 along the real axis to ∞, continuous from below. The other extends from -1 along the real axis to -∞, continuous from above.

Defers to `cmath.atanh` but is affected by `lmath.realcast` (outputs real values when possible) and `lmath.output_angle` (outputs angles according to `lmath.ANGLE_MODE`).

### `lmath.cosh(z: Complex) -> Union[Real, Complex]`

Return the hyperbolic cosine of *z*. The result is real when possible.

Defers to `cmath.cosh` but is affected by `lmath.realcast` (outputs real values when possible) and `lmath.accept_angle` (interprets angles according to `lmath.ANGLE_MODE`).

### `lmath.sinh(z: Complex) -> Union[Real, Complex]`

Return the hyperbolic sin of *z*. The result is real when possible.

Defers to `cmath.sinh` but is affected by `lmath.realcast` (outputs real values when possible) and `lmath.accept_angle` (interprets angles according to `lmath.ANGLE_MODE`).

### `lmath.tanh(z: Complex) -> Union[Real, Complex]`

Return the hyperbolic tangent of *z*. The result is real when possible.

Defers to `cmath.tanh` but is affected by `lmath.realcast` (outputs real values when possible) and `lmath.accept_angle` (interprets angles according to `lmath.ANGLE_MODE`).

### `lmath.distance(p: Iterable[Real], q: Iterable[Real]) -> float`

Return the Euclidean distance between two points in R² space, each given as a sequence (Iterable) of coordinates. If the points have unequal dimension, then the shorter is right-padded with zeros. Example: `distance((1, 2, 3), (4, 5))` will interpret the points as `(1, 2, 3)` and `(4, 5, 0)`.

Its stdlib counterpart (`math.dist` (3.8+)) requires the points to have the same dimension.

## Power and logarithmic functions

### `lmath.exp(z: Complex) -> Union[Real, Complex]`

Return *e* to the power *z*, where *e* is the base of the natural logarithms.

Defers to `cmath.exp` but is affected by `lmath.realcast` (outputs real values when possible).

### `lmath.expm1(x: Real) -> Real`

Return *e* to the power *x*, minus 1. Here, *e* is the base of the natural logarithms. For small floats *x*, the subtraction in `exp(x) - 1` can result in a significant loss of precision; this function provides a way to compute this quantity to full precision.

Because this defers to `math.expm1`, this function cannot accept complex arguments.

### `lmath.log(z: Complex, base: Optional[Complex] = None) -> Union[Real, Complex]`

Returns the logarithm of x to the given base. If the base is not specified, returns the natural logarithm of x. There is one branch cut, from 0 along the negative real axis to -∞, continuous from above.

This function defers to one of several functions as necessary:

- If *z* is real and *base* is None (natural log), then this function defers to `math.log1p(z-1)`, which maintains precision for *z* close to 1.
- If *z* is real and *base = 2*, then this function defers to `math.log2`, which is usually more accurate than `math.log(..., 2)`.
- If *base = 10*, then this function defers to `cmath.log10`, which is usually more accurate than `cmath.log(z, 10)`.
- Otherwise, this function defers to `cmath.log`.

Regardless, this function is affected by `lmath.realcast`, so its output will be real when possible.

### `roots_of_unity(n: int) -> Tuple[Complex]`

Return the *n*th roots of unity, as a tuple ordered counterclockwise around the unit circle, starting from *ω=1*. These are the numbers, *z*, for which `z ** n == 1` (at least, within floating-point precision.) The results correspond to the numbers `cartesian(modulus=1, phase=i*2*PI/n)` for `i = 0, 1, ..., n - 1` and are indexed accordingly.

Because `lmath.cartesian` is affected by `lmath.realcast`, the elements of the tuple are real when possible.

Raises `ValueError` if *n* is not an integer value not smaller than 1. Raises `TypeError` if *n* is not an integer value (floats with integer values—e.g., *n = 3.0*—are allowed.)

### `lmath.sqrt(z: Complex) -> Union[Real, Complex]`

Return the square root of *z*. There is one branch cut, from 0 along the negative real axis to -∞, continuous from above.

Defers to `cmath.sqrt` but is affected by `lmath.realcast`, so the result is real when *z* is real and nonnegative.

## Special functions

### `lmath.erf(x: Real) -> Real`

Return the [error function](https://en.wikipedia.org/wiki/Error_function) at x.

Defers to `math.erf`.

### `lmath.erfc(x: Real) -> Real`

Return the complementary error function at x; that is, return `1 - erf(x)` in a way that maintains precision for large *x*.

Defers to `math.erfc`.

### `lmath.gamma(x: Real) -> Real`

Return the [gamma function](https://en.wikipedia.org/wiki/Gamma_function) at *x*.

Defers to `math.gamma`.

### `lmath.normdist_pdf(x: Real, mu: Real = 0.0, sigma: Real = 1.0) -> Real`

Return the probability density function at *x* for the [normal distribution](https://en.wikipedia.org/wiki/Normal_distribution). The default parameters (μ=0, σ=1) give the standard normal distribution.

### `lmath.normdist_cdf(x: Real, mu: Real = 0.0, sigma: Real = 1.0) -> Real`

Return the cumulative distribution function at *x* for the [normal distribution](https://en.wikipedia.org/wiki/Normal_distribution). The default parameters (μ=0, σ=1) give the standard normal distribution.

In particular, `normdist_cdf(x, mu, sigma)` gives the probability that a measurement from a normal distribution with mean *mu* and standard deviation *sigma* is less than *x*. The probability that *a < x < b* is calculated as `normdist(b, ...) - normdist(a, ...)`.
