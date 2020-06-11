
import numpy as np
import numpy.ctypeslib as npct
from ctypes import c_double

# Load the library, using numpy mechanisms.
libcd = npct.load_library("lib_min_time_bvp", ".")

# Setup the return types and argument types.
array_1d_double = npct.ndpointer(dtype=np.double, ndim=1, flags='CONTIGUOUS')
array_2d_double = npct.ndpointer(dtype=np.double, ndim=2, flags='CONTIGUOUS')
libcd.min_time_bvp.restype = None
libcd.min_time_bvp.argtypes = [
    array_1d_double, array_1d_double, array_1d_double,
    array_1d_double, array_1d_double, array_1d_double,
    c_double, c_double, c_double, c_double, c_double, c_double,
    array_2d_double, array_2d_double]

def min_time_bvp(
    p0, v0, a0,
    p1, v1, a1,
    v_min, v_max, a_min, a_max, j_min, j_max):
    """
    Solve the minimum time state to state boundary value problem for a triple integrator.

    Inputs:
        p0, initial position, shape=(3,)
        v0, initial velocity, shape=(3,)
        a0, initial acceleration, shape=(3,)
        p1, final position, shape=(3,)
        v1, final velocity, shape=(3,)
        a1, final acceleration, shape=(3,)
        v_min, v_max, velocity limits, scalars
        a_min, a_max, acceleration limits, scalars
        j_min, j_max, jerk limits, scalars

    Outputs:
        t, start time for each constant jerk segment, shape=(3,M)
        j, jerk for each constant jerk segment, shape=(3,M)

    The minimum time solutions are bang-coast-bang control sequences. These can
    be described by a sequence of start times and jerk values for M
    constant-jerk segments. The number of segments is a function of the boundary
    values. Not every axis will have the same minimum number of segments, in
    which case it will be prepended by time=0, jerk=0 segments.
    """

    # The interface uses an excess fixed sized array for the output control steps.
    stride = 32 # Excess size.
    t = np.full((3,stride), np.nan, dtype=np.float64)
    j = np.full((3,stride), np.nan, dtype=np.float64)

    # Call to C++ implementation.
    libcd.min_time_bvp(
        p0, v0, a0,
        p1, v1, a1,
        v_min, v_max, a_min, a_max, j_min, j_max,
        t, j)

    # Remove redundant steps in the control sequence and trim the fixed size array.
    t_list = []
    j_list = []
    n_steps = 0
    for i in range(3):
        mask = np.logical_not(np.isnan(t[i,:]))
        (value, first_index, count) = np.unique(t[i,mask], return_index=True, return_counts=True)
        last_index = first_index + count - 1
        t_list.append(t[i,last_index])
        j_list.append(j[i,last_index])
        n_steps = max(n_steps, value.size)

    t_final = np.zeros((3, n_steps))
    j_final = np.zeros((3, n_steps))
    for i in range(3):
        n = len(t_list[i])
        t_final[i,-n:] = t_list[i]
        j_final[i,-n:] = j_list[i]

    return t_final, j_final
