# lilellia

This module is designed to provide an array of utilities, including a revamp/wrapper of Python's stdlib `math` and `itertools` modules.

Supported: Python 3.6+

## Main changes

### `math/cmath` vs. `lmath`

- `lmath` bridges the two stdlib math modules together by allowing complex-number results when necessary but converting them to real numbers whenever possible. Thus, `lmath.sqrt(4)` returns `2.0`, while `lmath.sqrt(-4)` returns `2j`.
- `lmath` allows for an arguably more seamless transition between angle modes in its (inverse) trigonometric calculations. Both stdlib modules *always* accept/return radian angles and must be manually converted via `math.radians` or `math.degrees`. With `lmath`, there is a module-level variable (`lmath.ANGLE_MODE: str`), which is read by the module's trig functions to determine how to interpret their inputs and outputs. A context manager (`lmath.force_angle_mode(temp_mode: str)`) which allows for local, temporary switches.
