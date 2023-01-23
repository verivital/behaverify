-- LTLSPEC G(var_failsafe_engaged -> (halt.active | surface.active | env_BLUEROV_SURFACED));

-- LTLSPEC G((count(halt.active, surface.active, avoid_obstacles.active, return_home.active, search_for_pipe.active, track_pipe.active, waypoint.active, loiter.active) = 1) <-> BlueROV.active);
-- LTLSPEC G((count(halt.active, surface.active, avoid_obstacles.active, return_home.active, search_for_pipe.active, track_pipe.active, waypoint.active, loiter.active) = 0) <-> !(BlueROV.active));
-- LTLSPEC G((count(halt.active, surface.active, avoid_obstacles.active, return_home.active, search_for_pipe.active, track_pipe.active, waypoint.active, loiter.active) <= 1));

-- LTLSPEC G (!(loiter.active));

-- LTLSPEC G (env_obstacles_present -> (halt.active | surface.active | avoid_obstacles.active | env_BLUEROV_SURFACED));



---------------------------------------------------------------------------------------------------------------
-- --1. Do No Harm
-- --2. Preserve UUV
-- --3. Complete Missions
---------------------------------------------------------------------------------------------------------------


-- --1. Do No Harm
-- --To ensure no harm is done, we will prioritize avoiding obstacles. Thus we either engage in obstacle avoidance or halt (or are halted) if obstacles are present.

-- LTLSPEC G ((env_obstacles_present | env_emergency_sensor) -> (halt.active | avoid_obstacles.active | env_BLUEROV_HALTED));


-- --2. Preserve UUV
-- --To ensure the UUV is safe, we first ensure we do not crash. This is covered by (1. Do No Harm). The next phase is to confirm we surface if a failsafe is triggered.

-- LTLSPEC G ((env_battery_low | env_emergency_sensor | env_sensor_failure| (env_reallocation_needed & !(env_reallocation_possible))) -> (surface.active | env_BLUEROV_SURFACED)); -- False. Halt can take precedence
-- LTLSPEC G ((env_battery_low | env_emergency_sensor | env_sensor_failure | (env_reallocation_needed & !(env_reallocation_possible))) -> (halt.active | surface.active | env_BLUEROV_SURFACED)); -- True

-- --additionally, we should surface if we've reached home

-- LTLSPEC G(((var_mission = MISSION_go_to_home) & env_home_reached) -> (halt.active | surface.active | env_BLUEROV_SURFACED));

-- --furthermore, ensure that we don't get lost going too far away

-- LTLSPEC G(env_geofence_warning -> (halt.active | surface.active | env_BLUEROV_SURFACED | avoid_obstacles.active | return_home.active));


-- --3. Complete Missions
-- --If 1 and 2 are handled, then we need to focus on 3. prove that we try and make progress on missions

-- LTLSPEC G ( !(env_BLUEROV_SURFACED | surface.active | halt.active | avoid_obstacles.active) -> ((var_mission_stage_2 = MISSION_pipe_tracking & env_command_stage_8 in {COMMAND_pipe_tracking, COMMAND_search_for_pipe}) | (var_mission_stage_2 = MISSION_go_to_waypoint & env_command_stage_8 = COMMAND_go_to_waypoint) | (var_mission_stage_2 = MISSION_go_to_home & env_command_stage_8 = COMMAND_go_to_home)));
