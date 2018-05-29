function [P,V,A,J] = rollout(P_init,V_init,A_init,J_setp_struct,T,ts) %#codegen

    num_axes = size(J_setp_struct,2);
   
    iterations = round(T/ts);       %induces small rounding error
    
    P.time = 0:ts:ts*iterations;
    V.time = 0:ts:ts*iterations;
    A.time = 0:ts:ts*iterations;
    J.time = 0:ts:ts*iterations;
     
    P.signals.values = zeros(iterations+1,1);
    V.signals.values = zeros(iterations+1,1);
    A.signals.values = zeros(iterations+1,1);
    J.signals.values = zeros(iterations+1,1);
        
    P = repmat(P,1,num_axes);
    V = repmat(V,1,num_axes);
    A = repmat(A,1,num_axes);
    J = repmat(J,1,num_axes);
    
    for index_axis = 1:num_axes
        for index = 0:1:iterations
            t_rollout = index * ts;
            [P(index_axis).signals.values(index+1,1),V(index_axis).signals.values(index+1,1),A(index_axis).signals.values(index+1,1),J(index_axis).signals.values(index+1,1)] = evaluate_to_time(P_init(index_axis),V_init(index_axis),A_init(index_axis),J_setp_struct(index_axis),t_rollout);
        end
        
    end       
        
end