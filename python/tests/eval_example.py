import numpy as np
import matplotlib.pyplot as plt
from py_opt_control import min_time_bvp

# Number of dimensions to test {1, 2, 3}.
n_dim = 2

# Constants
v_min = -10
v_max = 10
a_min = -5
a_max = 5
j_min = -100
j_max = 100

# Time series plot of full state.

# Hard coded initial and final state.
p0 = np.array([0, 0.5, 0], dtype=np.float64)
v0 = np.array([0, 0, 0], dtype=np.float64)
a0 = np.array([0, 0, 0], dtype=np.float64)
p1 = np.array([1, 2, -1], dtype=np.float64)
v1 = np.array([0, 0, 0], dtype=np.float64)
a1 = np.array([0, 0, 0], dtype=np.float64)

# If n_dim about is not 3, truncate to the desired dimension.
p0 = p0[:n_dim]
v0 = p0[:n_dim]
a0 = p0[:n_dim]
p1 = p1[:n_dim]
v1 = p1[:n_dim]
a1 = p1[:n_dim]

# Compute the jerk input sequence. The initial state (p0, v0, a0) and input
# sequence (t, j) is the smallest description of a solution trajectory.
(t, j) = min_time_bvp.min_time_bvp(
    p0, v0, a0,
    p1, v1, a1,
    v_min, v_max, a_min, a_max, j_min, j_max)

# Analytically integrate the full state at the switching times. Then densely
# sample the trajectory over time for plotting purposes.
a, v, p = min_time_bvp.switch_states(p0, v0, a0, t, j)
st, sj, sa, sv, sp = min_time_bvp.sample_min_time_bvp(p0, v0, a0, t, j, dt=0.001)

# Plot the state over time.
fig, axes = plt.subplots(4, 1, sharex=True)
for i in range(sp.shape[0]):
    for ax, s, l in zip(axes, [sp, sv, sa, sj], ('pos', 'vel', 'acc', 'jerk')):
        ax.plot(st, s[i,:])
        ax.set_ylabel(l)
axes[3].set_xlabel('time')
fig.suptitle('Full State over Time')

# Show plots.
plt.show()
