module Behavior_tree_blackboard where
data BTreeBlackboard = BTreeBlackboard {
  boardX :: Int
  , boardY :: Int  } deriving (Show)

updateBoardX :: BTreeBlackboard -> Int -> BTreeBlackboard
updateBoardX blackboard value
  | 0 > value || value > 10 = error "x illegal value"
  | otherwise = blackboard { boardX = value }

updateBoardY :: BTreeBlackboard -> Int -> BTreeBlackboard
updateBoardY blackboard value
  | 0 > value || value > 10 = error "y illegal value"
  | otherwise = blackboard { boardY = value }



initialBlackboard = BTreeBlackboard 0 10
