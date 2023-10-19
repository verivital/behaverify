module BTreeObstacleAvoidance where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionObstacleAvoidance :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionObstacleAvoidance _ nodeLocation _ _ _ _ oldBlackboard oldEnvironment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    boardEnvUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate0 boardEnv
      | not (True) = boardEnv
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        privateTempBoardEnv0 = boardEnv
        privateBoardEnv = privateTempBoardEnv1
        privateTempBoardEnv1 = (updateBoardGenerator (updateBoardBbObstacleWarning blackboard (privateRandom0 (fst (getRandomInteger (sereneBoardGenerator blackboard) 1)))) (snd (getRandomInteger (sereneBoardGenerator blackboard) 1)), environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
            privateRandom0 :: Integer -> Bool
            privateRandom0 0 = True
            privateRandom0 _ = False
    boardEnvUpdate1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate1 boardEnv
      | (boardBbObstacleWarning blackboard) = (updateBoardCmHsdInput blackboard "cm_obstacle_avoidance_task", environment)
      | otherwise = (updateBoardCmHsdInput blackboard (boardCmHsdInput blackboard), environment)
      where
        (blackboard, environment) = boardEnv
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv = Running
      where
        (blackboard, environment) = boardEnv
    preStatusBoardEnv = boardEnvUpdate1 . boardEnvUpdate0 $ (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) =  preStatusBoardEnv
    newFutureChanges = futureChanges
