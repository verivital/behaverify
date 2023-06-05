module Complex_robot where
import Behavior_tree_core
import In_maze_file
import In_target_file
import Flag_found_file
import Change_side_file
import Go_forward_file
import Go_side_file
import Search_tile_file
import Set_zone_file
import Flag_not_returned_file
import Can_move_forward_file
import Can_move_side_file
set_zone__node = BTreeNode set_zone [] 1
flag_not_returned__node = BTreeNode flag_not_returned [] 3
in_maze__node = BTreeNode in_maze [] 5
go_forward__node = BTreeNode go_forward [] 6
enter_maze__node = BTreeNode selectorFunc [in_maze__node, go_forward__node] 4
in_maze__node_1 = BTreeNode in_maze [] 10
maze_inverter__node = BTreeNode inverterCreator [in_maze__node_1] 9
can_move_forward__node = BTreeNode can_move_forward [] 14
go_forward__node_1 = BTreeNode go_forward [] 15
try_forward__node = BTreeNode sequenceFunc [can_move_forward__node, go_forward__node_1] 13
can_move_side__node = BTreeNode can_move_side [] 17
go_side__node = BTreeNode go_side [] 18
try_side__node = BTreeNode sequenceFunc [can_move_side__node, go_side__node] 16
change_side__node = BTreeNode change_side [] 19
move_through_maze__node = BTreeNode selectorFunc [try_forward__node, try_side__node, change_side__node] 12
move_through_maze_decorator__node = BTreeNode (xISyCreator Success Running) [move_through_maze__node] 11
navigate_maze__node = BTreeNode selectorFunc [maze_inverter__node, move_through_maze_decorator__node] 8
navigate_maze_decorator__node = BTreeNode (xISyCreator Failure Running) [navigate_maze__node] 7
in_target__node = BTreeNode in_target [] 20
can_move_side__node_1 = BTreeNode can_move_side [] 23
go_side__node_1 = BTreeNode go_side [] 24
try_side__node_1 = BTreeNode sequenceFunc [can_move_side__node_1, go_side__node_1] 22
to_side_decorator__node = BTreeNode (xISyCreator Failure Success) [try_side__node_1] 21
change_side__node_1 = BTreeNode change_side [] 25
flag_found__node = BTreeNode flag_found [] 27
search_tile__node = BTreeNode search_tile [] 29
can_move_side__node_2 = BTreeNode can_move_side [] 32
go_side__node_2 = BTreeNode go_side [] 33
try_side__node_2 = BTreeNode sequenceFunc [can_move_side__node_2, go_side__node_2] 31
change_side__node_2 = BTreeNode change_side [] 35
change_side_decorator__node = BTreeNode (xISyCreator Success Failure) [change_side__node_2] 34
go_forward__node_2 = BTreeNode go_forward [] 36
move_for_flag__node = BTreeNode selectorFunc [try_side__node_2, change_side_decorator__node, go_forward__node_2] 30
search_for_flag__node = BTreeNode selectorFunc [search_tile__node, move_for_flag__node] 28
have_or_find_flag__node = BTreeNode selectorFunc [flag_found__node, search_for_flag__node] 26
control_sequence__node = BTreeNode sequencePartialFunc [flag_not_returned__node, enter_maze__node, navigate_maze_decorator__node, in_target__node, to_side_decorator__node, change_side__node_1, have_or_find_flag__node] 2
control__node = BTreeNode (parallelCreator successOnAllFailureOne) [set_zone__node, control_sequence__node] 0
