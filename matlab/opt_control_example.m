clearvars;
%% ----------   Variables    ----------
index_example = 5;

switch index_example
    case 1
        num_axes         = 1;
        num_trajectories = 2;
        State_start      = [ 0.0  0.0  0.0];
        Waypoints(:,:,1) = [ 2.0  0.0  0.0  0.0  0.0];
        Waypoints(:,:,2) = [ 0.0  0.0  0.0  0.0  0.0];
        V_max            = [ 1.0  1.0];
        V_min            = [-1.0 -1.0];
        A_max            = [ 0.5  0.5];
        A_min            = [-0.5 -0.5];
        J_max            = [ 1.0  1.0];
        J_min            = [-1.0 -1.0];
        A_global         =   0.0;
    case 2
        num_axes         = 1;
        num_trajectories = 2;
        State_start      = [ 0.0  0.0  0.0];
        Waypoints(:,:,1) = [ 3.0  0.5  0.0  0.0  0.0];
        Waypoints(:,:,2) = [ 4.0  0.0  0.0  0.0  0.0];
        V_max            = [ 1.0  0.2];
        V_min            = [-1.0 -1.0];
        A_max            = [ 0.5  0.5];
        A_min            = [-0.5 -0.5];
        J_max            = [ 1.0  1.0];
        J_min            = [-1.0 -1.0];
        A_global         =   0.0;
     case 3
        num_axes         = 1;
        num_trajectories = 2;
        State_start      = [ 0.0  0.0  0.0];
        Waypoints(:,:,1) = [ 2.0  0.0  0.0  0.0  0.0];
        Waypoints(:,:,2) = [ 0.0  0.0  0.0  0.0  0.0];
        V_max            = [ 1.0  1.0];
        V_min            = [-1.0 -1.0];
        A_max            = [ 0.5  0.5];
        A_min            = [-0.5 -0.5];
        J_max            = [ Inf  Inf];
        J_min            = [-Inf -Inf];
        A_global         =   0.0;
    case 4
        num_axes         = 2;
        num_trajectories = 2;
        State_start      = [ 0.0  0.0  0.0;
                             0.0  0.0  0.0];
        Waypoints(:,:,1) = [ 1.0  0.0  0.0  0.0  0.0;
                             3.0  0.0  0.0  0.0  0.0];
        Waypoints(:,:,2) = [ 0.0  0.0  0.0  0.0  0.0;
                             0.0  0.0  0.0  0.0  0.0];
        V_max            = [ 1.0  1.0;
                             1.0  1.0];
        V_min            = [-1.0 -1.0;
                            -1.0 -1.0];
        A_max            = [ 0.5  0.5;
                             0.5  0.5];
        A_min            = [-0.5 -0.5;
                            -0.5 -0.5];
        J_max            = [ 1.0  1.0;
                             1.0  1.0];
        J_min            = [-1.0 -1.0;
                            -1.0 -1.0];
        A_global         = [ 0.0;
                             0.0];
    case 5
        rng(16);
        num_axes         = randi(10);
        num_trajectories = randi(5);

        State_start      =  0.0*rand(num_axes,3);
        
        V_max            =  1.0*ones(num_axes,num_trajectories);
        V_min            = -1.0*ones(num_axes,num_trajectories);
        A_max            =  0.5*ones(num_axes,num_trajectories);
        A_min            = -0.5*ones(num_axes,num_trajectories);
        J_max            =  1.0*ones(num_axes,num_trajectories);
        J_min            = -1.0*ones(num_axes,num_trajectories);
        A_global         =  0.0*ones(num_axes,1);
        
        P_waypoint_max   =  5.0.*ones(num_axes,num_trajectories);
        P_waypoint_min   = -5.0.*ones(num_axes,num_trajectories);
        V_waypoint_max   =  0.4.*ones(num_axes,num_trajectories);
        V_waypoint_min   = -0.4.*ones(num_axes,num_trajectories);
        A_waypoint_max   =  0.3.*ones(num_axes,num_trajectories);
        A_waypoint_min   = -0.3.*ones(num_axes,num_trajectories);
        PV_waypoint_max  =  0.2.*ones(num_axes,num_trajectories);
        PV_waypoint_min  = -0.2.*ones(num_axes,num_trajectories);
        PA_waypoint_max  =  0.0.*ones(num_axes,num_trajectories);
        PA_waypoint_min  =  0.0.*ones(num_axes,num_trajectories);
        
        P_waypoints      = reshape(P_waypoint_min+(P_waypoint_max-P_waypoint_min).*rand(num_axes,num_trajectories),num_axes,1,num_trajectories);
        V_waypoints      = reshape(V_waypoint_min+(V_waypoint_max-V_waypoint_min).*rand(num_axes,num_trajectories),num_axes,1,num_trajectories);
        A_waypoints      = reshape(A_waypoint_min+(A_waypoint_max-A_waypoint_min).*rand(num_axes,num_trajectories),num_axes,1,num_trajectories);
        PV_waypoints     = reshape(PV_waypoint_min+(PV_waypoint_max-PV_waypoint_min).*rand(num_axes,num_trajectories),num_axes,1,num_trajectories);
        PA_waypoints     = reshape(PA_waypoint_min+(PA_waypoint_max-PA_waypoint_min).*rand(num_axes,num_trajectories),num_axes,1,num_trajectories);
        Waypoints        = cat(2,P_waypoints,V_waypoints,A_waypoints,PV_waypoints,PA_waypoints);
        
    otherwise
        disp('please select a valid example!');
end

b_comp_global        = false;
b_sync_V             =  true(num_axes,num_trajectories);
b_sync_A             =  true(num_axes,num_trajectories);
b_sync_W             =  true(num_axes,num_trajectories);
b_rotate             = false(1,num_trajectories);
b_best_solution      =  true(num_axes,num_trajectories);
b_hard_vel_limit     = false(num_axes,num_trajectories);
b_catch_up           =  true(num_axes,num_trajectories);

%% ----------   Calculate    ----------
solution_in       = -1 * ones(num_axes,2,num_trajectories,'int8');

tic;
[J_setp_struct,solution_out,T_waypoints,~] = opt_control_mex(State_start,Waypoints,V_max,V_min,A_max,A_min,J_max,J_min,A_global,b_comp_global,b_sync_V,b_sync_A,b_sync_W,false(num_axes,num_trajectories),b_rotate,b_best_solution,b_hard_vel_limit,b_catch_up,ones(num_axes,8,1),ones(num_axes,1),zeros(num_axes,1),zeros(num_axes,1),solution_in);                                                              
toc;



%% ----------     Output     ----------
disp(['num_axes = ',num2str(num_axes)]);
disp(['num_trajectories = ',num2str(num_trajectories)]);

ts_rollout = 0.01;
T_rollout = max(sum(T_waypoints,2));
[P,V,A,J] = rollout(State_start(:,1),State_start(:,2),State_start(:,3)+A_global*b_comp_global,J_setp_struct,T_rollout,ts_rollout);

show_trajectory_1D;





