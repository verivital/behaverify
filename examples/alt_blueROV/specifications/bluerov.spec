---------------------------------------------------------------------------------------------------------------
-- --1. Do No Harm
-- --2. Preserve UUV
-- --3. Complete Missions
---------------------------------------------------------------------------------------------------------------

-- --1. Do No Harm
-- --To ensure no harm is done, we will prioritize avoiding obstacles. Thus we either engage in obstacle avoidance or halt (or are halted) if obstacles are present.

-- LTLSPEC G(var_bb_fls_warning_stage_1 -> (var_BLUEROV_SURFACED | (emergency_stop_task.active & var_cm_hsd_input_stage_8 = cm_surface_task))); -- TRUE
-- --This specification confirms that if the FLS warning is set to true, then one of the following is true
-- --1. We have already surfaced and are done
-- --2. We executed the emergecny_stop_task and the command sent to the blueROV is surface

-- LTLSPEC G((!(var_bb_fls_warning_stage_1) & !(var_bb_mission_stage_1 = e_stop) & (var_bb_obstacle_warning_stage_1)) -> (var_BLUEROV_SURFACED | var_cm_hsd_input_stage_8 = cm_obstacle_avoidance_task)); -- TRUE
-- --This specification confirms that if the FLS warning is NOT set to true and we are not executing an e_stop mission, then one of the following is true
-- --1. We have already surfaced and are done
-- --2. The commmand sent to the blueROV is obstacle avoidance

-- --between these two specifications we have handled avoiding obstacles. if we cannot go around the obstacle (FLS warning true), then we attempt to stop. If we can go around and are not stopping for some other reason, then we do so.



-- --2. Preserve UUV
-- --Preservation of the UUV consists of two factors. The first is not crashing into things. Fortunately, this is handled by objective [1. Do No Harm]. Therefore, we are now only interested in the second aspect: ensuring that we surface if a failsafe is set and that the UUV is not lost underwater.


-- LTLSPEC G((!(var_bb_obstacle_warning_stage_1) & (var_emergency_stop_warning_stage_2 | var_battery_low_warning_stage_1 | var_bb_sensor_failure_warning_stage_1 | var_obstacle_standoff_warning_stage_1)) -> (var_BLUEROV_SURFACED | var_cm_hsd_input_stage_8 = cm_surface_task)); -- TRUE
-- --This specification confirms that if we're not doing basic obstacle avoidance, then any failsafe being triggered (emergency_stop_warning, battery_low_warning, sensor_failure_warning, obstacle_standoff_warning) mean one of the following are true
-- --1. We have already surfaced and are done
-- --2. The command sent to the blueROV is surface


-- LTLSPEC G((!(var_bb_obstacle_warning_stage_1) & ((var_bb_rth_warning_stage_2 | var_bb_geofence_stage_1) & var_bb_home_reached_stage_1)) -> (var_BLUEROV_SURFACED | var_cm_hsd_input_stage_8 = cm_surface_task)); -- TRUE
-- --This specification confirms that if we're not doing basic obstacle avoidance, then if we were returning home and have reached home, one of the following are true
-- --1. We have already surfaced and are done
-- --2. The command sent to the blueROV is surface


-- LTLSPEC G((!(var_bb_obstacle_warning_stage_1) & ((var_bb_rth_warning_stage_2 | var_bb_geofence_stage_1) & !(var_cm_hsd_input_stage_8 = cm_surface_task))) -> (var_BLUEROV_SURFACED | var_cm_hsd_input_stage_8 = cm_rth_task)); -- TRUE
-- --This specification confirms that if we're not doing basic obstacle avoidance and we are not issuing the surface command, then if either geofence_warning or rth_warning have been set, one of the following are true
-- --1. We have already surfaced and are done
-- --2. The command sent to the blueROV is rth (return to home)

-- --Between these three specifications, we have confirmed that if we're not doing obstacle avoidance then failsafes will cause us to surface, reaching home will cause us to surface, and exceeding the geofence or getting an RTH from some other source will cause us to attempt to return to home (and if we reach home we will surface by the 2nd specification).
-- --This confirms that the UUV will attempt to preserve itself if it is not prioritizing [1. Do No Harm].



-- --3. Complete Missions
-- --Finally, if we possible, we would like to focus on completing missions. The two mission types are pipe_tracking and waypoint_following


-- LTLSPEC G((!(var_cm_hsd_input_stage_8 in {cm_surface_task, cm_rth_task, cm_obstacle_avoidance_task})) -> (var_BLUEROV_SURFACED | var_cm_hsd_input_stage_8 in {cm_loiter_task, cm_tracking_task, cm_waypoint_task})); --TRUE
-- --This specification confirms that if we are not busy with surfacing, returning to home, or avoiding obstacles, then one of the following is true
-- --1. We have already surfaced and are done
-- --2. The command sent is mission related.
-- --While this specification is true, it's also trivially true....because the full domain for cm_hsd_input is {cm_surface_task, cm_rth_task, cm_obstacle_avoidance_task} UNION {cm_loiter_task, cm_tracking_task, cm_waypoint_task}...so by excluding the first half in the assertion, the implication is trivially true. In fact, we can even remove var_BLUEROV_SURFACED.
-- LTLSPEC G((!(var_cm_hsd_input_stage_8 in {cm_surface_task, cm_rth_task, cm_obstacle_avoidance_task})) -> (var_cm_hsd_input_stage_8 in {cm_loiter_task, cm_tracking_task, cm_waypoint_task})); --TRUE
-- --The specification still holds. Let us move to more interesting mission statements.

-- LTLSPEC G((!(var_cm_hsd_input_stage_8 in {cm_surface_task, cm_rth_task, cm_obstacle_avoidance_task})) -> (var_BLUEROV_SURFACED | (var_bb_mission_stage_1 = pipe_following & var_bb_pipe_lost_warning_stage_1 & var_cm_hsd_input_stage_8 = cm_loiter_task) | (var_bb_mission_stage_1 = pipe_following & !(var_bb_pipe_lost_warning_stage_1) & var_cm_hsd_input_stage_8 = cm_tracking_task) | (var_bb_mission_stage_1 = waypoint_following & var_cm_hsd_input_stage_8 = cm_waypoint_task))); --TRUE
-- --This specification confirms that if we are not busy with surfacing, returning to home, or avoiding obstacles, then one of the following is true
-- --1. We have already surfaced and are done
-- --2. Our mission is follow a pipe and we have lost the pipe, so we are loitering until it reappears
-- --3. Our mission is follow a pipe and we have not lost the pipe, so we are following the pipe
-- --4. Our mission is go to a waypoint and we are going to a waypoint


-- --Thus, if we are not busy with [1. Do No Harm] or [2. Preserve UUV], we will be doing out best to [3. Complete Missions].


------------------------------------------------------------------------------------------------------------------
-- --Misc Tree makes sense checks

--Speed min and speed_max are mutually exclusive
LTLSPEC G(speed_min_task.active -> !speed_max_task.active);
LTLSPEC G(speed_max_task.active -> !speed_min_task.active);


--The last loiter task is included, but can never be reached.
LTLSPEC G(!(loiter_task_1.active));

--If we have not surfaced, then one of the tasks is selected by the priorities selected, or we're doing obstacle avoidance
LTLSPEC G(!(var_BLUEROV_SURFACED) -> (count(surface_task.active, surface_task_1.active, rth_task.active, loiter_task.active, tracking_task.active, waypoint_task.active) = 1 | (var_cm_hsd_input_stage_8 = cm_obstacle_avoidance_task)));
