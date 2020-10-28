import cmath
import collections
import contextlib
import functools
import itertools
import math
from numbers import Complex, Integral, Real
import sys
from typing import Any, Callable, Iterable, Optional, Tuple, Union


# Expose constants from `math` and `cmath` modules, using uppercase identifiers to mark them as constant.
PI = math.pi
TAU = math.tau
E = math.e
INF = math.inf
NAN = math.nan
INFI = INFJ = cmath.infj
NANI = NANJ = cmath.nanj


# Number-Theoretic and Representation Functions

def ceil(x: Real) -> Integral:
    """ Return the ceiling of x, the smallest integer value >= x.
    If x is not a float, this delegates to x.__ceil()__, which should return an Integral value. """
    return math.ceil(x)


def choose(n: int, k: int) -> int:
    """ Return the number of ways to choose k items from n without repetition and without order. """
    if sys.version_info >= (3, 8):
        return math.comb(n, k)

    # math.comb was only added in Python 3.8, so if we aren't running 3.8+, we'll have to write the function ourselves
    if n < 0:
        raise ValueError('n must be a non-negative integer')

    if k < 0:
        raise ValueError('k must be a non-negative integer')

    if k > n:
        return 0

    return factorial(n) / factorial(k) / factorial(n - k)


def factorial(x: Union[int, float]) -> int:
    """ Return x!, x factorial. """
    if isinstance(x, float) and not x.is_integer():
        raise ValueError('factorial() only accepts integral values')

    # convert to int to avoid 3.9+ deprecation for floats
    return math.factorial(int(x))


def floor(x: Real) -> Integral:
    """ Return the floor of x, the largest integer <= x. """
    return math.floor(x)


def gcd(*values: int) -> int:
    """ Return the greatest common divisor of the specified integer arguments. """
    if sys.version_info >= (3, 9):
        return math.gcd(*values)

    # In 3.9+, math.gcd allows arbitrarily many arguments. Pre-3.9, it expects exactly two.
    if len(values) == 0:
        return 0

    if len(values) == 1:
        # abs since gcd > 0
        return abs(values[0])

    if len(values) == 2:
        return math.gcd(*values)

    # with n > 2 arguments, we can recurse this to (n - 1) arguments by taking the gcd of the first two in their place
    a, b, *values = values
    return gcd(gcd(a, b), *values)


def lcm(*values: int) -> int:
    """ Return the least common multiple of the specified integer arguments. """
    if sys.version_info >= (3, 9):
        return math.lcm(*values)

    # math.lcm was only added in Python 3.9.

    if not all(isinstance(v, int) for v in values):
        raise TypeError('lcm() only accepts integer values')

    if len(values) == 0:
        return 1

    if len(values) == 1:
        # abs since lcm > 0
        return abs(values[0])

    if len(values) == 2:
        # lcm(a, b) = |ab| / gcd(a, b)
        a, b = values
        return abs(a * b) // gcd(a, b)

    # with n > 2 arguments, we can recurse this to (n - 1) by taking the lcm of the first two in their place
    a, b, *values = values
    return lcm(lcm(a, b), *values)


def modf(x: Real) -> Tuple[float, int]:
    """ Return the fractional and integer parts of x. """
    ModF = collections.namedtuple('ModF', ('fpart', 'ipart'))

    f, i = math.modf(x)
    return ModF(fpart=f, ipart=int(i))


def permutations(n: int, k: Optional[int] = None) -> int:
    """ Return the number of ways k items can be chosen from n without repetition but with order. """
    if sys.version_info >= (3, 8):
        return math.perm(n, k)

    # math.perm was only added in Python 3.8.
    if n < 0 or not isinstance(n, int):
        raise ValueError('n must be a non-negative integer')

    if k < 0 or not isinstance(k, int):
        raise ValueError('k must be a non-negative integer')

    if k > n:
        return 0

    return factorial(n) / factorial(n - k)

# Complex representation functions


def realcast(func: Callable[..., Complex], tol: float = 1e-12) -> Callable[..., Union[Real, Complex]]:
    """ A decorator to cast the output of the function as real when its imaginary part is sufficiently small. """
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        z = func(*args, **kwargs)
        if cmath.isclose(z.imag, 0.0, abs_tol=tol):
            return z.real
        return z

    return wrapped


@realcast
def cartesian(modulus: float, phase: float) -> Complex:
    """ Return the complex number with polar coordinates (modulus, phase). """
    return cmath.rect(modulus, phase)


def phase(z: Complex) -> float:
    """ Return the phase (argument) of z, as a float. The result is on [0, 2π). """
    @output_angle
    def _phase(z: Complex):
        phi = cmath.phase(z)

        # add 2π (τ) if the phase is negative (cmath.phase returns on [-π, π])
        # use abs(...) since cmath.phase(complex(1, -0.0)) == -0.0 (which is >= 0)
        return abs(phi) if phi >= 0 else phi + TAU
    return _phase(z)


def polar(z: Complex) -> Tuple[float, float]:
    """ Return the polar representation of z as the pair (r, phi). """
    Polar = collections.namedtuple('Polar', ('modulus', 'phase'))

    return Polar(modulus=abs(z), phase=phase(z))


# Trigonometric utilities

ANGLE_MODE: str = "RADIANS"


@contextlib.contextmanager
def force_angle_mode(temp_mode: str):
    """ A context manager that locally overrides the angle mode to be the given mode. """
    global ANGLE_MODE

    original = ANGLE_MODE

    try:
        ANGLE_MODE = temp_mode
        yield
    finally:
        ANGLE_MODE = original


# provide shorter alias
fam = force_angle_mode


def accept_angle(func: Callable[[Real], Any]) -> Callable[[Real], Any]:
    """ A decorator that uses ANGLE_MODE to parse its input angle in degrees or in radian. """
    @functools.wraps(func)
    def wrapped(theta):
        if ANGLE_MODE.upper() not in {'RADIANS', 'DEGREES'}:
            raise ValueError(f'ANGLE_MODE must be one of "RADIANS" and "DEGREES", not {ANGLE_MODE}')

        if ANGLE_MODE.upper() == 'DEGREES':
            theta *= PI / 180

        return func(theta)

    return wrapped


def output_angle(func: Callable[..., Real]) -> Callable[..., Real]:
    """ A decorator that uses ANGLE_MODE to parse its output angle in degrees or in radians. """
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        if ANGLE_MODE.upper() not in {'RADIANS', 'DEGREES'}:
            raise ValueError(f'ANGLE_MODE must be one of "RADIANS" and "DEGREES", not {ANGLE_MODE}')

        theta = func(*args, **kwargs)

        if ANGLE_MODE.upper() == 'DEGREES':
            return theta * 180 / PI
        return theta
    return wrapped


# Trigonometric functions

arccos = realcast(output_angle(cmath.acos))
arcsin = realcast(output_angle(cmath.asin))


@realcast
@output_angle
def arctan(z: Complex, a: Optional[Real] = None) -> Union[Real, Complex]:
    """ Return the arctangent of z when a is None. Return the quadrant-adjusted arctangent of z/a otherwise. """
    if a is None:
        return cmath.atan(z)

    if not isinstance(z, Real):
        raise ValueError('arctan(z, a): z must be real in two-argument arctan')
    if not isinstance(a, Real):
        raise ValueError('arctan(z, a): a must be real in two-argument arctan')

    return phase(complex(a, z))


cos = realcast(accept_angle(cmath.cos))
sin = realcast(accept_angle(cmath.sin))
tan = realcast(accept_angle(cmath.tan))


def distance(p: Iterable[Real], q: Iterable[Real]) -> float:
    """ Return the distance between points p and q in R² space. """
    distsqr = sum(pow(px - qx, 2.0) for px, qx in itertools.zip_longest(p, q, fillvalue=0))
    return sqrt(distsqr)


# Hyperbolic trig functions

arccosh = realcast(output_angle(cmath.acosh))
arcsinh = realcast(output_angle(cmath.asinh))
arctanh = realcast(output_angle(cmath.atanh))

cosh = realcast(accept_angle(cmath.cosh))
sinh = realcast(accept_angle(cmath.sinh))
tanh = realcast(accept_angle(cmath.tanh))


# Power and logarithmic functions

@realcast
def exp(z: Complex) -> Union[Real, Complex]:
    """ Return e**x, where e = 2.718... is Euler's constant.
    This is usually more precise than E**z or pow(E, z).
    """
    return cmath.exp(z)


def expm1(x: Real) -> Real:
    """ Return exp(x) - 1 in a way that maintains precision for small x. """
    return math.expm1(x)


def log(z: Complex, base: Optional[Complex] = None) -> Union[Real, Complex]:
    """ Returns the logarithm of z with the given base. When the base is None, return the natural log. """

    if isinstance(z, Real) and base is None:
        # use log1p(z - 1), which maintains precision for z close to 1
        return math.log1p(z - 1)

    if isinstance(z, Real) and base == 2:
        # usually more precise than log(z, 2) but only works for real z
        return math.log2(z)

    if base == 10:
        # usually more precise than log(z, 10)
        return cmath.log10(z)

    if base is None:
        # cmath.log(z, None) is a ValueError, so we need to handle this separately
        return cmath.log(z)

    return cmath.log(z, base)


def roots_of_unity(n: int) -> Tuple[Complex]:
    """ Return the nth roots of unity, as a tuple.
    They are ordered going counterclockwise around the unit circle, starting at ω = 1. """

    if isinstance(n, float) and n.is_integer():
        n = int(n)

    if n < 1:
        raise ValueError('nth roots of unity: n must be >= 1')

    if not isinstance(n, int):
        raise TypeError('nth roots of unity: n must be a positive integer')

    with force_angle_mode('radians'):
        return tuple(
            cartesian(modulus=1, phase=i*2*PI/n)
            for i in range(n)
        )


@realcast
def sqrt(z: Complex) -> Union[Real, Complex]:
    """ Return the square root of z. """
    return cmath.sqrt(z)


# Special functions


erf = math.erf
erfc = math.erfc
gamma = math.gamma


def normdist_pdf(x: Real, mu: Real = 0.0, sigma: Real = 1.0) -> Real:
    """ Return the probability density function for the normal distribution at x. """
    k = sigma * sqrt(2 * PI)
    z = (x - mu) / sigma

    return exp(-0.5 * z ** 2) / k


def normdist_cdf(x: Real, mu: Real = 0.0, sigma: Real = 1.0) -> Real:
    """ Return the CDF for the normal distribution at x. """
    z = (x - mu) / sigma

    return 0.5 + 0.5 * erf(z / sqrt(2))
