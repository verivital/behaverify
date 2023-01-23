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


-- --when we tick, exactly one of the priorities tasks is selected. not 0, not 2.
-- LTLSPEC G (BlueROV.active -> count(surface_task.active, surface_task_1.active, surface_task_2.active, surface_task_3.active, surface_task_4.active, rth_task.active, rth_task_1.active, loiter_task.active, tracking_task.active,  loiter_task_1.active, waypoint_task.active, loiter_task_2.active) = 1); -- true, but slow

-- --multiple failsafes can be activated
-- LTLSPEC G (!(var_battery_low_warning_stage_1 & var_bb_geofence_warning_stage_1)); -- both can be set, this spec should be false.



-- --the missions eventually run out
-- LTLSPEC F (var_finished_missions_stage_1); -- this should be false.
-- --honestly, no good way to do this without a bunch of restrictions.




-- --the blueROV surfaces eventually
-- LTLSPEC F (surface_task.active | surface_task_1.active | surface_task_2.active | surface_task_3.active | surface_task_4.active); -- this should be false, because missions don't need to end


-- --the blueROV surfaces eventually if battery gets low.
-- LTLSPEC G ((F var_battery = 0) -> F var_BLUEROV_SURFACED);



-- --obstacles eventually end
-- LTLSPEC G (var_bb_obstacle_warning -> F (!(var_bb_obstacle_warning) | var_BLUEROV_SURFACED)); -- fails. there is no way to prove that obstacles will not be detected at every step


-- --obstacle avoidance task command is ordered if bb_obstacle_warning
-- LTLSPEC G (var_bb_obstacle_warning_stage_1 -> (var_cm_hsd_input_stage_1 = cm_obstacle_avoidance_task)); -- true
-- LTLSPEC G (var_bb_obstacle_warning_stage_1 -> (var_cm_hsd_input_stage_2 = cm_obstacle_avoidance_task));-- true
-- LTLSPEC G (var_bb_obstacle_warning_stage_1 -> (var_cm_hsd_input_stage_3 = cm_obstacle_avoidance_task));-- true
-- LTLSPEC G (var_bb_obstacle_warning_stage_1 -> (var_cm_hsd_input_stage_4 = cm_obstacle_avoidance_task));-- true
-- LTLSPEC G (var_bb_obstacle_warning_stage_1 -> (var_cm_hsd_input_stage_5 = cm_obstacle_avoidance_task));-- true
-- LTLSPEC G (var_bb_obstacle_warning_stage_1 -> (var_cm_hsd_input_stage_6 = cm_obstacle_avoidance_task));-- true
-- LTLSPEC G (var_bb_obstacle_warning_stage_1 -> (var_cm_hsd_input_stage_7 = cm_obstacle_avoidance_task));-- true
-- LTLSPEC G (var_bb_obstacle_warning_stage_1 -> (var_cm_hsd_input_stage_8 = cm_obstacle_avoidance_task));-- true
-- LTLSPEC G (var_bb_obstacle_warning_stage_1 -> (var_cm_hsd_input_stage_9 = cm_obstacle_avoidance_task));-- true
-- LTLSPEC G (var_bb_obstacle_warning_stage_1 -> (var_cm_hsd_input_stage_10 = cm_obstacle_avoidance_task));-- true
-- LTLSPEC G (var_bb_obstacle_warning_stage_1 -> (var_cm_hsd_input_stage_11 = cm_obstacle_avoidance_task));-- true, but slow
-- LTLSPEC G (var_bb_obstacle_warning_stage_1 -> (var_cm_hsd_input_stage_12 = cm_obstacle_avoidance_task));-- true, very slow
-- LTLSPEC G (var_bb_obstacle_warning_stage_1 -> (var_cm_hsd_input_stage_13 = cm_obstacle_avoidance_task));-- probably true, extremely slow


-- --loiter_task_1 is unreachable (it is reachable. i meant loiter task 2... lol)
-- CTLSPEC EF (loiter_task_1.active); -- True
-- LTLSPEC G (!(loiter_task_1.active)); -- False, so it's eventually active



-- --loiter_task_2 is unreachable
-- CTLSPEC EF (loiter_task_2.active); -- False now.
-- LTLSPEC G (!(loiter_task_2.active)); -- True now, formerly false. slow though. see below
-- False. It's reachable... because i had an error in the file. specifically, i assumed emergency_stop_warning would be initialized to false, which may not be true, because bb_misison can be set to e_stop at start. fixed. for now. rechekcing if reachable.


-- --surface guarantees, but in ctl
-- CTLSPEC EF(var_BLUEROV_SURFACED); -- true, it is possible to reach the surface
-- CTLSPEC AF(var_BLUEROV_SURFACED); -- false, you are not guaranteed to reach the surface




------------------------------------------------------------
--specifications from contingency manager.
-- prioritize 1. do no harm, 2. keep the UUV safe, 3. completing the mission.


-- --1. do no harm
-- --this specification is TRUE if surfacing is safe and will not do harm. proof: obstacle avoidance always takes priority, but sometimes surfacing can interrupt.
-- --this specification is FALSE if surfacing is NOT always safe.
-- --for the true version, refer back to prior specifications which prove tht if  failsafe is set, we surface, and that if bb_obstacle_warning is set, we do obstacle avoidance
-- --for the false version, use the following specification to prove a violation
-- LTLSPEC G(var_bb_obstacle_warning_stage_1 -> !(emergency_stop_task.active)); -- FALSE. it is possible for obstacle avoidance ot be going, and emergency_stop_task to occur, which overwrites everthing else
-- --CTL version
-- CTLSPEC EF(var_bb_obstacle_warning_stage_1 & emergency_stop_task.active); -- TRUE. it is possible blah blah.

-- --2. keep the UUV safe
-- --exactly the same as specification 1. unclear on the difference to be honest.


-- --3. completing the mission
-- --impossible to show that the mission will be completed without asserting the mission is completed, or using a fairness constraint to do the same thing.
-- --however, we can show that if failsafes are not triggered and there is no obstacle avoidance, then we do our mission.

-- LTLSPEC G ((BlueROV.active & !(surface_task.active | surface_task_1.active | surface_task_2.active | surface_task_3.active | surface_task_4.active)) -> (var_bb_mission_stage_1 = waypoint_following & (loiter_task_1.active | waypoint_task.active)) | (var_bb_mission_stage_1 = pipe_following & tracking_task.active)); --FALSE. return to home might be triggered.
-- LTLSPEC G ((BlueROV.active & !(surface_task.active | surface_task_1.active | surface_task_2.active | surface_task_3.active | surface_task_4.active | rth_task.active | rth_task_1.active)) -> (var_bb_mission_stage_1 = waypoint_following & (loiter_task_1.active | waypoint_task.active)) | (var_bb_mission_stage_1 = pipe_following & (tracking_task.active | loiter_task.active)));  --TRUE. but this is very sketchy. Specifically, this is ONLY true because pipe_following cannot end. The issue i see with the currrent layout is that pipe_lost_warning is set BEFORE the mission is updated. Thus, if pipe_tracking could end, the following scenario could take place.
-- --tick 1. mission is pipe_tracking. mission ends.
-- --tick 2. pipe_lost_warning is set to true. mission is set to waypoint_following. tree executes loiter_task because pipe_lost_warning is set to true
-- --tick 3+. tree continues to execute loiter_task. it is not possible to unset this. eventually, battery runs out, and bluerov surfaces.
-- --the below version slightly more complete.
-- LTLSPEC G ((BlueROV.active & !(surface_task.active | surface_task_1.active | surface_task_2.active | surface_task_3.active | surface_task_4.active | rth_task.active | rth_task_1.active)) -> (var_bb_mission_stage_1 = waypoint_following & var_cm_hsd_input_stage_13 = cm_waypoint_task) | (var_bb_mission_stage_1 = pipe_following & var_cm_hsd_input_stage_13 = cm_tracking_task) | (var_cm_hsd_input_stage_13 = cm_obstacle_avoidance_task) | var_cm_hsd_input_stage_13 = cm_loiter_task);  --TRUE.


