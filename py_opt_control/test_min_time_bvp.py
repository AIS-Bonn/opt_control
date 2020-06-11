import numpy as np
import matplotlib.pyplot as plt
import min_time_bvp

# p0 = np.array([0, 1, 0], dtype=np.float64)
# v0 = np.array([0, 1, -2], dtype=np.float64)
# a0 = np.array([0, 0, 0], dtype=np.float64)
# p1 = np.array([1, 3, 1], dtype=np.float64)
# v1 = np.array([0, 1, 1], dtype=np.float64)
# a1 = np.array([0, 0, 0], dtype=np.float64)

p0 = np.array([0, 0, 0], dtype=np.float64)
v0 = np.array([0, 0, 0], dtype=np.float64)
a0 = np.array([0, 0, 0], dtype=np.float64)
p1 = np.array([1, 2, -1], dtype=np.float64)
v1 = np.array([0, 0, 0], dtype=np.float64)
a1 = np.array([0, 0, 0], dtype=np.float64)

v_min = -10
v_max = 10
a_min = -5
a_max = 5
j_min = -1
j_max = 1

(t, j) = min_time_bvp.min_time_bvp(
    p0, v0, a0,
    p1, v1, a1,
    v_min, v_max, a_min, a_max, j_min, j_max)

print(t)
print(j)
