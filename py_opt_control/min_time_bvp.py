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
    Solve the minimum time state-to-state boundary value problem for a triple integrator.

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
        t, switch times, shape=(3,M)
        j, jerk values, shape=(3,M)

    The minimum time solutions are bang-coast-bang control sequences. These can
    be described by the initial state and a sequence of start times and jerk
    values for several constant-jerk segments. Here the time sequence begins
    with t=0 and ends with t=tf at the moment the final state is reached. The
    jerk value j[k] is applied from time t[k] until t[k+1]. Note that the jerk
    value j[-1] is irrelevant.

    The optimal number of segments is a function of the boundary values. Not every axis
    will have the same minimum number of segments, in which case it will be
    prepended by multiple coincident time=0, jerk=0 segments.
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

def switch_states(p0, v0, a0, t, j):
    """
    Given an initial state and an input switching sequence, compute the full
    state at each switch time. Returned a, v, p matrices are arranged like j.

    Inputs:
        p0, initial position,     shape=(3,)
        v0, initial velocity,     shape=(3,)
        a0, initial acceleration, shape=(3,)
        t, switch times, shape=(3,N)
        j, jerk,         shape=(3,N)
    Outputs:
        a, acceleration, shape=(3,N)
        v, velocity,     shape=(3,N)
        p, position,     shape=(3,N)

    For axis i at time t[i,k] the state is (p[i,k], v[i,k], a[i,k]) and a
    constant jerk segment with value j[i,k] is initiated.
    """
    n_axis   = p0.shape[0]
    n_switch = t.shape[1] # number of switch states


    p = np.zeros((n_axis, n_switch))
    v = np.zeros((n_axis, n_switch))
    a = np.zeros((n_axis, n_switch))

    p[:,0] = p0
    v[:,0] = v0
    a[:,0] = a0

    for n in range(n_axis):
        for i in range(0,  n_switch-1):
            dt = t[n,i+1] - t[n,i]
            p[n,i+1] = 1/6*j[n,i]*dt**3 + 1/2*a[n,i]*dt**2 + v[n,i]*dt + p[n,i]
            v[n,i+1] = 1/2*j[n,i]*dt**2 +     a[n,i]*dt    + v[n,i]
            a[n,i+1] =     j[n,i]*dt    +     a[n,i]

    return a, v, p

def sample_min_time_bvp(p0, v0, a0, t, j, dt):
    """
    Given an initial state and an input switching sequence, compute the full
    state at sampled times with resolution dt.

    Inputs:
        p0, initial position,     shape=(3,)
        v0, initial velocity,     shape=(3,)
        a0, initial acceleration, shape=(3,)
        t,  switch times, shape=(3,N)
        j,  jerk,         shape=(3,N)
        dt, time steps
    Outputs:
        st, times,        shape=(3,M)
        sj, jerk,         shape=(3,M)
        sa, acceleration, shape=(3,M)
        sv, velocity,     shape=(3,M)
        sp, position,     shape=(3,M)
    """

    n_axis = p0.size
    n_switch = t.shape[1]

    # It is expected that the final t for each axis are identical.
    end_t = t[:,-1].max()
    t[:,-1] = end_t

    # Allocate dense samples over time, jerk, acceleration, velocity, position.
    st = np.arange(t[0,0], end_t, dt)
    if st[-1] != end_t:
        st = np.append(st, end_t)
    n_sample = st.size
    sj = np.full((n_axis, n_sample), np.nan)
    sa = np.full((n_axis, n_sample), np.nan)
    sv = np.full((n_axis, n_sample), np.nan)
    sp = np.full((n_axis, n_sample), np.nan)

    # Accurate states at exact switching times.
    a, v, p = switch_states(p0, v0, a0, t, j)

    # Samples
    for n in range(n_axis):
        for i in range(n_switch-1):
            mask = np.logical_and(t[n,i] <= st, st <= t[n,i+1])
            dt = st[mask] - t[n,i]
            sp[n,mask] = 1/6*j[n,i]*dt**3 + 1/2*a[n,i]*dt**2 + v[n,i]*dt + p[n,i]
            sv[n,mask] = 1/2*j[n,i]*dt**2 +     a[n,i]*dt    + v[n,i]
            sa[n,mask] =     j[n,i]*dt    +     a[n,i]
            sj[n,mask] =     j[n,i]

    return st, sj, sa, sv, sp
