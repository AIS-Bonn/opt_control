import numpy as np
import matplotlib.pyplot as plt
from py_opt_control import min_time_bvp

# Constants
v_min =  -10
v_max =   10
a_min =   -5
a_max =    5
j_min = -100
j_max =  100

# Hard coded initial and final state.
p0 = np.array([0, 2])
v0 = np.array([0, 0])
a0 = np.array([0, 0])
p1 = np.array([3, 1])
v1 = np.array([1, 0])
a1 = np.array([0, 0])

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
