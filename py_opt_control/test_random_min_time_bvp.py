# Randomized testing over a variety of types of boundary conditions.

import numpy as np
import matplotlib.pyplot as plt
import min_time_bvp

def compute_many_mp(p0, v0, a0, p1, v1, a1, params):
    """
    Compute and verify many motion primitives.
    """
    n_mp = p0.shape[0]
    mp = []
    for i in range(n_mp):
        (t, j) = min_time_bvp.min_time_bvp(
            p0[i], v0[i], a0[i],
            p1[i], v1[i], a1[i],
            params['v_min'], params['v_max'], params['a_min'], params['a_max'], params['j_min'], params['j_max'],
            params['sync_v'], params['sync_a'], params['sync_w'])
        a, v, p = min_time_bvp.switch_states(p0[i], v0[i], a0[i], t, j)
        st, sj, sa, sv, sp = min_time_bvp.sample_min_time_bvp(p0[i], v0[i], a0[i], t, j, dt=0.01)
        is_valid = np.allclose(p1[i], sp[:,-1])
        if not is_valid:
            print('\nTest failed: end position is wrong. Initial condition:')
            print(p0[i])
            print(v0[i])
            print(a0[i])
            print()
        mp.append({'p0':p0[i], 'v0':v0[i], 'a0':a0[i], 't':t, 'j':j, 'is_valid':is_valid})
    return mp


def plot_2d_projection_many_mp(ax, mp):
    """
    Plot many motion primitives projected onto the x-y axis, independent of
    original dimension.
    """
    n_dim = mp[0]['p0'].shape[0]

    for m in mp:
        if m['is_valid']:
            st, sj, sa, sv, sp = min_time_bvp.sample_min_time_bvp(
                m['p0'], m['v0'], m['a0'], m['t'], m['j'], dt=0.001)
            if n_dim > 1:
                ax.plot(sp[0,:], sp[1,:])
            else:
                ax.plot(sp[0,:], np.zeros_like(sp[0,:]))
    ax.axis('equal')

def test_to_zero(n_dim, params, n_tests, ax):
    decimal_places = 2
    p0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    v0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    a0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    p1 = np.zeros((n_tests,n_dim))
    v1 = np.zeros((n_tests,n_dim))
    a1 = np.zeros((n_tests,n_dim))
    mp = compute_many_mp(p0, v0, a0, p1, v1, a1, params)
    plot_2d_projection_many_mp(ax, mp)
    return sum(1 for m in mp if not m['is_valid'])

def test_to_nonzero_p(n_dim, params, n_tests, ax):
    decimal_places = 2
    p0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    v0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    a0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    p1 = np.ones((n_tests,n_dim))
    v1 = np.zeros((n_tests,n_dim))
    a1 = np.zeros((n_tests,n_dim))
    mp = compute_many_mp(p0, v0, a0, p1, v1, a1, params)
    plot_2d_projection_many_mp(ax, mp)
    return sum(1 for m in mp if not m['is_valid'])

def test_to_nonzero_pv(n_dim, params, n_tests, ax):
    decimal_places = 2
    p0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    v0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    a0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    p1 = np.ones((n_tests,n_dim))
    v1 = np.ones((n_tests,n_tests))
    v1[:,1:] = -1
    a1 = np.zeros((n_tests,n_dim))
    mp = compute_many_mp(p0, v0, a0, p1, v1, a1, params)
    plot_2d_projection_many_mp(ax, mp)
    return sum(1 for m in mp if not m['is_valid'])

def test_to_nonzero_pva(n_dim, params, n_tests, ax):
    decimal_places = 2
    p0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    v0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    a0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    p1 = np.ones((n_tests,n_dim))
    v1 = np.ones((n_tests,n_tests))
    v1[:,1:] = -1
    a1 = -np.ones((n_tests,n_tests))
    a1[:,1:] = 1
    mp = compute_many_mp(p0, v0, a0, p1, v1, a1, params)
    plot_2d_projection_many_mp(ax, mp)
    return sum(1 for m in mp if not m['is_valid'])

def test_zero_a(n_dim, params, n_tests, ax):
    decimal_places = 2
    p0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    v0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    a0 = np.zeros((n_tests,n_dim))
    p1 = np.ones((n_tests,n_dim))
    v1 = np.ones((n_tests,n_tests))
    v1[:,1:] = -1
    a1 = np.zeros((n_tests,n_dim))
    mp = compute_many_mp(p0, v0, a0, p1, v1, a1, params)
    plot_2d_projection_many_mp(ax, mp)
    return sum(1 for m in mp if not m['is_valid'])

def test_zero_va(n_dim, params, n_tests, ax):
    decimal_places = 2
    p0 = np.round(np.random.uniform(-1, 1, (n_tests,n_dim)), decimal_places)
    v0 = np.zeros((n_tests,n_dim))
    a0 = np.zeros((n_tests,n_dim))
    p1 = np.ones((n_tests,n_dim))
    v1 = np.zeros((n_tests,n_dim))
    a1 = np.zeros((n_tests,n_dim))
    mp = compute_many_mp(p0, v0, a0, p1, v1, a1, params)
    plot_2d_projection_many_mp(ax, mp)
    return sum(1 for m in mp if not m['is_valid'])

if __name__ == '__main__':

    n_tests = 100

    n_dim = 2

    params = {
        'v_min':  -10,
        'v_max':   10,
        'a_min':   -5,
        'a_max':    5,
        'j_min': -100,
        'j_max':  100,
        'sync_v': True,
        'sync_a': True,
        'sync_w': False,
    }

    fig, axes = plt.subplots(2, 2)
    axes = axes.flatten()
    n_failed = test_to_zero(n_dim, params, n_tests, axes[0])
    axes[0].set_title(f'To Zero State, Failed {n_failed}/{n_tests}')
    n_failed = test_to_nonzero_p(n_dim, params, n_tests, axes[1])
    axes[1].set_title(f'To Nonzero P, Failed {n_failed}/{n_tests}')
    n_failed = test_to_nonzero_pv(n_dim, params, n_tests, axes[2])
    axes[2].set_title(f'To Nonzero P-V, Failed {n_failed}/{n_tests}')
    n_failed = test_to_nonzero_pva(n_dim, params, n_tests, axes[3])
    axes[3].set_title(f'To Nonzero P-V-A, Failed {n_failed}/{n_tests}')

    fig, axes = plt.subplots(2, 1)
    axes = axes.flatten()
    n_failed = test_zero_va(n_dim, params, n_tests, axes[1])
    axes[1].set_title(f'Zero V-A Boundaries, Failed {n_failed}/{n_tests}')
    n_failed = test_zero_a(n_dim, params, n_tests, axes[0])
    axes[0].set_title(f'Zero A Boundaries, Failed {n_failed}/{n_tests}')

    # Show plots.
    plt.show()
