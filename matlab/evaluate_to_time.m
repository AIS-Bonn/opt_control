function [P,V,A,J] = evaluate_to_time(P_init,V_init,A_init,J_setp_struct,T) %#codegen

    num_axes = size(J_setp_struct,2);

    P = zeros(num_axes,1);
    V = zeros(num_axes,1);
    A = zeros(num_axes,1);
    J = zeros(num_axes,1);

    for index_axis = 1:num_axes

        if (T > J_setp_struct(index_axis).time(end))
            J_setp_struct(index_axis).time = vertcat(J_setp_struct(index_axis).time,T);
            J_setp_struct(index_axis).signals.values = horzcat(J_setp_struct(index_axis).signals.values,0);
        end

        index_setp_max = find(J_setp_struct(index_axis).time<=T,1,'last');
        
        t_remaining = cat(2,diff(J_setp_struct(index_axis).time(1:index_setp_max(1,1),1))',T - J_setp_struct(index_axis).time(index_setp_max(1,1),1));
        J_remaining = J_setp_struct(index_axis).signals.values(1,1:index_setp_max(1,1));

        [P_eval,V_eval,A_eval] = evaluate(t_remaining,J_remaining,P_init(index_axis),V_init(index_axis),A_init(index_axis));

        P(index_axis,1) = P_eval(end);
        V(index_axis,1) = V_eval(end);
        A(index_axis,1) = A_eval(end);
        J(index_axis,1) = J_remaining(end);

    end
    
end
