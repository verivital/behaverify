-- LTLSPEC G (var_battery_low_warning -> (surface_task.active | surface_task_1.active | surface_task_2.active | surface_task_3.active | surface_task_4.active)); -- false
-- LTLSPEC G (var_battery_low_warning_stage_1 -> (surface_task.active | surface_task_1.active | surface_task_2.active | surface_task_3.active | surface_task_4.active)); -- true
-- LTLSPEC G (count(surface_task.active | surface_task_1.active | surface_task_2.active | surface_task_3.active | surface_task_4.active) < 2); -- true
-- LTLSPEC G (speed_max_task.active -> (!(speed_min_task.active) & !(speed_min_task_1.active))); -- true
-- LTLSPEC G (speed_min_task.active -> (!(speed_max_task.active) & !(speed_min_task_1.active))); -- true
-- LTLSPEC G (speed_min_task_1.active -> (!(speed_min_task.active) & !(speed_max_task.active))); -- true
-- LTLSPEC F (var_mission_idx = 4); -- false
-- LTLSPEC G (!(var_battery_low_warning_stage_1 & var_bb_geofence_warning_stage_1)); -- both can be set, this spec should be false.
-- LTLSPEC G (var_bb_geofence_warning_stage_1 -> rth_par_1.active); -- returns False (correct, but kinda slow).

LTLSPEC G (var_battery_low_warning -> G (var_battery_low_warning)); -- this is false, var_battery_low_warning can be unset


-- mission is pipetracking, obstacle avoidance triggered, prove pipetracking/waypoint is resumed?
-- intentionally break trees in order to prove these specs are actually relevant. make more .bt files in order to do this.

-- see what happens if pipe mission actually ends.

-- differentiate between failsafes that end the mission vs bad states that can be recovered from
-- mission endings probably cause the surface and we just end
-- a bad state is something like we have to avoid an obstacle. can we detect end of bad state and continue with mission as intended?


--failsafes:
-- battery_low_warning
-- sensor_failure_warning
-- emergency_stop_warning
-- home reached?????
-- obstacle_standoff_warning???
