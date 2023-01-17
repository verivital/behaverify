--FAIRNESS (get_mission_DOT_saw_target);
LTLSPEC G (count(go_down.active, go_left.active, go_right.active, go_up.active) <= 1);
LTLSPEC F (remaining_goals = 0);
