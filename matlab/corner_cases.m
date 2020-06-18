clearvars;

%% Base parameters.

% State/Input limits are the same along every axis.
V_max_value            = 10.0;
V_min_value            = -10.0;
A_max_value            = 5;
A_min_value            = -5;
J_max_value            =  100.0;
J_min_value            = -100.0;
A_global_value         = 0;

% Options are the same along every axis.
b_comp_global_value    = false;
b_sync_V_value         = true;
b_sync_A_value         = true;
b_sync_J_value         = false;
b_sync_W_value         = false;
b_rotate_value         = false;
b_best_solution_value  = true;
b_hard_vel_limit_value = false;
b_catch_up_value       = true;

%% Boundary conditions.

index_example = 5;

switch index_example
    case 1
        State_start      = [ 0.6  0.0  0.0;
                             0.9  0.0  0.0];
        Waypoints(:,:,1) = [ 1.0  0.0  0.0  0.0  0.0;
                             1.0  0.0  0.0  0.0  0.0];
    case 2
        State_start      = [-0.6  0.9  0.0;
                             0.1 -1.0  0.0];
        Waypoints(:,:,1) = [ 1.0  1.0  0.0  0.0  0.0;
                             1.0 -1.0  0.0  0.0  0.0];
    case 3
        State_start      = [ 0.0  0.0  0.0;
                             0.8  0.0  0.0];
        Waypoints(:,:,1) = [ 1.0  0.0  0.0  0.0  0.0;
                             1.0  0.0  0.0  0.0  0.0];
    case 4
        State_start      = [ 0.9  0.2  0.9;
                             0.2  0.0  0.0];
        Waypoints(:,:,1) = [ 0.0  0.0  0.0  0.0  0.0;
                             0.0  0.0  0.0  0.0  0.0];
    case 5
        State_start      = [ 0.4  0.7  0.0;
                             1.0  1.0  0.0];
        Waypoints(:,:,1) = [ 1.0  1.0  0.0  0.0  0.0;
                             1.0 -1.0  0.0  0.0  0.0];
    otherwise
        disp('Please select a valid example!');
end

%% Replicate parameters over axes.
num_axes = size(State_start, 1);
num_trajectories = size(State_start,3);

V_max = repmat(V_max_value, num_axes, num_trajectories);
V_min = repmat(V_min_value, num_axes, num_trajectories);
A_max = repmat(A_max_value, num_axes, num_trajectories);
A_min = repmat(A_min_value, num_axes, num_trajectories);
J_max = repmat(J_max_value, num_axes, num_trajectories);
J_min = repmat(J_min_value, num_axes, num_trajectories);
A_global = repmat(A_global_value, num_axes, 1);

b_comp_global    = b_comp_global_value;
b_sync_V         = repmat(b_sync_V_value, num_axes, num_trajectories);
b_sync_A         = repmat(b_sync_A_value, num_axes, num_trajectories);
b_sync_J         = repmat(b_sync_J_value, num_axes, num_trajectories);
b_sync_W         = repmat(b_sync_W_value, num_axes, num_trajectories);
b_rotate         = repmat(b_rotate_value, 1, num_trajectories);
b_best_solution  = repmat(b_best_solution_value, num_axes,num_trajectories);
b_hard_vel_limit = repmat(b_hard_vel_limit_value, num_axes,num_trajectories);
b_catch_up       = repmat(b_catch_up_value, num_axes, num_trajectories);

solution_in      = -1 * ones(num_axes, 2, num_trajectories,'int16');
ts_rollout       = 0.001;

%% ----------   Calculate    ----------
tic;
[J_setp_struct,solution_out,T_waypoints,P,V,A,J,t] = opt_control_lib_mex(State_start,Waypoints,V_max,V_min,A_max,A_min,J_max,J_min,A_global,b_comp_global,b_sync_V,b_sync_A,b_sync_J,b_sync_W,b_rotate,b_best_solution,b_hard_vel_limit,b_catch_up,solution_in,ts_rollout);
toc;


%% ----------     Output     ----------
disp(['num_axes = ',num2str(num_axes)]);
disp(['num_trajectories = ',num2str(num_trajectories)]);
T_rollout = max(sum(T_waypoints,2));

disp('solution_out')
disp(solution_out)

% Display time and jerk events.
disp('')
for k=1:num_axes
    fprintf('axis %i\n time and jerk\n', k)
    disp([J_setp_struct(k).time, J_setp_struct(k).signals.values'])
end

show_trajectory_1D;


