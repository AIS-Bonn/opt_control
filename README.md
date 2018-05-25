
# opt_control - Time-optimal Trajectory Generation and Control
**opt_control** generates time-optimal third order trajectories with constant jerk, resulting in bang-singular-bang trajectories.
The trajectories respect per-axis constraints on minimum and maximum velocity, acceleration and jerk.
Individual axes can be coupled by synchronizing the total time of the each trajectory.
Since the method is very fast (<<1ms), it can be used in closed loop even for fast systems.
With the ability to predict the target state, trajectories end in an optimal interception point when the waypoint is non-stationary.
It has been successfully used on different micro aerial vehicles, in different research projects and robotic competitions.


# Papers describing the Approach
Marius Beul and Sven Behnke: [Fast Full State Trajectory Generation for Multirotors](http://ais.uni-bonn.de/papers/ICUAS_2017_Beul_Trajectory_Generation.pdf)  
In Proceedings of International Conference on Unmanned Aircraft Systems (ICUAS), Miami, FL, USA, June 2017

Marius Beul and Sven Behnke: [Analytical Time-optimal Trajectory Generation and Control for Multirotors](http://ais.uni-bonn.de/papers/ICUAS_2016_Beul.pdf)  
In Proceedings of International Conference on Unmanned Aircraft Systems (ICUAS), Arlington, VA, USA, June 2016



# Getting started
run `opt_control_example` in MATLAB.
The variable `index_example` selects the example.

- example 1 generates a predefined trajectory with two consecutive waypoints for a single axis.  
- example 2 generates a predefined trajectory with two consecutive waypoints for a single axis with changing bounds and infeasible start state for the second waypoint.  
- example 3 generates a predefined trajectory with two consecutive waypoints for two axes.  
- example 4 generates a random trajectory with up to five consecutive waypoints for up to five axes.


# Meaning of variables and size of matrices

Given that the trajectory consists of m axes and n consecutive waypoints, the variables have the following size:


| Variable         | Type   | Size        |
|------------------|--------|-------------|
| State_start      | double | (m x 3)     |
| Waypoints        | double | (m x 5 x n) |
| V_max            | double | (m x n)     |
| V_min            | double | (m x n)     |
| A_max            | double | (m x n)     |
| A_min            | double | (m x n)     |
| J_max            | double | (m x n)     |
| J_min            | double | (m x n)     |
| A_global         | double | (m x 1)     |
| b_comp_global    | bool   | (1 x 1)     |
| b_sync_V         | bool   | (m x n)     |
| b_sync_A         | bool   | (m x n)     |
| b_sync_W         | bool   | (m x n)     |
| b_rotate         | bool   | (1 x n)     |
| b_best_solution  | bool   | (m x n)     |
| b_hard_vel_limit | bool   | (m x n)     |
| b_catch_up       | bool   | (m x n)     |
| solution_in      | double | (m x 2 x n) |
|                  |        |             |
| J_setp_struct    | struct | (m x 1)     |
| solution_out     | double | (m x 2 x n) |
| T_waypoints      | double | (m x n)     |


### State_start
Start state of the whole trajectory. The state consist of position, velocity and acceleration per axis

### Waypoints
List of waypoints the trajectory has to cross. Each waypoint is 5-dimensional, consisting of position, velocity, acceleration, velocity prediction, and acceleration prediction (not functional) per axis.
The velocity prediction variable describes the motion of the waypoint. This enables the method to generate interception trajectories. Velocity and acceleration variables are waypoint-centric. This means, if a waypoint is moving, the allocentric velocity in the waypoint is waypoint velocity + waypoint velocity prediction.

### V_max
Maximum velocity.

### V_min
Minimum velocity.

### A_max
Maximum acceleration.

### A_min
Minimum acceleration.

### J_max
Maximum jerk.

### J_min
Minimum jerk.

### A_global
Global acceleration. This can be for example constant sidewind when controlling an MAV.

### b_comp_global
Should global acceleration be compensated?

### b_sync_V
Should the velocity of faster axes be reduced to synchronize with the slowest axis. When both, b_sync_V and b_sync_A are switched on (and b_sync_W switched off), the trajectory with the smallest deviation from the time-optimal trajectory is chosen.

### b_sync_A
Should the acceleration of faster axes be reduced to synchronize with the slowest axis? When both, b_sync_V and b_sync_A are switched on (and b_sync_W switched off), the trajectory with the smallest deviation from the time-optimal trajectory is chosen.

### b_sync_W
Should all axes be synchronized by waiting? This means that faster axes wait before starting or after finishing at the waypoint for the slowest axis. This only works when waypoint velocity and acceleration is zero of either the start- or target waypoint. This setting superceeds b_sync_V and b_sync_A, since it is computationally much cheaper. So when b_sync_W is true, the settings of b_sync_V and b_sync_A are ignored and it is synchronized by waiting.

### b_rotate
Rotate the axes so that the x-axis points into the direction of movement between waypoints. This only makes sense with more than one axis. Considering a 3-dimensional trajectory (x,y,z), the coordinate system is rotated about the z-axis.


### b_best_solution
Should the best solution be returned? See _solution_in_ for details.

### b_hard_vel_limit
This only affects trajectories that start in an infeasible (outside of allowed velocity or acceleration margins) state. If the start velocity is infeasible, should we return to the allowed bounds as fast as possible (b_hard_vel_limit ==  true) resulting in the shortest possible time outside the limits, or is it allowed to stay outside a little longer for shortest total time and a smoother trajectory. See also example 2.

### b_catch_up
Should later synchronized axes try to catch up with unsynchronized previous axes? So, should they catch up in time to synchronize again?

### solution_in
Each trajectory connecting two waypoints for a single axis can be one of 24 cases (time-optimal) and one of 28 cases (synchronized). If _b_best_solution_ is set to false, not all cases are tried to find a solution for the problem, but when a solution is found, return. If you know the case beforehand (e.g. from a previous run with similar waypoints), you can provide the initial case here. If the case is not suitable for the problem however, the method will try the other cases until it finds a solution. Set _solution_in_ to -1 if you have no clue about the possible case.

### J_setp_struct
This variable outputs the switching times of the trajectory with the corresponding jerks. This is why we do all the math...!

### solution_out
This encodes the case of the time-optimal and synchronized trajectories.

### T_waypoints
This variable gives the incremental times between waypoints for each axis.


# License

**opt_control** is licensed under the BSD 3-clause license.

# Contact

```
Marius Beul <mbeul@ais.uni-bonn.de>
Institute of Computer Science VI
Rheinische Friedrich-Wilhelms-Universität Bonn
Endenicher Allee 19a
53115 Bonn
```
