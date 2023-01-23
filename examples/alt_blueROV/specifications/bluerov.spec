-- mission is pipetracking, obstacle avoidance triggered, prove pipetracking/waypoint is resumed?
-- the mission isn't really suspended by obstacle avoidance.....

-- intentionally break trees in order to prove these specs are actually relevant. make more .bt files in order to do this.

-- see what happens if pipe mission actually ends. NO WAY TO DO THIS.
-- the only way to set a new mission is if waypoint_mission completes.

-- differentiate between failsafes that end the mission vs bad states that can be recovered from
-- mission endings probably cause the surface and we just end
-- a bad state is something like we have to avoid an obstacle. can we detect end of bad state and continue with mission as intended?


--failsafes:
-- battery_low_warning
-- sensor_failure_warning
-- emergency_stop_warning
-- home reached?????
-- obstacle_standoff_warning???

-- --battery failsafe always results in a surface task
-- LTLSPEC G (var_battery_low_warning_stage_1 -> (surface_task.active | surface_task_1.active | surface_task_2.active | surface_task_3.active | surface_task_4.active)); -- true
-- --battery failsafe is pernament
-- LTLSPEC G (var_battery_low_warning_stage_1 -> G (var_battery_low_warning_stage_1)); -- this is false, var_battery_low_warning can be unset

-- --sensor failsafe always results in a surface task
-- LTLSPEC G (var_bb_sensor_failure_warning_stage_1 -> (surface_task.active | surface_task_1.active | surface_task_2.active | surface_task_3.active | surface_task_4.active)); -- true
-- --sensor failsafe is pernament
-- LTLSPEC G (var_bb_sensor_failure_warning_stage_1 -> G (var_bb_sensor_failure_warning_stage_1)); -- true, it's pernament

-- --emergency failsafe always results in a surface task
-- LTLSPEC G (var_emergency_stop_warning_stage_1 -> (surface_task.active | surface_task_1.active | surface_task_2.active | surface_task_3.active | surface_task_4.active)); -- true
-- --emergency failsafe is pernament
-- LTLSPEC G (var_emergency_stop_warning_stage_1 -> G (var_emergency_stop_warning_stage_1)); -- true, it's pernament

-- --home_reached always results in a surface task
-- LTLSPEC G (var_bb_home_reached_stage_1 -> (surface_task.active | surface_task_1.active | surface_task_2.active | surface_task_3.active | surface_task_4.active)); -- false
-- LTLSPEC G (var_bb_home_reached_stage_1 -> X(surface_task.active | surface_task_1.active | surface_task_2.active | surface_task_3.active | surface_task_4.active)); -- true
-- --home_reached is pernament
-- LTLSPEC G (var_bb_home_reached_stage_1 -> G (var_bb_home_reached_stage_1)); -- true, it's pernament

-- --obstacle_standoff always results in a surface task
-- LTLSPEC G (var_obstacle_standoff_warning_stage_1 -> (surface_task.active | surface_task_1.active | surface_task_2.active | surface_task_3.active | surface_task_4.active)); -- true
-- --obstacle_standoff is pernament
-- LTLSPEC G (var_obstacle_standoff_warning_stage_1 -> G (var_obstacle_standoff_warning_stage_1)); -- this is false, var_obstacle_standoff_warning can be unset



-- --surface task cannot be entered multiple times during a single tick
-- LTLSPEC G (count(surface_task.active, surface_task_1.active, surface_task_2.active, surface_task_3.active, surface_task_4.active) < 2); -- true

-- --speed_min is only set once and speed_min and max are mutually exclusive
-- LTLSPEC G (speed_max_task.active -> (!(speed_min_task.active) & !(speed_min_task_1.active))); -- true
-- LTLSPEC G (speed_min_task.active -> (!(speed_max_task.active) & !(speed_min_task_1.active))); -- true
-- LTLSPEC G (speed_min_task_1.active -> (!(speed_min_task.active) & !(speed_max_task.active))); -- true

-- --multiple failsafes can be activated
-- LTLSPEC G (!(var_battery_low_warning_stage_1 & var_bb_geofence_warning_stage_1)); -- both can be set, this spec should be false.



-- --the missions eventually run out
-- LTLSPEC F (var_finished_missions_stage_1); -- this should be false.
-- --honestly, no good way to do this without a bunch of restrictions.




-- --the blueROV surfaces eventually
-- LTLSPEC F (surface_task.active | surface_task_1.active | surface_task_2.active | surface_task_3.active | surface_task_4.active); -- this should be false, because missions don't need to end
