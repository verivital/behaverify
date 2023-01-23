LTLSPEC G(var_failsafe_engaged -> (surface.active | env_BLUEROV_SURFACED));

LTLSPEC G((count(surface.active, avoid_obstacles.active, return_home.active, search.active, track_pipe.active, waypoint.active, loiter.active) = 1) <-> BlueROV.active);
LTLSPEC G((count(surface.active, avoid_obstacles.active, return_home.active, search.active, track_pipe.active, waypoint.active, loiter.active) = 0) <-> !(BlueROV.active));
LTLSPEC G((count(surface.active, avoid_obstacles.active, return_home.active, search.active, track_pipe.active, waypoint.active, loiter.active) <= 1));

LTLSPEC G (!(loiter.active));

LTLSPEC G (env_obstacles_present -> (surface.active | avoid_obstacles.active | env_BLUEROV_SURFACED));
