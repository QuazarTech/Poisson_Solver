#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import arrayfire as af
from fft_poisson_3d import fft_poisson


def test_fft_poisson():
    """
    This function tests that the FFT solver works as intended.
    We take an expression for density for which the fields can
    be calculated analytically, and check that the numerical
    solution as given by the FFT solver and the analytical
    solution correspond well with each other.
    """
    
    af.set_backend('cpu')
    
    x_start = 0
    y_start = 0
    z_start = 0

    x_end = 1
    y_end = 2
    z_end = 3

    N_x = np.random.randint(16, 32)
    N_y = np.random.randint(16, 32)
    N_z = np.random.randint(16, 32)
    
    print ("N_x", N_x)
    print ("N_y", N_y)
    print ("N_z", N_z)

    dx = (x_end - x_start) / N_x
    dy = (y_end - y_start) / N_y
    dz = (z_end - z_start) / N_z

    # Using a centered formulation for the grid points of x, y, z:
    x = x_start + (np.arange(N_x) + 0.5) * dx
    y = y_start + (np.arange(N_y) + 0.5) * dy
    z = z_start + (np.arange(N_z) + 0.5) * dz

    y, x, z = np.meshgrid(y, x, z)

    x = af.to_array(x)
    y = af.to_array(y)
    z = af.to_array(z)

    rho = af.sin(2 * np.pi * x + 4 * np.pi * y + 6 * np.pi * z)

    Ex_analytic = -(2 * np.pi) / (56 * np.pi**2) * \
                  af.cos(2 * np.pi * x + 4 * np.pi * y + 6 * np.pi * z)

    Ey_analytic = -(4 * np.pi) / (56 * np.pi**2) * \
                  af.cos(2 * np.pi * x + 4 * np.pi * y + 6 * np.pi * z)

    Ez_analytic = -(6 * np.pi) / (56 * np.pi**2) * \
                  af.cos(2 * np.pi * x + 4 * np.pi * y + 6 * np.pi * z)

    potential, Ex_numerical, Ey_numerical, Ez_numerical = fft_poisson(rho, dx, dy, dz)

    # Checking that the L1 norm of error is at machine precision:
    Ex_err = af.sum(af.abs(Ex_numerical - Ex_analytic)) / Ex_analytic.elements()
    Ey_err = af.sum(af.abs(Ey_numerical - Ey_analytic)) / Ey_analytic.elements()
    Ez_err = af.sum(af.abs(Ez_numerical - Ez_analytic)) / Ez_analytic.elements()
    
    print ("Ex_err : ",Ex_err)
    print ("Ey_err : ",Ey_err)
    print ("Ez_err : ",Ez_err)

    assert(Ex_err < 1e-14)
    assert(Ey_err < 1e-14)
    assert(Ez_err < 1e-14)
    
test_fft_poisson()
