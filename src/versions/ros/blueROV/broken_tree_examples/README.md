Each file in here has been 'broken' in some way in order to explain why the original tree is the way it is.

## failed_e_stop.bt

In this file, we don't have a special surface condition for emergency stop. This causes the blueROV to not trigger the emergency stop in cases where it should have been triggered if an obstacle avoidance flag is set to true.

changes:

- emergency_stop_fs was changed so it checks if True instead of if False (done to accomodate logic. this is not the 'important' change).

- removed the do emergency_stop_check block and merged it into the general surface_task block. THIS IS THE IMPORTANT CHANGE.

- removed references to surface_task_1, because it does not exist in this structure. Not important (but necessary for this to make any sense).


## failed_obstacle_avoidance.bt

In this file, we don't abort priorities when bb_obstacle_warning is set to True. This causes the blueROV to continue with missions as usual

changes:

- removed the check_obstacle_avoidance_resuired check. THIS IS THE IMPORTANT CHANGE.


## failsafe_final.bt

In this file, we move the check if failsafe was triggered to the end of priorities instead of leaving it at the beginning. This causes the blueROV to ignore failsafes.

changes:

- moved the check failsafe sement to end of priorities.

## mission_server_last.bt

In this file, we move the mission_server to before mission_end. This results in us not using the most relevant mission in some cases.

## mission_server_last.bt

In this file, we move the mission_server to after priorities. This cause various priorities to use outdated mission information.
