LTLSPEC G (count(go_down.active, go_left.active, go_right.active, go_up.active) <= 1);
-- FAIRNESS (get_mission_DOT_saw_target_stage_1);
LTLSPEC F (env_remaining_goals_stage_1 = 0);
