module BehaviorTreeBlackboard where

data BTreeBlackboard = BTreeBlackboard {
  x :: Int
  , y :: Int  } deriving (Show)

update_blackboard_x :: BTreeBlackboard -> Int -> BTreeBlackboard
update_blackboard_x blackboard value
  | 0 > value || value > 10 = error "x illegal value"
  | otherwise = blackboard { x = value }

update_blackboard_y :: BTreeBlackboard -> Int -> BTreeBlackboard
update_blackboard_y blackboard value
  | 0 > value || value > 10 = error "y illegal value"
  | otherwise = blackboard { y = value }



initialBTreeBlackboard = BTreeBlackboard 0 10
