function Waypoints_evolved = evolve_waypoints(Waypoints,T) %#codegen

    Waypoints_evolved = Waypoints;

    Waypoints_evolved(:,1,:) = Waypoints(:,1,:) + Waypoints(:,4,:) * T + 1/2 * Waypoints(:,5,:) * T^2;
    Waypoints_evolved(:,2,:) = Waypoints(:,2,:) + Waypoints(:,4,:) + 1/2 * Waypoints(:,5,:) * T;
    Waypoints_evolved(:,4,:) = Waypoints(:,4,:) + Waypoints(:,5,:) * T;


end