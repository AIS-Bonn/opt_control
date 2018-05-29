% Software License Agreement (BSD License)
% Copyright (c) 2018, Computer Science Institute VI, University of Bonn
% All rights reserved.
% Redistribution and use in source and binary forms, with or without
% modification, are permitted provided that the following conditions
% are met:
% 
% * Redistributions of source code must retain the above copyright
%   notice, this list of conditions and the following disclaimer.
% * Redistributions in binary form must reproduce the above
%   copyright notice, this list of conditions and the following
%   disclaimer in the documentation and/or other materials provided
%   with the distribution.
% * Neither the name of University of Bonn, Computer Science Institute
%   VI nor the names of its contributors may be used to endorse or
%   promote products derived from this software without specific
%   prior written permission.
% 
% THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
% "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
% LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
% FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
% COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
% INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
% BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
% LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
% CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
% LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
% ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
% POSSIBILITY OF SUCH DAMAGE.

function [J_setp_struct,solution_out,T_waypoints,T_viapoints] = opt_control(State_start,Waypoints,V_max_in,V_min_in,A_max_in,A_min_in,J_max_in,J_min_in,A_wind,b_compensate_wind,b_sync_V_in,b_sync_A_in,b_sync_W_in,b_coll_prev_in,b_rotate_in,b_best_solution_in,b_hard_vel_limit_in,b_catch_up,Obstacles,MAV_d,MAV_margin,axis_penalty,solution_in) %#codegen                                                            
    coder.extrinsic('num2str');
    
    num_axes = size(Waypoints,1);
    num_trajectories = size(Waypoints,3);
    
    opt_control_check_inputs(State_start,Waypoints,V_max_in,V_min_in,A_max_in,A_min_in,J_max_in,J_min_in,A_wind,b_compensate_wind,b_sync_V_in,b_sync_A_in,b_sync_W_in,b_coll_prev_in,b_rotate_in,b_best_solution_in,Obstacles,MAV_d,MAV_margin,axis_penalty,b_hard_vel_limit_in,b_catch_up,solution_in);
    
    if (b_compensate_wind == true)
        [State_start,A_max_in,A_min_in] = compensate_wind(State_start,A_wind,A_max_in,A_min_in);
    end
    
    solution_out = solution_in;
    
    T_viapoints = [];
    T_waypoints = zeros(num_axes,num_trajectories);
    
    t_setp = cell(num_axes,num_trajectories);
    J_setp = cell(num_axes,num_trajectories);
    
    
    Waypoints = cat(3,cat(2,State_start,zeros(num_axes,2)),Waypoints);    

    for index_trajectory = 1:num_trajectories
        
        % Evolve
        T_old = max(sum(T_waypoints(:,1:index_trajectory),2));
        Obstacles_evolved = evolve_obstacles(Obstacles,T_old);
        Waypoints_evolved = evolve_waypoints(Waypoints,T_old);

        % Assign Input Variables
        P_init  = Waypoints_evolved(:,1,index_trajectory);
        V_init  = Waypoints_evolved(:,2,index_trajectory);
        A_init  = Waypoints_evolved(:,3,index_trajectory);
        VP_init = Waypoints_evolved(:,4,index_trajectory);
        AP_init = Waypoints_evolved(:,5,index_trajectory);
        
        P_wayp  = Waypoints_evolved(:,1,index_trajectory+1);
        V_wayp  = Waypoints_evolved(:,2,index_trajectory+1);
        A_wayp  = Waypoints_evolved(:,3,index_trajectory+1);
        VP_wayp = Waypoints_evolved(:,4,index_trajectory+1);
        AP_wayp = Waypoints_evolved(:,5,index_trajectory+1);
        
        V_max = V_max_in(:,index_trajectory);
        V_min = V_min_in(:,index_trajectory);
        A_max = A_max_in(:,index_trajectory);
        A_min = A_min_in(:,index_trajectory);
        J_max = J_max_in(:,index_trajectory);
        J_min = J_min_in(:,index_trajectory);
        
        b_sync_V         = b_sync_V_in(:,index_trajectory);
        b_sync_A         = b_sync_A_in(:,index_trajectory);
        b_sync_W         = b_sync_W_in(:,index_trajectory);
        b_coll_prev      = b_coll_prev_in(:,index_trajectory);
        b_rotate         = b_rotate_in(1,index_trajectory);

        b_best_solution  = b_best_solution_in(:,index_trajectory);
        b_hard_vel_limit = b_hard_vel_limit_in(:,index_trajectory);
        
        solution_trajectory = solution_in(:,:,index_trajectory);

  
        % Display Trajectory Information
        b_debug = false;
        if (b_debug == true)
            disp('-------------------');
            disp(['P_init = ', num2str(P_init','% .1f'),' m, ','V_init = ',num2str(V_init','% .1f'),' m/s, ','A_init = ',num2str(A_init','% .1f'),' m/s^2']);
            disp(['P_wayp = ', num2str(P_wayp','% .1f'),' m, ','V_wayp = ',num2str(V_wayp','% .1f'),' m/s, ','A_wayp = ',num2str(A_wayp','% .1f'),' m/s^2']);
            disp(['V_max = ',  num2str(V_max','% .1f'),' m/s, ','A_max = ',num2str(A_max','% .1f'),' m/s^2, ','J_max = ',num2str(J_max','% .1f'),' m/s^3']);
            disp(['V_min = ',  num2str(V_min','% .1f'),' m/s, ','A_min = ',num2str(A_min','% .1f'),' m/s^2, ','J_min = ',num2str(J_min','% .1f'),' m/s^3']);
            disp(['VP_init = ',num2str(VP_init','% .1f'),' m/s, ','AP_wayp = ',num2str(AP_init','% .1f'),' m/s^2\n']);
            disp(['VP_wayp = ',num2str(VP_wayp','% .1f'),' m/s, ','AP_wayp = ',num2str(AP_wayp','% .1f'),' m/s^2\n']);
            disp('-------------------');
        end


        % Prediction
        Obstacles_pred = predict_obstacles(Obstacles_evolved,P_wayp,VP_wayp,AP_wayp);
        [P_init_pred,V_init_pred,A_init_pred,P_wayp_pred,V_wayp_pred,A_wayp_pred,V_max_pred,V_min_pred,A_max_pred,A_min_pred] = predict_state(P_init,V_init,A_init,P_wayp,V_wayp,A_wayp,VP_wayp,AP_wayp,V_max,V_min,A_max,A_min);

        
        % Rotation
        if (b_rotate == true)
            alpha = atan2((P_wayp_pred(2) - P_init_pred(2)),(P_wayp_pred(1) - P_init_pred(1)));
            P_init_pred = rotate_state(alpha,P_init_pred);
            V_init_pred = rotate_state(alpha,V_init_pred);
            A_init_pred = rotate_state(alpha,A_init_pred);
            P_wayp_pred = rotate_state(alpha,P_wayp_pred);
            V_wayp_pred = rotate_state(alpha,V_wayp_pred);
            A_wayp_pred = rotate_state(alpha,A_wayp_pred);
        else
            alpha = 0;
        end
        
        
        % Catch up
        if (b_catch_up == true)
            T_catch_up = max(sum(T_waypoints(:,1:index_trajectory-1),2))-sum(T_waypoints(:,1:index_trajectory-1),2);
        else
            T_catch_up = zeros(num_axes,1);
        end
        
        
        % Generate Trajectory
        [t,J,solution_out(:,:,index_trajectory),T_viapoints] = synchronize_trajectory(P_init_pred,V_init_pred,A_init_pred,P_wayp_pred,V_wayp_pred,A_wayp_pred,V_max_pred,V_min_pred,A_max_pred,A_min_pred,J_max,J_min,b_sync_V,b_sync_A,b_sync_W,b_coll_prev,b_best_solution,Obstacles_pred,MAV_d,MAV_margin,axis_penalty,b_hard_vel_limit,T_catch_up,solution_trajectory);

        
        % Rotation
        if (b_rotate == true)
            [t,J] = rotate_jerk(alpha,t,J);
        end
        
        % Assign Output Variables
        for index_axis = 1:num_axes
            t_setp{index_axis,index_trajectory} = t{index_axis};
            J_setp{index_axis,index_trajectory} = J{index_axis};
            T_waypoints(index_axis,index_trajectory) = sum(t{index_axis});
        end
        
    end
    J_setp_struct = construct_setp_struct(t_setp,J_setp);
end



