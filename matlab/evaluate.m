function [P,V,A] = evaluate(t,J,P_init,V_init,A_init) %#codegen

    num_setpoints = size(t,2);
    
    P = ones(1,num_setpoints) * (P_init + t(1) * V_init + 1/2 * t(1)^2 * A_init + 1/6 * t(1)^3 * J(1));
    V = ones(1,num_setpoints) * (V_init + t(1) * A_init + 1/2 * t(1)^2 * J(1));
    A = ones(1,num_setpoints) * (A_init + t(1) * J(1));

    for index_setpoint = 2:num_setpoints
        P(index_setpoint) = polyval([1/6*J(index_setpoint) 1/2*A(index_setpoint-1) V(index_setpoint-1) P(index_setpoint-1)],t(index_setpoint));
        V(index_setpoint) = polyval([1/2*J(index_setpoint) A(index_setpoint-1) V(index_setpoint-1)],t(index_setpoint));
        A(index_setpoint) = polyval([J(index_setpoint) A(index_setpoint-1)],t(index_setpoint));
    end

end

