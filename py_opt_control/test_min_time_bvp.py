import numpy as np
import matplotlib.pyplot as plt
import min_time_bvp

# Constants
v_min = -10
v_max = 10
a_min = -5
a_max = 5
j_min = -100
j_max = 100




# Time series plot of full state.
p0 = np.array([0, 0.5, 0], dtype=np.float64)
v0 = np.array([0, 0, 0], dtype=np.float64)
a0 = np.array([0, 0, 0], dtype=np.float64)

p1 = np.array([1, 2, -1], dtype=np.float64)
v1 = np.array([0, 0, 0], dtype=np.float64)
a1 = np.array([0, 0, 0], dtype=np.float64)

(t, j) = min_time_bvp.min_time_bvp(
    p0, v0, a0,
    p1, v1, a1,
    v_min, v_max, a_min, a_max, j_min, j_max)
a, v, p = min_time_bvp.switch_states(p0, v0, a0, t, j)
st, sj, sa, sv, sp = min_time_bvp.sample_min_time_bvp(p0, v0, a0, t, j, dt=0.001)

fig, axes = plt.subplots(4, 1, sharex=True)
for i in range(sp.shape[0]):
    for ax, s, l in zip(axes, [sp, sv, sa, sj], ('pos', 'vel', 'acc', 'jerk')):
        ax.plot(st, s[i,:])
        ax.set_ylabel(l)
axes[3].set_xlabel('time')
fig.suptitle('Full State over Time')




# Many motions to stop at (1,1,1)
N = 100
p0 = np.random.uniform(-1, 1, (N,3))
v0_master = np.random.uniform(-1, 1, (N,3))
a0_master = np.random.uniform(-1, 1, (N,3))

p1 = np.array([1, 1, 1], dtype=np.float64)
v1 = np.array([0, 0, 0], dtype=np.float64)
a1 = np.array([0, 0, 0], dtype=np.float64)

fig, axes = plt.subplots(2, 2)
axes = axes.flatten()
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
            print('\nFailed.')
            print(p0[i])
            print(v0[i])
            print(a0[i])

        axes[jj].plot(sp[0,:], sp[1,:])
    axes[jj].set_xlim((-0.2, 1.2))
    axes[jj].set_ylim((-0.2, 1.2))
    axes[jj].axis('equal')
fig.suptitle('Motions to stop at (1,1,1)')


# Show plots.
plt.show()
