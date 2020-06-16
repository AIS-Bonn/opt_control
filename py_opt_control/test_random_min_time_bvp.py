# TODO: Disentangle calculations from plotting so this function can also be used
# to profile computational speed.

import numpy as np
import matplotlib.pyplot as plt
import min_time_bvp

# Number of dimensions to test {1, 2, 3}.
n_dim = 2

# Constants
v_min = -10
v_max = 10
a_min = -5
a_max = 5
j_min = -100
j_max = 100

# Random initial states.
decimal_places = 1
N = 50
p0 = np.random.uniform(0, 1, (N,n_dim))
v0_master = np.random.uniform(0, 1, (N,n_dim))
a0_master = np.random.uniform(0, 1, (N,n_dim))
p0 = np.round(p0, decimal_places)
v0_master = np.round(v0_master, decimal_places)
a0_master = np.round(a0_master, decimal_places)

# Hard coded final state, truncated to selected number of dimensions.
p1 = np.array([1, 1, 1], dtype=np.float64)
v1 = np.array([0, 0, 0], dtype=np.float64)
a1 = np.array([0, 0, 0], dtype=np.float64)
p1 = p1[:n_dim]
v1 = v1[:n_dim]
a1 = a1[:n_dim]

fig, axes = plt.subplots(2, 2)
axes = axes.flatten()
hard_indices = []
for jj in range(3):
    if jj == 0:
        v0 = 0 * v0_master
        a0 = 0 * a0_master
        axes[jj].set_title('Zero Initial Velocity and Acceleration')
    elif jj == 1:
        v0 = 1 * v0_master
        a0 = 0 * a0_master
        axes[jj].set_title('Fixed Initial Velocity, Zero Acceleration')
    elif jj == 2:
        v0 = 1 * v0_master
        a0 = 1 * a0_master
        axes[jj].set_title('Fixed Initial Velocity and Acceleration')
    for i in range(N):
        (t, j) = min_time_bvp.min_time_bvp(
            p0[i], v0[i], a0[i],
            p1, v1, a1,
            v_min, v_max, a_min, a_max, j_min, j_max)

        a, v, p = min_time_bvp.switch_states(p0[i], v0[i], a0[i], t, j)
        st, sj, sa, sv, sp = min_time_bvp.sample_min_time_bvp(p0[i], v0[i], a0[i], t, j, dt=0.01)

        if not np.allclose(p1, sp[:,-1]):
            print('\nTest failed: end position is wrong. Initial condition:')
            print(p0[i])
            print(v0[i])
            print(a0[i])
            print()
            hard_indices.append(i)

        if n_dim > 1:
            axes[jj].plot(sp[0,:], sp[1,:])
        else:
            axes[jj].plot(sp[0,:], np.zeros_like(sp[0,:]))

    axes[jj].set_xlim((-0.2, 1.2))
    axes[jj].set_ylim((-0.2, 1.2))
    axes[jj].axis('equal')
fig.suptitle('Motions to stop at (1,1,1)')

print(f"Failed {len(hard_indices)}/{N} tests.")

# Show plots.
plt.show()
