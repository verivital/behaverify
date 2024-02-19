module Simple_robot_10 where
import Data.List ( sort )
import qualified Data.Set as Set
import qualified Data.Map as Map
import Data.Maybe ( fromJust )
import Data.Array.IArray as IArray ( (!), array, Array )

data STATE = STATE {
  x_true___ :: Integer
  , y_true___ :: Integer
  , x_goal___ :: Integer
  , y_goal___ :: Integer
  , remaining_goals___ :: Integer
  , goal_reached___ :: Bool
  , move_robot___ :: NODE_STATUS
  , try_right___ :: NODE_STATUS
  , x_too_small___ :: NODE_STATUS
  , go_right___ :: NODE_STATUS
  , try_left___ :: NODE_STATUS
  , x_too_big___ :: NODE_STATUS
  , go_left___ :: NODE_STATUS
  , try_up___ :: NODE_STATUS
  , y_too_small___ :: NODE_STATUS
  , go_up___ :: NODE_STATUS
  , try_down___ :: NODE_STATUS
  , y_too_big___ :: NODE_STATUS
  , go_down___ :: NODE_STATUS
  }
  deriving (Eq, Ord, Show)

initial_states :: Set.Set STATE
initial_states = next_func
  where
    x_true___VAL = 0
    y_true___VAL = 0
    x_goal___VAL = 0
    y_goal___VAL = 0
    remaining_goals___VAL = 0
    goal_reached___VAL = True
    next_func :: Set.Set STATE
    next_func = result
      where
        -- for x_true___VAL
        values
          | False = Set.singleton x_true___VAL
          | True = Set.fromList [(0), (1), (2), (3), (4), (5), (6), (7), (8), (9), (10)]
        result = Set.foldr (Set.union . next_func) Set.empty values
          where
            next_func :: Integer -> Set.Set STATE
            next_func x_true___VAL = result
              where
        
                -- for y_true___VAL
                values
                  | False = Set.singleton y_true___VAL
                  | True = Set.fromList [(0), (1), (2), (3), (4), (5), (6), (7), (8), (9), (10)]
                result = Set.foldr (Set.union . next_func) Set.empty values
                  where
                    next_func :: Integer -> Set.Set STATE
                    next_func y_true___VAL = result
                      where
                
                        -- for x_goal___VAL
                        values
                          | False = Set.singleton x_goal___VAL
                          | True = Set.fromList [(0), (1), (2), (3), (4), (5), (6), (7), (8), (9), (10)]
                        result = Set.foldr (Set.union . next_func) Set.empty values
                          where
                            next_func :: Integer -> Set.Set STATE
                            next_func x_goal___VAL = result
                              where
                        
                                -- for y_goal___VAL
                                values
                                  | False = Set.singleton y_goal___VAL
                                  | True = Set.fromList [(0), (1), (2), (3), (4), (5), (6), (7), (8), (9), (10)]
                                result = Set.foldr (Set.union . next_func) Set.empty values
                                  where
                                    next_func :: Integer -> Set.Set STATE
                                    next_func y_goal___VAL = result
                                      where
                                
                                        -- for remaining_goals___VAL
                                        values
                                          | False = Set.singleton remaining_goals___VAL
                                          | True = Set.singleton (3)
                                        result = Set.foldr (Set.union . next_func) Set.empty values
                                          where
                                            next_func :: Integer -> Set.Set STATE
                                            next_func remaining_goals___VAL = result
                                              where
                                        
                                                -- for goal_reached___VAL
                                                values
                                                  | False = Set.singleton goal_reached___VAL
                                                  | True = Set.singleton False
                                                result = Set.foldr (Set.union . next_func) Set.empty values
                                                  where
                                                    next_func :: Bool -> Set.Set STATE
                                                    next_func goal_reached___VAL = result
                                                      where
                                                
                                                        result = Set.singleton (STATE x_true___VAL y_true___VAL x_goal___VAL y_goal___VAL remaining_goals___VAL goal_reached___VAL INVALID INVALID INVALID INVALID INVALID INVALID INVALID INVALID INVALID INVALID INVALID INVALID INVALID)

next_states :: STATE -> Set.Set STATE
next_states state 
  | ((>) (remaining_goals___ state) (0)) = next_func
  | otherwise = Set.singleton state
  where
    x_true___VAL = x_true___ state
    y_true___VAL = y_true___ state
    x_goal___VAL = x_goal___ state
    y_goal___VAL = y_goal___ state
    remaining_goals___VAL = remaining_goals___ state
    goal_reached___VAL = goal_reached___ state
    move_robot___VAL = move_robot___ state
    try_right___VAL = try_right___ state
    x_too_small___VAL = x_too_small___ state
    go_right___VAL = go_right___ state
    try_left___VAL = try_left___ state
    x_too_big___VAL = x_too_big___ state
    go_left___VAL = go_left___ state
    try_up___VAL = try_up___ state
    y_too_small___VAL = y_too_small___ state
    go_up___VAL = go_up___ state
    try_down___VAL = try_down___ state
    y_too_big___VAL = y_too_big___ state
    go_down___VAL = go_down___ state
    next_func :: Set.Set STATE
    next_func = result
      where
        -- for x_too_small___
        value
          | False = INVALID
          | ((<) x_true___VAL x_goal___VAL) = SUCCESS
          | otherwise = FAILURE
        result = next_func value
          where
            next_func :: NODE_STATUS -> Set.Set STATE
            next_func x_too_small___VAL = result
              where
        
                -- for x_true___VAL
                values
                  | ((/=) x_too_small___VAL SUCCESS) = Set.singleton x_true___VAL
                  | True = Set.singleton (max (0) (min (10) ((+) x_true___VAL (1))))
                result = Set.foldr (Set.union . next_func) Set.empty values
                  where
                    next_func :: Integer -> Set.Set STATE
                    next_func x_true___VAL = result
                      where
                
                        -- for y_true___VAL
                        values
                          | ((/=) x_too_small___VAL SUCCESS) = Set.singleton y_true___VAL
                          | True = Set.singleton (max (0) (min (10) ((+) y_true___VAL (0))))
                        result = Set.foldr (Set.union . next_func) Set.empty values
                          where
                            next_func :: Integer -> Set.Set STATE
                            next_func y_true___VAL = result
                              where
                        
                                -- for go_right___
                                value
                                  | ((/=) x_too_small___VAL SUCCESS) = INVALID
                                  | otherwise = SUCCESS
                                result = next_func value
                                  where
                                    next_func :: NODE_STATUS -> Set.Set STATE
                                    next_func go_right___VAL = result
                                      where
                                
                                        -- for try_right___
                                        children = [x_too_small___VAL, go_right___VAL]
                                        value
                                          | False = INVALID
                                          | elem FAILURE children = FAILURE
                                          | elem RUNNING children = RUNNING
                                          | otherwise = SUCCESS
                                        result = next_func value
                                          where
                                            next_func :: NODE_STATUS -> Set.Set STATE
                                            next_func try_right___VAL = result
                                              where
                                        
                                                -- for x_too_big___
                                                value
                                                  | ((/=) try_right___VAL FAILURE) = INVALID
                                                  | ((>) x_true___VAL x_goal___VAL) = SUCCESS
                                                  | otherwise = FAILURE
                                                result = next_func value
                                                  where
                                                    next_func :: NODE_STATUS -> Set.Set STATE
                                                    next_func x_too_big___VAL = result
                                                      where
                                                
                                                        -- for x_true___VAL
                                                        values
                                                          | ((/=) x_too_big___VAL SUCCESS) = Set.singleton x_true___VAL
                                                          | True = Set.singleton (max (0) (min (10) ((+) x_true___VAL (-1))))
                                                        result = Set.foldr (Set.union . next_func) Set.empty values
                                                          where
                                                            next_func :: Integer -> Set.Set STATE
                                                            next_func x_true___VAL = result
                                                              where
                                                        
                                                                -- for y_true___VAL
                                                                values
                                                                  | ((/=) x_too_big___VAL SUCCESS) = Set.singleton y_true___VAL
                                                                  | True = Set.singleton (max (0) (min (10) ((+) y_true___VAL (0))))
                                                                result = Set.foldr (Set.union . next_func) Set.empty values
                                                                  where
                                                                    next_func :: Integer -> Set.Set STATE
                                                                    next_func y_true___VAL = result
                                                                      where
                                                                
                                                                        -- for go_left___
                                                                        value
                                                                          | ((/=) x_too_big___VAL SUCCESS) = INVALID
                                                                          | otherwise = SUCCESS
                                                                        result = next_func value
                                                                          where
                                                                            next_func :: NODE_STATUS -> Set.Set STATE
                                                                            next_func go_left___VAL = result
                                                                              where
                                                                        
                                                                                -- for try_left___
                                                                                children = [x_too_big___VAL, go_left___VAL]
                                                                                value
                                                                                  | ((/=) try_right___VAL FAILURE) = INVALID
                                                                                  | elem FAILURE children = FAILURE
                                                                                  | elem RUNNING children = RUNNING
                                                                                  | otherwise = SUCCESS
                                                                                result = next_func value
                                                                                  where
                                                                                    next_func :: NODE_STATUS -> Set.Set STATE
                                                                                    next_func try_left___VAL = result
                                                                                      where
                                                                                
                                                                                        -- for y_too_small___
                                                                                        value
                                                                                          | ((/=) try_left___VAL FAILURE) = INVALID
                                                                                          | ((<) y_true___VAL y_goal___VAL) = SUCCESS
                                                                                          | otherwise = FAILURE
                                                                                        result = next_func value
                                                                                          where
                                                                                            next_func :: NODE_STATUS -> Set.Set STATE
                                                                                            next_func y_too_small___VAL = result
                                                                                              where
                                                                                        
                                                                                                -- for x_true___VAL
                                                                                                values
                                                                                                  | ((/=) y_too_small___VAL SUCCESS) = Set.singleton x_true___VAL
                                                                                                  | True = Set.singleton (max (0) (min (10) ((+) x_true___VAL (0))))
                                                                                                result = Set.foldr (Set.union . next_func) Set.empty values
                                                                                                  where
                                                                                                    next_func :: Integer -> Set.Set STATE
                                                                                                    next_func x_true___VAL = result
                                                                                                      where
                                                                                                
                                                                                                        -- for y_true___VAL
                                                                                                        values
                                                                                                          | ((/=) y_too_small___VAL SUCCESS) = Set.singleton y_true___VAL
                                                                                                          | True = Set.singleton (max (0) (min (10) ((+) y_true___VAL (1))))
                                                                                                        result = Set.foldr (Set.union . next_func) Set.empty values
                                                                                                          where
                                                                                                            next_func :: Integer -> Set.Set STATE
                                                                                                            next_func y_true___VAL = result
                                                                                                              where
                                                                                                        
                                                                                                                -- for go_up___
                                                                                                                value
                                                                                                                  | ((/=) y_too_small___VAL SUCCESS) = INVALID
                                                                                                                  | otherwise = SUCCESS
                                                                                                                result = next_func value
                                                                                                                  where
                                                                                                                    next_func :: NODE_STATUS -> Set.Set STATE
                                                                                                                    next_func go_up___VAL = result
                                                                                                                      where
                                                                                                                
                                                                                                                        -- for try_up___
                                                                                                                        children = [y_too_small___VAL, go_up___VAL]
                                                                                                                        value
                                                                                                                          | ((/=) try_left___VAL FAILURE) = INVALID
                                                                                                                          | elem FAILURE children = FAILURE
                                                                                                                          | elem RUNNING children = RUNNING
                                                                                                                          | otherwise = SUCCESS
                                                                                                                        result = next_func value
                                                                                                                          where
                                                                                                                            next_func :: NODE_STATUS -> Set.Set STATE
                                                                                                                            next_func try_up___VAL = result
                                                                                                                              where
                                                                                                                        
                                                                                                                                -- for y_too_big___
                                                                                                                                value
                                                                                                                                  | ((/=) try_up___VAL FAILURE) = INVALID
                                                                                                                                  | ((>) y_true___VAL y_goal___VAL) = SUCCESS
                                                                                                                                  | otherwise = FAILURE
                                                                                                                                result = next_func value
                                                                                                                                  where
                                                                                                                                    next_func :: NODE_STATUS -> Set.Set STATE
                                                                                                                                    next_func y_too_big___VAL = result
                                                                                                                                      where
                                                                                                                                
                                                                                                                                        -- for x_true___VAL
                                                                                                                                        values
                                                                                                                                          | ((/=) y_too_big___VAL SUCCESS) = Set.singleton x_true___VAL
                                                                                                                                          | True = Set.singleton (max (0) (min (10) ((+) x_true___VAL (0))))
                                                                                                                                        result = Set.foldr (Set.union . next_func) Set.empty values
                                                                                                                                          where
                                                                                                                                            next_func :: Integer -> Set.Set STATE
                                                                                                                                            next_func x_true___VAL = result
                                                                                                                                              where
                                                                                                                                        
                                                                                                                                                -- for y_true___VAL
                                                                                                                                                values
                                                                                                                                                  | ((/=) y_too_big___VAL SUCCESS) = Set.singleton y_true___VAL
                                                                                                                                                  | True = Set.singleton (max (0) (min (10) ((+) y_true___VAL (-1))))
                                                                                                                                                result = Set.foldr (Set.union . next_func) Set.empty values
                                                                                                                                                  where
                                                                                                                                                    next_func :: Integer -> Set.Set STATE
                                                                                                                                                    next_func y_true___VAL = result
                                                                                                                                                      where
                                                                                                                                                
                                                                                                                                                        -- for go_down___
                                                                                                                                                        value
                                                                                                                                                          | ((/=) y_too_big___VAL SUCCESS) = INVALID
                                                                                                                                                          | otherwise = SUCCESS
                                                                                                                                                        result = next_func value
                                                                                                                                                          where
                                                                                                                                                            next_func :: NODE_STATUS -> Set.Set STATE
                                                                                                                                                            next_func go_down___VAL = result
                                                                                                                                                              where
                                                                                                                                                        
                                                                                                                                                                -- for try_down___
                                                                                                                                                                children = [y_too_big___VAL, go_down___VAL]
                                                                                                                                                                value
                                                                                                                                                                  | ((/=) try_up___VAL FAILURE) = INVALID
                                                                                                                                                                  | elem FAILURE children = FAILURE
                                                                                                                                                                  | elem RUNNING children = RUNNING
                                                                                                                                                                  | otherwise = SUCCESS
                                                                                                                                                                result = next_func value
                                                                                                                                                                  where
                                                                                                                                                                    next_func :: NODE_STATUS -> Set.Set STATE
                                                                                                                                                                    next_func try_down___VAL = result
                                                                                                                                                                      where
                                                                                                                                                                
                                                                                                                                                                        -- for move_robot___
                                                                                                                                                                        children = [try_right___VAL, try_left___VAL, try_up___VAL, try_down___VAL]
                                                                                                                                                                        value
                                                                                                                                                                          | False = INVALID
                                                                                                                                                                          | elem SUCCESS children = SUCCESS
                                                                                                                                                                          | elem RUNNING children = RUNNING
                                                                                                                                                                          | otherwise = FAILURE
                                                                                                                                                                        result = next_func value
                                                                                                                                                                          where
                                                                                                                                                                            next_func :: NODE_STATUS -> Set.Set STATE
                                                                                                                                                                            next_func move_robot___VAL = result
                                                                                                                                                                              where
                                                                                                                                                                        
                                                                                                                                                                                -- for goal_reached___VAL
                                                                                                                                                                                values
                                                                                                                                                                                  | False = Set.singleton goal_reached___VAL
                                                                                                                                                                                  | True = Set.singleton ((&&) ((==) x_goal___VAL x_true___VAL) ((==) y_goal___VAL y_true___VAL))
                                                                                                                                                                                result = Set.foldr (Set.union . next_func) Set.empty values
                                                                                                                                                                                  where
                                                                                                                                                                                    next_func :: Bool -> Set.Set STATE
                                                                                                                                                                                    next_func goal_reached___VAL = result
                                                                                                                                                                                      where
                                                                                                                                                                                
                                                                                                                                                                                        -- for remaining_goals___VAL
                                                                                                                                                                                        values
                                                                                                                                                                                          | False = Set.singleton remaining_goals___VAL
                                                                                                                                                                                          | goal_reached___VAL = Set.singleton (max (0) ((-) remaining_goals___VAL (1)))
                                                                                                                                                                                          | True = Set.singleton remaining_goals___VAL
                                                                                                                                                                                        result = Set.foldr (Set.union . next_func) Set.empty values
                                                                                                                                                                                          where
                                                                                                                                                                                            next_func :: Integer -> Set.Set STATE
                                                                                                                                                                                            next_func remaining_goals___VAL = result
                                                                                                                                                                                              where
                                                                                                                                                                                        
                                                                                                                                                                                                -- for x_goal___VAL
                                                                                                                                                                                                values
                                                                                                                                                                                                  | False = Set.singleton x_goal___VAL
                                                                                                                                                                                                  | ((==) (0) remaining_goals___VAL) = Set.singleton x_goal___VAL
                                                                                                                                                                                                  | goal_reached___VAL = Set.fromList [(0), (1), (2), (3), (4), (5), (6), (7), (8), (9), (10)]
                                                                                                                                                                                                  | True = Set.singleton x_goal___VAL
                                                                                                                                                                                                result = Set.foldr (Set.union . next_func) Set.empty values
                                                                                                                                                                                                  where
                                                                                                                                                                                                    next_func :: Integer -> Set.Set STATE
                                                                                                                                                                                                    next_func x_goal___VAL = result
                                                                                                                                                                                                      where
                                                                                                                                                                                                
                                                                                                                                                                                                        -- for y_goal___VAL
                                                                                                                                                                                                        values
                                                                                                                                                                                                          | False = Set.singleton y_goal___VAL
                                                                                                                                                                                                          | ((==) (0) remaining_goals___VAL) = Set.singleton y_goal___VAL
                                                                                                                                                                                                          | goal_reached___VAL = Set.fromList [(0), (1), (2), (3), (4), (5), (6), (7), (8), (9), (10)]
                                                                                                                                                                                                          | True = Set.singleton y_goal___VAL
                                                                                                                                                                                                        result = Set.foldr (Set.union . next_func) Set.empty values
                                                                                                                                                                                                          where
                                                                                                                                                                                                            next_func :: Integer -> Set.Set STATE
                                                                                                                                                                                                            next_func y_goal___VAL = result
                                                                                                                                                                                                              where
                                                                                                                                                                                                        
                                                                                                                                                                                                                result = Set.singleton (STATE x_true___VAL y_true___VAL x_goal___VAL y_goal___VAL remaining_goals___VAL goal_reached___VAL move_robot___VAL try_right___VAL x_too_small___VAL go_right___VAL try_left___VAL x_too_big___VAL go_left___VAL try_up___VAL y_too_small___VAL go_up___VAL try_down___VAL y_too_big___VAL go_down___VAL)

data NODE_STATUS = SUCCESS | RUNNING | FAILURE | INVALID
  deriving (Enum, Eq, Ord, Show)

type STATE_MAP = Map.Map STATE (Set.Set STATE)

if_then_else :: Bool -> a -> a -> a
if_then_else True val _ = val
if_then_else False _ val = val
    
reachable_states :: Set.Set STATE
reachable_states = reachable_states_func Set.empty initial_states
  where
    reachable_states_func :: Set.Set STATE -> Set.Set STATE -> Set.Set STATE
    reachable_states_func seen_states states_to_explore
      | Set.null unvisited_states = seen_states
      | otherwise = reachable
      where
        unvisited_states = Set.difference states_to_explore seen_states
        reachable = reachable_states_func (Set.union seen_states unvisited_states) (Set.unions (Set.map next_states unvisited_states))

state_map :: STATE_MAP
state_map = construct_state_map Map.empty (Map.fromList [(new_state, Set.empty) | new_state <- Set.toList initial_states])
  where
    dummy_next_states :: STATE -> a -> Set.Set STATE
    dummy_next_states state _ = next_states state
    construct_state_map :: STATE_MAP -> STATE_MAP -> STATE_MAP
    construct_state_map seen_map to_explore_map
      | Map.null unvisited_map = seen_map
      | otherwise = full_map
      where
        unvisited_map = Map.difference to_explore_map seen_map
        explored_map = Map.mapWithKey dummy_next_states unvisited_map
        new_seen_map
          | Map.size seen_map > Map.size explored_map = Map.union seen_map explored_map
          | otherwise = Map.union explored_map seen_map
        nextExplore = Map.fromList [(new_state, Set.empty) | new_state <- Set.toList (Set.unions (Map.elems explored_map))]
        full_map = construct_state_map new_seen_map nextExplore

reversed_map_lookup :: STATE_MAP -> STATE -> Set.Set STATE
reversed_map_lookup state_map state = fromJust (Map.lookup state state_map)

ctl_ax :: (STATE -> Bool) -> STATE -> Bool
ctl_ax function state = Set.foldr ((&&) . function) True (fromJust (Map.lookup state state_map))

ctl_ex :: (STATE -> Bool) -> STATE -> Bool
ctl_ex function state = Set.foldr ((||) . function) False (fromJust (Map.lookup state state_map))

ctl_af :: (STATE -> Bool) -> STATE -> Bool
ctl_af function = ctl_af_state_search function Set.empty
ctl_af_state_search :: (STATE -> Bool) -> Set.Set STATE -> STATE -> Bool
ctl_af_state_search function seen_states state
  | function state = True
  | Set.member state seen_states = False -- This means we haven't reached true and have nothing left to check
  | otherwise = Set.foldr ((&&) . ctl_af_state_search function (Set.insert state seen_states)) True (fromJust (Map.lookup state state_map)) -- more searching required.


ctl_ef :: (STATE -> Bool) -> STATE -> Bool
ctl_ef function state = (||) (function state) (ctl_ef_state_search function (Set.singleton state) (fromJust (Map.lookup state state_map)))
ctl_ef_state_search :: (STATE -> Bool) -> Set.Set STATE -> Set.Set STATE -> Bool
ctl_ef_state_search function seen_states states_to_explore
  | Set.null unexplored_states = False -- This means we haven't reached true and have nothing left to check
  | otherwise = conclusion -- This means we still have states to check
  where
    unexplored_states = Set.difference states_to_explore seen_states  -- make sure to remove any overlap.
    found_true = Set.foldr ((||) . function) False unexplored_states -- check if the condition holds for any of the new states
    conclusion
      | found_true = True -- if the condition holds for any of the new states, then we're done.
      | otherwise = ctl_ef_state_search function (Set.union seen_states unexplored_states) (Set.foldr (Set.union . reversed_map_lookup state_map) Set.empty unexplored_states) -- more searching required.


ctl_ag :: (STATE -> Bool) -> STATE -> Bool
ctl_ag function state = (&&) (function state) (ctl_ag_state_search function (Set.singleton state) (fromJust (Map.lookup state state_map)))
ctl_ag_state_search :: (STATE -> Bool) -> Set.Set STATE -> Set.Set STATE -> Bool
ctl_ag_state_search function seen_states states_to_explore
  | Set.null unexplored_states = True -- we ran out of states and found nothing wrong, return true.
  | otherwise = conclusion
  where
    unexplored_states = Set.difference states_to_explore seen_states  -- make sure to remove any overlap.
    all_true = Set.foldr ((&&) . function) True unexplored_states -- check if the condition holds for all of the new states
    conclusion
      | not all_true = False -- at least one of our current states failed, so it didn't hold globally.
      | otherwise = ctl_ag_state_search function (Set.union seen_states unexplored_states) (Set.foldr (Set.union . reversed_map_lookup state_map) Set.empty unexplored_states) -- keep searching


ctl_eg :: (STATE -> Bool) -> STATE -> Bool
ctl_eg function = ctl_eg_state_search function Set.empty
ctl_eg_state_search :: (STATE -> Bool) -> Set.Set STATE -> STATE -> Bool
ctl_eg_state_search function seen_states state
  | not (function state) = False -- it doesn't hold for the state, so it's not true.
  | Set.member state seen_states = True -- we've looped!
  | otherwise = Set.foldr ((||) . ctl_eg_state_search function (Set.insert state seen_states)) False (fromJust (Map.lookup state state_map)) -- more searching required.


ctl_au :: (STATE -> Bool) -> (STATE -> Bool) -> STATE -> Bool
ctl_au function_hold function_release state = (||) (function_release state) ((&&) (function_hold state) (ctl_au_state_search function_hold function_release (Set.singleton state) (fromJust (Map.lookup state state_map))))
ctl_au_state_search :: (STATE -> Bool) -> (STATE -> Bool) -> Set.Set STATE -> Set.Set STATE -> Bool
ctl_au_state_search function_hold function_release seen_states states_to_explore
  | Set.null unexplored_states = False -- we ran out of states and at least one path didn't terminate with the release.
  | otherwise = conclusion
  where
    unexplored_states = Set.difference states_to_explore seen_states  -- make sure to remove any overlap.
    not_released_states = Set.filter (not . function_release) unexplored_states -- Filter so we only have states where the release condition is false.
    allTrue = Set.foldr ((&&) . function_hold) True not_released_states -- check if the condition holds for all of the not released states
    conclusion
      | not allTrue = False -- at least one of our current states failed, so it didn't reach the point of release
      | otherwise = ctl_au_state_search function_hold function_release (Set.union seen_states unexplored_states) (Set.foldr (Set.union . reversed_map_lookup state_map) Set.empty not_released_states) -- keep searching


ctl_eu :: (STATE -> Bool) -> (STATE -> Bool) -> STATE -> Bool
ctl_eu function_hold function_release state = (||) (function_release state) ((&&) (function_hold state) (ctl_eu_state_search function_hold function_release (Set.singleton state) (fromJust (Map.lookup state state_map))))
ctl_eu_state_search :: (STATE -> Bool) -> (STATE -> Bool) -> Set.Set STATE -> Set.Set STATE -> Bool
ctl_eu_state_search function_hold function_release seen_states states_to_explore
  | Set.null unexplored_states = False -- we ran out of states and no path terminated with the release.
  | otherwise = conclusion
  where
    unexplored_states = Set.difference states_to_explore seen_states  -- make sure to remove any overlap.
    release_found = Set.foldr ((||) . function_release) False unexplored_states -- check if the condition holds for all of the not released states
    holding_states = Set.filter function_hold unexplored_states -- Filter so we only have states where the release condition is false.
    conclusion
      | release_found = True -- we managed to reach the release
      | otherwise = ctl_eu_state_search function_hold function_release (Set.union seen_states unexplored_states) (Set.foldr (Set.union . reversed_map_lookup state_map) Set.empty holding_states) -- keep searching


ctl_aw :: (STATE -> Bool) -> (STATE -> Bool) -> STATE -> Bool
ctl_aw function_hold function_release state = (||) (function_release state) ((&&) (function_hold state) (ctl_aw_state_search function_hold function_release Set.empty (fromJust (Map.lookup state state_map))))
ctl_aw_state_search :: (STATE -> Bool) -> (STATE -> Bool) -> Set.Set STATE -> Set.Set STATE -> Bool
ctl_aw_state_search function_hold function_release seen_states states_to_explore
  | Set.null unexplored_states = True -- we ran out of states and there were no problems
  | otherwise = conclusion
  where
    unexplored_states = Set.difference states_to_explore seen_states  -- make sure to remove any overlap.
    not_released_states = Set.filter (not . function_release) unexplored_states -- Filter so we only have states where the release condition is false.
    all_true = Set.foldr ((&&) . function_hold) True not_released_states -- check if the condition holds for all of the not released states
    conclusion
      | not all_true = False -- at least one of our current states failed, so it didn't reach the point of release
      | otherwise = ctl_aw_state_search function_hold function_release (Set.union seen_states unexplored_states) (Set.foldr (Set.union . reversed_map_lookup state_map) Set.empty not_released_states) -- keep searching


ctl_ew :: (STATE -> Bool) -> (STATE -> Bool) -> STATE -> Bool
ctl_ew function_hold function_release = ctl_ew_state_search function_hold function_release Set.empty
ctl_ew_state_search :: (STATE -> Bool) -> (STATE -> Bool) -> Set.Set STATE -> STATE -> Bool
ctl_ew_state_search function_hold function_release seen_states state
  | function_release state = True
  | not (function_hold state) = False
  | otherwise = Set.foldr ((||) . ctl_ew_state_search function_hold function_release (Set.insert state seen_states)) False (fromJust (Map.lookup state state_map)) -- more searching required.

ctl_0 :: Bool
ctl_0 = Set.foldr ((&&) . ctl_func) True initial_states
  where
    ctl_func :: STATE -> Bool
    ctl_func state = (ctl_ef (\state -> ((==) (remaining_goals___ state) (0))) state)

invar_1 :: Bool
invar_1 = Set.foldr ((&&) . invar_func) True reachable_states
  where
    invar_func :: STATE -> Bool
    invar_func state = (>) (remaining_goals___ state) 0

invar_2 :: Bool
invar_2 = Set.foldr ((&&) . invar_func) True reachable_states
  where
    invar_func :: STATE -> Bool
    invar_func state = (>) (remaining_goals___ state) (-1)


data STATE2 = STATE2 {
  x :: Integer
  , y :: Integer
  }
  deriving (Eq, Ord, Show)

fuck :: Set.Set STATE2
fuck = Set.fromList [
  STATE2 x_val token_val
  | x_val <- [0, 2]
  , y_val <- [0, 5]
  , x_val /= y_val
  , let token_val = y_val * x_val
  , x_val <- [x_val + y_val, x_val - y_val]
  , y_val <- if_then_else (x_val < 0) [10] [token_val]
  ]

main :: IO ()
main = 
  do {
    print "model checking for Simple_robot_10"
    ; print fuck
    -- ; putStrLn ((++) "ctl_0 is " (show ctl_0))
    -- ; putStrLn ((++) "invar_1 is " (show invar_1))
    -- ; putStrLn ((++) "invar_2 is " (show invar_2))
  }
