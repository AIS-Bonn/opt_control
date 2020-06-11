function [J_setp_struct, solution_out, T_waypoints, P, V, A, J, t, solve_time] = bvp(p0, v0, a0, p1, v1, a1, v_min, v_max, a_min, a_max, j_min, j_max)


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

    b_comp_global    = false;
    b_sync_V         =  true(num_axes,num_trajectories);
    b_sync_A         =  true(num_axes,num_trajectories);
    b_sync_J         = false(num_axes,num_trajectories);
    b_sync_W         =  true(num_axes,num_trajectories);
    b_rotate         = false(1,num_trajectories);
    b_best_solution  =  true(num_axes,num_trajectories);
    b_hard_vel_limit = false(num_axes,num_trajectories);
    b_catch_up       =  true(num_axes,num_trajectories);
    solution_in      = -1 * ones(num_axes,2,num_trajectories,'int16');
    ts_rollout       = 0.01;


    %% ----------   Calculate    ----------
    tic;
    [J_setp_struct, solution_out, T_waypoints, P, V, A, J, t] = opt_control_lib_mex(...
        State_start, ...
        Waypoints, ...
        V_max,V_min,A_max,A_min,J_max,J_min, ...
        A_global,b_comp_global,b_sync_V,b_sync_A,b_sync_J,b_sync_W,b_rotate,b_best_solution,b_hard_vel_limit,b_catch_up,solution_in,ts_rollout);
    solve_time = toc;

end