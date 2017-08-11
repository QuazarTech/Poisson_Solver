#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import arrayfire as af


def fft_poisson(rho, dx, dy, dz):
    """
    It is assumed that the rho array is defined such that:
    axis 0 - variation along x
    axis 1 - variation along y
    axis 2 - variation along z

    This FFT solver will work only when run using periodic boundary conditions.

    Additionally, it should be noted that the physical points should be passed
    to this function. Passing the non-physical(ghost) zones will generate
    erroneous results

    NOTE: The density that is passed to this function is the charge density.
    """
    k_x = np.fft.fftfreq(rho.shape[0], dx)
    k_y = np.fft.fftfreq(rho.shape[1], dy)
    k_z = np.fft.fftfreq(rho.shape[2], dz)

    k_y, k_x, k_z = np.meshgrid(k_y, k_x, k_z)

    k_x = af.to_array(k_x)
    k_y = af.to_array(k_y)
    k_z = af.to_array(k_z)

    rho_hat = af.fft3(rho)

    potential_hat = rho_hat / (4 * np.pi**2 * (k_x**2 + k_y**2 + k_z**2))

    # At the [0, 0, 0] index, k_x = k_y = k_z = 0
    # Manually assigning to zero(from inf) 
    potential_hat[0, 0, 0] = 0

    Ex_hat = -1j * 2 * np.pi * k_x * potential_hat
    Ey_hat = -1j * 2 * np.pi * k_y * potential_hat
    Ez_hat = -1j * 2 * np.pi * k_z * potential_hat

    Ex = af.ifft3(Ex_hat)
    Ey = af.ifft3(Ey_hat)
    Ez = af.ifft3(Ez_hat)
    
    potential = af.ifft3(potential_hat)

    return(potential, Ex, Ey, Ez)
