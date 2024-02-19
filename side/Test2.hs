module Test2 where
import Data.List ( sort, group )
import qualified Data.Set as Set
import qualified Data.Map as Map
import Data.Maybe ( fromJust )
import Data.Array ( Array, array, listArray, (!) )

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

initial_states :: [STATE]
initial_states = map head (group (sort [
  STATE x_true___VAL y_true___VAL x_goal___VAL y_goal___VAL remaining_goals___VAL goal_reached___VAL INVALID INVALID INVALID INVALID INVALID INVALID INVALID INVALID INVALID INVALID INVALID INVALID INVALID
  | let x_true___VAL = 0
  , let y_true___VAL = 0
  , let x_goal___VAL = 0
  , let y_goal___VAL = 0
  , let remaining_goals___VAL = 0
  , let goal_reached___VAL = True
  , x_true___VAL <- [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
  --, x_true___VAL <- [0]
  --, y_true___VAL <- [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
  , y_true___VAL <- [0]
  , x_goal___VAL <- [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
  , y_goal___VAL <- [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
  --, y_goal___VAL <- [0]
  , let remaining_goals___VAL = 2
  , let goal_reached___VAL = False
  ]))

next_states :: STATE -> [STATE]
next_states state 
  | ((>) (remaining_goals___ state) 0) = result
  | otherwise = [state]
  where
    result = map head (group (sort [
      STATE x_true___VAL y_true___VAL x_goal___VAL y_goal___VAL remaining_goals___VAL goal_reached___VAL move_robot___VAL try_right___VAL x_too_small___VAL go_right___VAL try_left___VAL x_too_big___VAL go_left___VAL try_up___VAL y_too_small___VAL go_up___VAL try_down___VAL y_too_big___VAL go_down___VAL
      | let x_true___VAL = x_true___ state
      , let y_true___VAL = y_true___ state
      , let x_goal___VAL = x_goal___ state
      , let y_goal___VAL = y_goal___ state
      , let remaining_goals___VAL = remaining_goals___ state
      , let goal_reached___VAL = goal_reached___ state
      , let x_too_small___VAL = if_then_else ((<) x_true___VAL x_goal___VAL) SUCCESS FAILURE
      , x_true___VAL <- [if_then_else ((/=) x_too_small___VAL SUCCESS) x_true___VAL (max 0 (min 50 ((+) x_true___VAL 1)))]
      , y_true___VAL <- [if_then_else ((/=) x_too_small___VAL SUCCESS) y_true___VAL (max 0 (min 50 ((+) y_true___VAL 0)))]
      , let go_right___VAL = if_then_else ((/=) x_too_small___VAL SUCCESS) INVALID SUCCESS
      , let children = [x_too_small___VAL, go_right___VAL]
      , let try_right___VAL = if_then_else (elem FAILURE children) FAILURE (if_then_else (elem RUNNING children) RUNNING SUCCESS)
      , let x_too_big___VAL = if_then_else ((/=) try_right___VAL FAILURE) INVALID (if_then_else ((>) x_true___VAL x_goal___VAL) SUCCESS FAILURE)
      , x_true___VAL <- [if_then_else ((/=) x_too_big___VAL SUCCESS) x_true___VAL (max 0 (min 50 ((+) x_true___VAL (-1))))]
      , y_true___VAL <- [if_then_else ((/=) x_too_big___VAL SUCCESS) y_true___VAL (max 0 (min 50 ((+) y_true___VAL 0)))]
      , let go_left___VAL = if_then_else ((/=) x_too_big___VAL SUCCESS) INVALID SUCCESS
      , let children = [x_too_big___VAL, go_left___VAL]
      , let try_left___VAL = if_then_else ((/=) try_right___VAL FAILURE) INVALID (if_then_else (elem FAILURE children) FAILURE (if_then_else (elem RUNNING children) RUNNING SUCCESS))
      , let y_too_small___VAL = if_then_else ((/=) try_left___VAL FAILURE) INVALID (if_then_else ((<) y_true___VAL y_goal___VAL) SUCCESS FAILURE)
      , x_true___VAL <- [if_then_else ((/=) y_too_small___VAL SUCCESS) x_true___VAL (max 0 (min 50 ((+) x_true___VAL 0)))]
      , y_true___VAL <- [if_then_else ((/=) y_too_small___VAL SUCCESS) y_true___VAL (max 0 (min 50 ((+) y_true___VAL 1)))]
      , let go_up___VAL = if_then_else ((/=) y_too_small___VAL SUCCESS) INVALID SUCCESS
      , let children = [y_too_small___VAL, go_up___VAL]
      , let try_up___VAL = if_then_else ((/=) try_left___VAL FAILURE) INVALID (if_then_else (elem FAILURE children) FAILURE (if_then_else (elem RUNNING children) RUNNING SUCCESS))
      , let y_too_big___VAL = if_then_else ((/=) try_up___VAL FAILURE) INVALID (if_then_else ((>) y_true___VAL y_goal___VAL) SUCCESS FAILURE)
      , x_true___VAL <- [if_then_else ((/=) y_too_big___VAL SUCCESS) x_true___VAL (max 0 (min 50 ((+) x_true___VAL 0)))]
      , y_true___VAL <- if_then_else ((/=) y_too_big___VAL SUCCESS) [y_true___VAL] [(max 0 (min 50 ((+) y_true___VAL (-1))))]
      , let go_down___VAL = if_then_else ((/=) y_too_big___VAL SUCCESS) INVALID SUCCESS
      , let children = [y_too_big___VAL, go_down___VAL]
      , let try_down___VAL = if_then_else ((/=) try_up___VAL FAILURE) INVALID (if_then_else (elem FAILURE children) FAILURE (if_then_else (elem RUNNING children) RUNNING SUCCESS))
      , let children = [try_right___VAL, try_left___VAL, try_up___VAL, try_down___VAL]
      , let move_robot___VAL = if_then_else (elem SUCCESS children) SUCCESS (if_then_else (elem RUNNING children) RUNNING FAILURE)
      , goal_reached___VAL <- [(&&) ((==) x_goal___VAL x_true___VAL) ((==) y_goal___VAL y_true___VAL)]
      , remaining_goals___VAL <- [if_then_else goal_reached___VAL (max 0 ((-) remaining_goals___VAL 1)) remaining_goals___VAL]
      --, x_goal___VAL <- if_then_else ((==) 0 remaining_goals___VAL) [x_goal___VAL] (if_then_else goal_reached___VAL [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50] [x_goal___VAL])
      , x_goal___VAL <- if_then_else ((==) 0 remaining_goals___VAL) [x_goal___VAL] (if_then_else goal_reached___VAL [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] [x_goal___VAL])
      --, y_goal___VAL <- if_then_else ((==) 0 remaining_goals___VAL) [y_goal___VAL] (if_then_else goal_reached___VAL [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50] [y_goal___VAL])
      , y_goal___VAL <- if_then_else ((==) 0 remaining_goals___VAL) [y_goal___VAL] (if_then_else goal_reached___VAL [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] [y_goal___VAL])
      ]))

data NODE_STATUS = SUCCESS | RUNNING | FAILURE | INVALID
   deriving (Enum, Eq, Ord, Show)

--type STATE_MAP = Map.Map STATE [STATE]
type STATE_MAP = Map.Map STATE_ID [STATE_ID]
type STATE_ID = Integer
type FUNCTION_ID = Integer

if_then_else :: Bool -> a -> a -> a
if_then_else True val _ = val
if_then_else False _ val = val

list_difference :: [STATE] -> [STATE] -> [STATE]
list_difference [] _ = []
list_difference a [] = a
list_difference (a_head : a_tail) (b_head : b_tail)
  | a_head < b_head = a_head : list_difference a_tail (b_head : b_tail)
  | a_head == b_head = list_difference a_tail b_tail
  | otherwise = list_difference (a_head : a_tail) b_tail

list_merge :: [STATE] -> [STATE] -> [STATE]
list_merge [] b = b
list_merge a [] = a
list_merge (a_head : a_tail) (b_head : b_tail)
  | a_head < b_head = a_head : list_merge a_tail (b_head : b_tail)
  | a_head == b_head = a_head : list_merge a_tail b_tail
  | otherwise = b_head : list_merge (a_head : a_tail) b_tail

reachable_states :: Array Integer STATE
number_of_reachable_states :: Integer
initial_states_location :: [Integer]
(initial_states_location, number_of_reachable_states, reachable_states) = output
  where
    output = (initial_states_location_, number_of_reachable_states_, reachable_states_)
    (initial_states_location_, number_of_reachable_states_) = location_and_length 0 initial_states reachable_states_list
    reachable_states_ = listArray (0, number_of_reachable_states_ - 1) reachable_states_list
    integer_length :: [STATE] -> Integer
    integer_length [] = 0
    integer_length (x:xs) = 1 + (integer_length xs)
    location_and_length :: Integer -> [STATE] -> [STATE] -> ([Integer], Integer)
    location_and_length _ [] reachable = ([], integer_length reachable)
    location_and_length current_index (initial_head : initial_tail) (reachable_head : reachable_tail) = (index_list, length_value)
      where
        next_vals
          | initial_head == reachable_head = location_and_length (current_index + 1) initial_tail reachable_tail
          | otherwise =  location_and_length current_index (initial_head : initial_tail) reachable_tail
        index_list
          | initial_head == reachable_head = current_index : fst next_vals
          | otherwise = fst next_vals
        length_value = 1 + (snd next_vals)
    reachable_states_list :: [STATE]
    reachable_states_list = reachable_states_func [] initial_states
      where
        reachable_states_func :: [STATE] -> [STATE] -> [STATE]
        reachable_states_func seen_states states_to_explore
          | null unvisited_states = seen_states
          | otherwise = reachable
          where
            unvisited_states = list_difference states_to_explore seen_states
            reachable = reachable_states_func (list_merge seen_states unvisited_states) (foldr (list_merge . next_states) [] unvisited_states)


state_to_num :: STATE -> STATE_ID
state_to_num = state_to_num_rec 0 (number_of_reachable_states - 1)
state_to_num_rec :: STATE_ID -> STATE_ID -> STATE -> STATE_ID
state_to_num_rec lower_bound upper_bound state
  | middle_state == state = middle_bound
  | middle_state < state = state_to_num_rec (middle_bound + 1) upper_bound state
  | otherwise = state_to_num_rec lower_bound (middle_bound - 1) state
  where
    middle_bound = div (upper_bound + lower_bound) 2
    middle_state = reachable_states ! middle_bound


state_map :: STATE_MAP
state_map = Map.map (map state_to_num) (Map.mapKeys state_to_num state_map_states)
  where
    state_map_states :: Map.Map STATE [STATE]
    state_map_states = construct_state_map Map.empty (Map.fromList [(new_state, []) | new_state <- initial_states])
      where
        dummy_next_states :: STATE -> a -> [STATE]
        dummy_next_states state _ = next_states state
        construct_state_map :: Map.Map STATE [STATE] -> Map.Map STATE [STATE] -> Map.Map STATE [STATE]
        construct_state_map seen_map to_explore_map
          | Map.null unvisited_map = seen_map
          | otherwise = full_map
          where
            unvisited_map = Map.difference to_explore_map seen_map
            explored_map = Map.mapWithKey dummy_next_states unvisited_map
            new_seen_map
              | Map.size seen_map > Map.size explored_map = Map.union seen_map explored_map
              | otherwise = Map.union explored_map seen_map
            next_explore = Map.fromList [(new_state, []) | new_state <- foldr list_merge [] (Map.elems explored_map)]
            full_map = construct_state_map new_seen_map next_explore


memoization_array_index :: FUNCTION_ID -> STATE_ID -> Bool
memoization_array_index function_num state_num = memoization_array ! (function_num, state_num)


memoization_array :: Array (Integer, Integer) Bool
memoization_array = array ((0, 0), (number_of_functions - 1, number_of_reachable_states - 1)) [((function_num, state_num), evaluate_function_state function_num state_num) | function_num <- [0..(number_of_functions - 1)], state_num <- [0..(number_of_reachable_states - 1)]]

number_of_functions :: FUNCTION_ID
number_of_functions = 1

evaluate_function_state :: FUNCTION_ID -> STATE_ID -> Bool
evaluate_function_state function_num = num_to_function function_num

num_to_function :: FUNCTION_ID -> (STATE_ID -> Bool)
num_to_function 0 = ctl_func_0


ctl_0 :: Bool
ctl_0 = foldr ((&&) . (memoization_array_index 0)) True initial_states_location
--   where
--     ctl_func :: STATE -> Bool
--     ctl_func state = (ctl_af (\state -> ((==) (remaining_goals___ state) 0)) state)

--always finally
ctl_func_0 :: STATE_ID -> Bool
ctl_func_0 state_num = (||) (inner_func (reachable_states ! state_num)) (foldr ((&&) . (memoization_array_index 0)) True (fromJust (Map.lookup state_num state_map)))
  where
    inner_func :: STATE -> Bool
    inner_func state = ((==) (remaining_goals___ state) 0)

--exists finally
ctl_func_1 :: STATE_ID -> Bool
ctl_func_1 state_num = (||) (inner_func (reachable_states ! state_num)) (foldr ((||) . (memoization_array_index 1)) False (fromJust (Map.lookup state_num state_map)))
  where
    inner_func :: STATE -> Bool
    inner_func state = ((==) (remaining_goals___ state) 0)

--always globally
ctl_func_2 :: STATE_ID -> Bool
ctl_func_2 state_num = (&&) (inner_func (reachable_states ! state_num)) (foldr ((&&) . (memoization_array_index 2)) True (fromJust (Map.lookup state_num state_map)))
  where
    inner_func :: STATE -> Bool
    inner_func state = ((==) (remaining_goals___ state) 0)

--exists globally
ctl_func_3 :: STATE_ID -> Bool
ctl_func_3 state_num = (&&) (inner_func (reachable_states ! state_num)) (foldr ((||) . (memoization_array_index 3)) False (fromJust (Map.lookup state_num state_map)))
  where
    inner_func :: STATE -> Bool
    inner_func state = ((==) (remaining_goals___ state) 0)


--always next
ctl_func_4 :: STATE_ID -> Bool
ctl_func_4 state_num = foldr ((&&) . inner_func . ((!) reachable_states)) True (fromJust (Map.lookup state_num state_map))
  where
    inner_func :: STATE -> Bool
    inner_func state = ((==) (remaining_goals___ state) 0)

--exists next
ctl_func_5 :: STATE_ID -> Bool
ctl_func_5 state_num = foldr ((||) . inner_func . ((!) reachable_states)) False (fromJust (Map.lookup state_num state_map))
  where
    inner_func :: STATE -> Bool
    inner_func state = ((==) (remaining_goals___ state) 0)

--always until
ctl_func_6 :: STATE_ID -> Bool
ctl_func_6 state_num = (||) (release_func (reachable_states ! state_num)) ((&&) (hold_func (reachable_states ! state_num)) (foldr ((&&) . (memoization_array_index 6)) True (fromJust (Map.lookup state_num state_map))))
  where
    release_func :: STATE -> Bool
    release_func state = ((==) (remaining_goals___ state) 0)
    hold_func :: STATE -> Bool
    hold_func state = ((==) (remaining_goals___ state) 1)

--exists until
ctl_func_7 :: STATE_ID -> Bool
ctl_func_7 state_num = (||) (release_func (reachable_states ! state_num)) ((&&) (hold_func (reachable_states ! state_num)) (foldr ((||) . (memoization_array_index 7)) False (fromJust (Map.lookup state_num state_map))))
  where
    release_func :: STATE -> Bool
    release_func state = ((==) (remaining_goals___ state) 0)
    hold_func :: STATE -> Bool
    hold_func state = ((==) (remaining_goals___ state) 1)


--always weak
ctl_func_8 :: STATE_ID -> Bool
ctl_func_8 state_num = (||) (release_func (reachable_states ! state_num)) ((&&) (hold_func (reachable_states ! state_num)) (foldr ((&&) . (memoization_array_index 8)) True (fromJust (Map.lookup state_num state_map))))
  where
    release_func :: STATE -> Bool
    release_func state = ((==) (remaining_goals___ state) 0)
    hold_func :: STATE -> Bool
    hold_func state = ((==) (remaining_goals___ state) 1)

--exists until
ctl_func_7 :: STATE_ID -> Bool
ctl_func_7 state_num = (||) (release_func (reachable_states ! state_num)) ((&&) (hold_func (reachable_states ! state_num)) (foldr ((||) . (memoization_array_index 7)) False (fromJust (Map.lookup state_num state_map))))
  where
    release_func :: STATE -> Bool
    release_func state = ((==) (remaining_goals___ state) 0)
    hold_func :: STATE -> Bool
    hold_func state = ((==) (remaining_goals___ state) 1)
    


--reversed_map_lookup :: STATE_MAP -> STATE -> [STATE]
--reversed_map_lookup state_map state = fromJust (Map.lookup state state_map)

-- reversed_map_lookup :: STATE_MAP -> Integer -> [Integer]
-- reversed_map_lookup state_map state = fromJust (Map.lookup state state_map)


-- ctl_ax :: FUNCTION_ID -> STATE_ID -> Bool
-- ctl_ax function_num state_num = foldr ((&&) . (memoization_array_index function_num)) True (fromJust (Map.lookup state_num state_map))

-- ctl_ex :: FUNCTION_ID -> STATE_ID -> Bool
-- ctl_ex function_num state_num = foldr ((||) . (memoization_array_index function_num)) False (fromJust (Map.lookup state_num state_map))

-- ctl_af :: FUNCTION_ID -> STATE_ID -> Bool
-- ctl_af function_num state_id = ctl_af_state_search function_num [] [state_id]
-- ctl_af_state_search :: FUNCTION_ID -> [STATE_ID] -> [STATE_ID] -> Bool
-- ctl_af_state_search function seen_states state
--   | function state = True -- we found truth!
--   | Set.member state seen_states = False -- This means we haven't reached true and have nothing left to check
--   | otherwise = foldr ((&&) . ctl_af_state_search function (Set.insert state seen_states)) True (fromJust (Map.lookup state state_map)) -- more searching required.

-- -- ctl_af :: (STATE -> Bool) -> STATE -> Bool
-- -- ctl_af function = ctl_af_state_search function []
-- -- ctl_af_state_search :: (STATE -> Bool) -> [STATE] -> STATE -> Bool
-- -- ctl_af_state_search function seen_states state
-- --   | function state = True -- we found truth!
-- --   | Set.member state seen_states = False -- This means we haven't reached true and have nothing left to check
-- --   | otherwise = foldr ((&&) . ctl_af_state_search function (Set.insert state seen_states)) True (fromJust (Map.lookup state state_map)) -- more searching required.


-- ctl_ef :: (STATE -> Bool) -> STATE -> Bool
-- ctl_ef function state = (||) (function state) (ctl_ef_state_search function (Set.singleton state) (fromJust (Map.lookup state state_map)))
-- ctl_ef_state_search :: (STATE -> Bool) -> Set.Set STATE -> Set.Set STATE -> Bool
-- ctl_ef_state_search function seen_states states_to_explore
--   | Set.null unexplored_states = False -- This means we haven't reached true and have nothing left to check
--   | otherwise = conclusion -- This means we still have states to check
--   where
--     unexplored_states = Set.difference states_to_explore seen_states  -- make sure to remove any overlap.
--     found_true = Set.foldr ((||) . function) False unexplored_states -- check if the condition holds for any of the new states
--     conclusion
--       | found_true = True -- if the condition holds for any of the new states, then we're done.
--       | otherwise = ctl_ef_state_search function (Set.union seen_states unexplored_states) (Set.foldr (Set.union . reversed_map_lookup state_map) Set.empty unexplored_states) -- more searching required.


-- ctl_ag :: (STATE -> Bool) -> STATE -> Bool
-- ctl_ag function state = (&&) (function state) (ctl_ag_state_search function (Set.singleton state) (fromJust (Map.lookup state state_map)))
-- ctl_ag_state_search :: (STATE -> Bool) -> Set.Set STATE -> Set.Set STATE -> Bool
-- ctl_ag_state_search function seen_states states_to_explore
--   | Set.null unexplored_states = True -- we ran out of states and found nothing wrong, return true.
--   | otherwise = conclusion
--   where
--     unexplored_states = Set.difference states_to_explore seen_states  -- make sure to remove any overlap.
--     all_true = Set.foldr ((&&) . function) True unexplored_states -- check if the condition holds for all of the new states
--     conclusion
--       | not all_true = False -- at least one of our current states failed, so it didn't hold globally.
--       | otherwise = ctl_ag_state_search function (Set.union seen_states unexplored_states) (Set.foldr (Set.union . reversed_map_lookup state_map) Set.empty unexplored_states) -- keep searching


-- ctl_eg :: (STATE -> Bool) -> STATE -> Bool
-- ctl_eg function = ctl_eg_state_search function Set.empty
-- ctl_eg_state_search :: (STATE -> Bool) -> Set.Set STATE -> STATE -> Bool
-- ctl_eg_state_search function seen_states state
--   | not (function state) = False -- it doesn't hold for the state, so it's not true.
--   | Set.member state seen_states = True -- we've looped!
--   | otherwise = Set.foldr ((||) . ctl_eg_state_search function (Set.insert state seen_states)) False (fromJust (Map.lookup state state_map)) -- more searching required.


-- ctl_au :: (STATE -> Bool) -> (STATE -> Bool) -> STATE -> Bool
-- ctl_au function_hold function_release state = (||) (function_release state) ((&&) (function_hold state) (ctl_au_state_search function_hold function_release (Set.singleton state) (fromJust (Map.lookup state state_map))))
-- ctl_au_state_search :: (STATE -> Bool) -> (STATE -> Bool) -> Set.Set STATE -> Set.Set STATE -> Bool
-- ctl_au_state_search function_hold function_release seen_states states_to_explore
--   | Set.null unexplored_states = False -- we ran out of states and at least one path didn't terminate with the release.
--   | Set.null not_released_states = True -- we released everything!
--   | otherwise = conclusion
--   where
--     unexplored_states = Set.difference states_to_explore seen_states  -- make sure to remove any overlap.
--     not_released_states = Set.filter (not . function_release) unexplored_states -- Filter so we only have states where the release condition is false.
--     allTrue = Set.foldr ((&&) . function_hold) True not_released_states -- check if the condition holds for all of the not released states
--     conclusion
--       | not allTrue = False -- at least one of our current states failed, so it didn't reach the point of release
--       | otherwise = ctl_au_state_search function_hold function_release (Set.union seen_states unexplored_states) (Set.foldr (Set.union . reversed_map_lookup state_map) Set.empty not_released_states) -- keep searching


-- ctl_eu :: (STATE -> Bool) -> (STATE -> Bool) -> STATE -> Bool
-- ctl_eu function_hold function_release state = (||) (function_release state) ((&&) (function_hold state) (ctl_eu_state_search function_hold function_release (Set.singleton state) (fromJust (Map.lookup state state_map))))
-- ctl_eu_state_search :: (STATE -> Bool) -> (STATE -> Bool) -> Set.Set STATE -> Set.Set STATE -> Bool
-- ctl_eu_state_search function_hold function_release seen_states states_to_explore
--   | Set.null unexplored_states = False -- we ran out of states and no path terminated with the release.
--   | otherwise = conclusion
--   where
--     unexplored_states = Set.difference states_to_explore seen_states  -- make sure to remove any overlap.
--     release_found = Set.foldr ((||) . function_release) False unexplored_states -- check if the condition holds for all of the not released states
--     holding_states = Set.filter function_hold unexplored_states -- Filter so we only have states where the release condition is false.
--     conclusion
--       | release_found = True -- we managed to reach the release
--       | otherwise = ctl_eu_state_search function_hold function_release (Set.union seen_states unexplored_states) (Set.foldr (Set.union . reversed_map_lookup state_map) Set.empty holding_states) -- keep searching


-- ctl_aw :: (STATE -> Bool) -> (STATE -> Bool) -> STATE -> Bool
-- ctl_aw function_hold function_release state = (||) (function_release state) ((&&) (function_hold state) (ctl_aw_state_search function_hold function_release Set.empty (fromJust (Map.lookup state state_map))))
-- ctl_aw_state_search :: (STATE -> Bool) -> (STATE -> Bool) -> Set.Set STATE -> Set.Set STATE -> Bool
-- ctl_aw_state_search function_hold function_release seen_states states_to_explore
--   | Set.null unexplored_states = True -- we ran out of states and there were no problems
--   | otherwise = conclusion
--   where
--     unexplored_states = Set.difference states_to_explore seen_states  -- make sure to remove any overlap.
--     not_released_states = Set.filter (not . function_release) unexplored_states -- Filter so we only have states where the release condition is false.
--     all_true = Set.foldr ((&&) . function_hold) True not_released_states -- check if the condition holds for all of the not released states
--     conclusion
--       | not all_true = False -- at least one of our current states failed, so it didn't reach the point of release
--       | otherwise = ctl_aw_state_search function_hold function_release (Set.union seen_states unexplored_states) (Set.foldr (Set.union . reversed_map_lookup state_map) Set.empty not_released_states) -- keep searching


-- ctl_ew :: (STATE -> Bool) -> (STATE -> Bool) -> STATE -> Bool
-- ctl_ew function_hold function_release = ctl_ew_state_search function_hold function_release Set.empty
-- ctl_ew_state_search :: (STATE -> Bool) -> (STATE -> Bool) -> Set.Set STATE -> STATE -> Bool
-- ctl_ew_state_search function_hold function_release seen_states state
--   | function_release state = True
--   | not (function_hold state) = False
--   | otherwise = Set.foldr ((||) . ctl_ew_state_search function_hold function_release (Set.insert state seen_states)) False (fromJust (Map.lookup state state_map)) -- more searching required.



main :: IO ()
main = 
  do {
    print "model checking for Simple_robot_50"
    ; print (length initial_states)
    ; print number_of_reachable_states
    ; print (ctl_0)
    --; print (list_difference initial_states (take 14 initial_states))
    --; print (length (list_merge initial_states initial_states))
    --; putStrLn ((++) "ctl_0 is " (show ctl_0))
  }
