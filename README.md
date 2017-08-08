# Poisson Solver:

This project contains the files which solve the Poisson equation:

<p align="center"><img src="https://rawgit.com/QuazarTech/Poisson_Solver/master/.svgs/d081cfc402036f5c2f39b090d8461018.svg?invert_in_darkmode" align=middle width=169.36425pt height=36.953894999999996pt/></p>

## Dependencies:

The solver makes use of [ArrayFire](https://github.com/arrayfire/arrayfire) and requires it to be built and installed on the system of usage in addition to the python interface([arrayfire-python](https://github.com/arrayfire/arrayfire-python). The following Python packages are also required:
* numpy
* pytest

Once [ArrayFire](https://github.com/arrayfire/arrayfire) is installed successfully, all other dependencies can be installed using `pip install -r requirements.txt`

## Usage:

The function `fft_poisson` assumes that in the density array, `x` varies along axis 0, `y` varies along axis 1, `z` varies along axis 2. Additionally, we consider cell centered formulation to be used throughout. Hence the density array needs to be passed to the function following these conventions:
```python
from fft_poisson_3d import fft_poisson
Ex, Ey, Ez = fft_poisson(rho, dx, dy, dz)
```
## Testing:

The solver can be tested by running:
```python
py.test test_fft_poisson_3d.py
```

