import numpy as np
import numpy.ctypeslib as npct
from ctypes import c_double, c_int32, c_bool
import pathlib

# Load the library, using numpy mechanisms.
path = pathlib.Path(__file__).parent.parent.absolute() / "build"
libcd = npct.load_library("lib_min_time_bvp", path)

# Setup the return types and argument types.
array_1d_double = npct.ndpointer(dtype=np.double, ndim=1, flags=('C_CONTIGUOUS'))
array_2d_double = npct.ndpointer(dtype=np.double, ndim=2, flags=('C_CONTIGUOUS'))
libcd.min_time_bvp.restype = None
libcd.min_time_bvp.argtypes = [
    c_int32,
    array_1d_double, array_1d_double, array_1d_double,
    array_1d_double, array_1d_double, array_1d_double,
    c_double, c_double, c_double, c_double, c_double, c_double,
    c_bool, c_bool, c_bool,
    array_2d_double, array_2d_double]

def min_time_bvp(
    p0, v0, a0,
    p1, v1, a1,
    v_min, v_max, a_min, a_max, j_min, j_max,
    sync_v=True,
    sync_a=True,
    sync_w=True):
    """
    Solve the minimum time state-to-state boundary value problem for a triple
    integrator in N dimensions.

    Inputs:
        p0, initial position, shape=(N,)
        v0, initial velocity, shape=(N,)
        a0, initial acceleration, shape=(N,)
        p1, final position, shape=(N,)
        v1, final velocity, shape=(N,)
        a1, final acceleration, shape=(N,)
        v_min, v_max, velocity limits, scalars
        a_min, a_max, acceleration limits, scalars
        j_min, j_max, jerk limits, scalars
        sync_v, synchronize arrivals by reducing velocities
        sync_a, synchronize arrivals by reducing accelerations
        sync_w, synchronize arrivals by waiting (overrides other sync params)

    Outputs:
        t, switch times, shape=(N,M)
        j, jerk values, shape=(N,M)

    The minimum time solutions are bang-coast-bang control sequences. These can
    be described by the initial state (p0,v0,a0) and a sequence of start times t
    and jerk values j for several constant-jerk segments. Here the time sequence
    begins with t=0 and ends with t=tf at the moment the final state is reached.
    The jerk value j[k] is applied from time t[k] until t[k+1]. Note that the
    jerk value j[-1] is irrelevant.

    The optimal number of segments is a function of the boundary values. Not
    every axis will have the same minimum number of segments, in which case it
    will be prepended by multiple coincident time=0, jerk=0 segments.
    """

    (p0, v0, a0, p1, v1, a1) = (s.astype(np.float64, copy=False) for s in (p0, v0, a0, p1, v1, a1))

    n_dim = p0.size

    # The interface uses an excess fixed sized array for the output control steps.
    stride = 32 # Excess size.
    t = np.full((n_dim,stride), np.nan, dtype=np.float64)
    j = np.full((n_dim,stride), np.nan, dtype=np.float64)

    # Call to C++ implementation.
    libcd.min_time_bvp(
        n_dim,
        p0, v0, a0,
        p1, v1, a1,
        v_min, v_max, a_min, a_max, j_min, j_max,
        sync_v, sync_a, sync_w,
        t, j)

    # Remove redundant steps in the control sequence and trim the fixed size
    # array. The output of the C library call is a little odd -- signals need to
    # be applied in the original order, and nearly-identical times might not
    # necessarily appear in chronological order.
    t_list = []
    j_list = []
    n_steps = 0
    for i in range(n_dim):
        mask = np.logical_not(np.isnan(t[i,:]))
        (_, first_index, count) = np.unique(t[i,mask], return_index=True, return_counts=True)
        last_index = first_index + count - 1
        last_index.sort()
        t_list.append(t[i,last_index])
        j_list.append(j[i,last_index])
    n_steps = max(len(tl) for tl in t_list)
    t_final = np.zeros((n_dim, n_steps))
    j_final = np.zeros((n_dim, n_steps))
    for i in range(n_dim):
        n = len(t_list[i])
        t_final[i,-n:] = t_list[i]
        j_final[i,-n:] = j_list[i]

    return t_final, j_final

def min_time_bvp_paranoia(
    p0, v0, a0,
    p1, v1, a1,
    v_min, v_max, a_min, a_max, j_min, j_max,
    sync_v=True,
    sync_a=True,
    sync_w=True):
    t, j = min_time_bvp(
        p0, v0, a0,
        p1, v1, a1,
        v_min, v_max, a_min, a_max, j_min, j_max,
        sync_v,
        sync_a,
        sync_w)
    a, v, p = switch_states(p0, v0, a0, t, j)
    st, sj, sa, sv, sp = sample_min_time_bvp(p0, v0, a0, t, j, dt=0.01)
    is_valid = np.allclose(p1, sp[:,-1])
    if not is_valid:
        sync_w = not sync_w
        t, j = min_time_bvp(
            p0, v0, a0,
            p1, v1, a1,
            v_min, v_max, a_min, a_max, j_min, j_max,
            sync_v,
            sync_a,
            sync_w)
        a, v, p = switch_states(p0, v0, a0, t, j)
        st, sj, sa, sv, sp = sample_min_time_bvp(p0, v0, a0, t, j, dt=0.01)
    return t, j

def switch_states(p0, v0, a0, t, j):
    """
    Given an initial state and an input switching sequence, compute the full
    state at each switch time. Returned a, v, p matrices are arranged like j.

    Inputs:
        p0, initial position,     shape=(N,)
        v0, initial velocity,     shape=(N,)
        a0, initial acceleration, shape=(N,)
        t, switch times, shape=(N,M)
        j, jerk,         shape=(N,M)
    Outputs:
        a, acceleration, shape=(N,M)
        v, velocity,     shape=(N,M)
        p, position,     shape=(N,M)

    For axis i at time t[i,k] the state is (p[i,k], v[i,k], a[i,k]) and a
    constant jerk segment with value j[i,k] is initiated.
    """
    
    n_axis   = p0.size
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

def sample(p0, v0, a0, t, j, st):
    """
    Given an initial state and an input switching sequence, compute the full
    state at a set of explicitly specified sample times. 

    Inputs:
        p0, initial position,     shape=(N,)
        v0, initial velocity,     shape=(N,)
        a0, initial acceleration, shape=(N,)
        t,  switch times, shape=(N,M)
        j,  jerk,         shape=(N,M)
        st, samplle_time, shape=(K,)
    Outputs:
        st, times,        shape=(N,K)
        sj, jerk,         shape=(N,K)
        sa, acceleration, shape=(N,K)
        sv, velocity,     shape=(N,K)
        sp, position,     shape=(N,K)
    """

    n_axis = p0.size
    n_switch = t.shape[1]

    # Accurate states at exact switching times.
    a, v, p = switch_states(p0, v0, a0, t, j)

    if t.shape[1] > 1:
        n_sample = st.size
        sj = np.full((n_axis, n_sample), np.nan)
        sa = np.full((n_axis, n_sample), np.nan)
        sv = np.full((n_axis, n_sample), np.nan)
        sp = np.full((n_axis, n_sample), np.nan)

        # Samples
        for n in range(n_axis):
            for i in range(n_switch-1):
                mask = np.logical_and(t[n,i] <= st, st <= t[n,i+1])
                dt = st[mask] - t[n,i]
                sp[n,mask] = 1/6*j[n,i]*dt**3 + 1/2*a[n,i]*dt**2 + v[n,i]*dt + p[n,i]
                sv[n,mask] = 1/2*j[n,i]*dt**2 +     a[n,i]*dt    + v[n,i]
                sa[n,mask] =     j[n,i]*dt    +     a[n,i]
                sj[n,mask] =     j[n,i]
    else:
        # No sampling needed for zero time solution.
        st, sj, sa, sv, sp = t, j, a, v, p

    return st, sj, sa, sv, sp

def uniformly_sample(p0, v0, a0, t, j, dt):
    """
    Given an initial state and an input switching sequence, compute the full
    state at sampled times with resolution dt. 

    Inputs:
        p0, initial position,     shape=(N,)
        v0, initial velocity,     shape=(N,)
        a0, initial acceleration, shape=(N,)
        t,  switch times, shape=(N,M)
        j,  jerk,         shape=(N,M)
        dt, time resolution
    Outputs:
        st, times,        shape=(N,K)
        sj, jerk,         shape=(N,K)
        sa, acceleration, shape=(N,K)
        sv, velocity,     shape=(N,K)
        sp, position,     shape=(N,K)
    """

    # It is expected that the final t for each axis are identical.
    end_t = t[:,-1].max()
    t[:,-1] = end_t
    
    # Allocate dense samples over time, jerk, acceleration, velocity, position.
    st = np.arange(t[0,0], end_t, dt)
    if st[-1] != end_t: # The final sample time gets exactly to the end state.
        st = np.append(st, end_t)

    _, sj, sa, sv, sp = sample(p0, v0, a0, t, j, st)
    return st, sj, sa, sv, sp
