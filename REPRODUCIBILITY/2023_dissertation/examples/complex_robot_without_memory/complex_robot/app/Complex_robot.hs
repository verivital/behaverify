module Complex_robot where
import Behavior_tree_core
import In_home_file
import In_maze_file
import In_target_file
import Flag_found_file
import Need_side_file
import Success_node_file
import Change_side_file
import Go_forward_file
import Go_side_file
import Never_need_side_file
import Search_tile_file
import Set_zone_file
import Flag_not_returned_file
import Can_move_forward_file
import Can_move_side_file
set_zone__node = BTreeNode set_zone [] 1
flag_not_returned__node = BTreeNode flag_not_returned [] 3
in_maze__node = BTreeNode in_maze [] 6
can_move_forward__node = BTreeNode can_move_forward [] 10
go_forward__node = BTreeNode go_forward [] 11
try_forward__node = BTreeNode sequenceFunc [can_move_forward__node, go_forward__node] 9
can_move_side__node = BTreeNode can_move_side [] 14
go_side__node = BTreeNode go_side [] 15
try_side__node = BTreeNode sequenceFunc [can_move_side__node, go_side__node] 13
change_side__node = BTreeNode change_side [] 17
return_failure__node = BTreeNode (decoratorCreator (xISyCreator Success Failure)) [change_side__node] 16
try_side_or_change__node = BTreeNode selectorFunc [try_side__node, return_failure__node] 12
success_node__node = BTreeNode success_node [] 18
move_through_maze__node = BTreeNode selectorFunc [try_forward__node, try_side_or_change__node, success_node__node] 8
move_through_maze_decorator__node = BTreeNode (decoratorCreator (xISyCreator Success Running)) [move_through_maze__node] 7
navigate_maze__node = BTreeNode sequenceFunc [in_maze__node, move_through_maze_decorator__node] 5
in_maze__node_1 = BTreeNode in_maze [] 21
maze_inverter__node = BTreeNode (decoratorCreator inverterCreator) [in_maze__node_1] 20
in_target__node = BTreeNode in_target [] 24
flag_found__node = BTreeNode flag_found [] 25
go_home__node = BTreeNode sequenceFunc [in_target__node, flag_found__node] 23
in_home__node = BTreeNode in_home [] 27
flag_found__node_1 = BTreeNode flag_found [] 29
flag_inverter__node = BTreeNode (decoratorCreator inverterCreator) [flag_found__node_1] 28
go_target__node = BTreeNode sequenceFunc [in_home__node, flag_inverter__node] 26
traversal_needed__node = BTreeNode selectorFunc [go_home__node, go_target__node] 22
go_forward__node_1 = BTreeNode go_forward [] 30
enter_maze__node = BTreeNode sequenceFunc [maze_inverter__node, traversal_needed__node, go_forward__node_1] 19
in_target__node_1 = BTreeNode in_target [] 32
need_side__node = BTreeNode need_side [] 33
can_move_side__node_1 = BTreeNode can_move_side [] 37
go_side__node_1 = BTreeNode go_side [] 38
try_side__node_1 = BTreeNode sequenceFunc [can_move_side__node_1, go_side__node_1] 36
change_side__node_1 = BTreeNode change_side [] 40
return_failure__node_1 = BTreeNode (decoratorCreator (xISyCreator Success Failure)) [change_side__node_1] 39
try_side_or_change__node_1 = BTreeNode selectorFunc [try_side__node_1, return_failure__node_1] 35
side_reached__node = BTreeNode (decoratorCreator (xISyCreator Failure Success)) [try_side_or_change__node_1] 34
never_need_side__node = BTreeNode never_need_side [] 41
to_side__node = BTreeNode sequenceFunc [in_target__node_1, need_side__node, side_reached__node, never_need_side__node] 31
in_target__node_2 = BTreeNode in_target [] 43
flag_found__node_2 = BTreeNode flag_found [] 45
flag_inverter__node_1 = BTreeNode (decoratorCreator inverterCreator) [flag_found__node_2] 44
search_tile__node = BTreeNode search_tile [] 47
can_move_side__node_2 = BTreeNode can_move_side [] 51
go_side__node_2 = BTreeNode go_side [] 52
try_side__node_2 = BTreeNode sequenceFunc [can_move_side__node_2, go_side__node_2] 50
change_side__node_2 = BTreeNode change_side [] 54
return_failure__node_2 = BTreeNode (decoratorCreator (xISyCreator Success Failure)) [change_side__node_2] 53
try_side_or_change__node_2 = BTreeNode selectorFunc [try_side__node_2, return_failure__node_2] 49
go_forward__node_2 = BTreeNode go_forward [] 55
move_for_flag__node = BTreeNode selectorFunc [try_side_or_change__node_2, go_forward__node_2] 48
search_for_flag__node = BTreeNode selectorFunc [search_tile__node, move_for_flag__node] 46
search_target__node = BTreeNode sequenceFunc [in_target__node_2, flag_inverter__node_1, search_for_flag__node] 42
control_selector__node = BTreeNode selectorFunc [navigate_maze__node, enter_maze__node, to_side__node, search_target__node] 4
control_sequence__node = BTreeNode sequenceFunc [flag_not_returned__node, control_selector__node] 2
control__node = BTreeNode (parallelCreator successOnAllFailureOne) [set_zone__node, control_sequence__node] 0
