LTLSPEC G (blackboard.battery_low_warning -> (surface_task.active | surface_task_1.active | surface_task_2.active | surface_task_3.active | surface_task_4.active));
LTLSPEC G (count(surface_task.active | surface_task_1.active | surface_task_2.active | surface_task_3.active | surface_task_4.active) < 2);
LTLSPEC G (speed_max_task.active -> (!(speed_min_task.active) & !(speed_min_task_1.active)));
LTLSPEC G (speed_min_task.active -> (!(speed_max_task.active) & !(speed_min_task_1.active)));
LTLSPEC G (speed_min_task_1.active -> (!(speed_min_task.active) & !(speed_max_task.active)));
LTLSPEC F (blackboard.mission_idx = 4);
