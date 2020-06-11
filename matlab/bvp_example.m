p0 = [-1, 0 , 1];
v0 = [10, 1, -1];
a0 = [1, -1, 0];
p1 = [-2, 4 , 6];
v1 = [1, -1, 0];
a1 = [0, 1, -1];

p0 = [0, 0 , 0];
v0 = [0, 0, 0];
a0 = [0, 0, 0];
p1 = [1, 2 , -1];
v1 = [0, 0, 0];
a1 = [0, 0, 0];

v_min = -10 * ones(1,3);
v_max = 10 * ones(1,3);
a_min = -5 * ones(1,3);
a_max = 5 * ones(1,3);
j_min = -1 * ones(1,3);
j_max = 1 * ones(1,3);

[J_setp_struct, solution_out, T_waypoints, P, V, A, J, t, solve_time] = bvp(p0, v0, a0, p1, v1, a1, v_min, v_max, a_min, a_max, j_min, j_max);

T_rollout = max(sum(T_waypoints,2));

%% Everything below is for plotting.
num_axes         = numel(p0);
num_trajectories = 1;

z = zeros(1,num_axes);
State_start      = [p0; v0; a0]';
Waypoints(:,:,1) = [p1; v1; a1; z; z]';

V_max            = v_max';
V_min            = v_min';
A_max            = a_max';
A_min            = a_min';
J_max            = j_max';
J_min            = j_min';
A_global         = zeros(num_axes, num_trajectories);

show_trajectory_1D;