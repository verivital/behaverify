module BTreeDdLecTask where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionDdLecTask :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionDdLecTask _ nodeLocation _ _ _ _ oldBlackboard oldEnvironment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    boardEnvUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate0 boardEnv
      | not (True) = boardEnv
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        privateTempBoardEnv0 = boardEnv
        privateBoardEnv = privateTempBoardEnv1
        privateTempBoardEnv1 = (updateBoardGenerator (updateBoardDdOutput blackboard (privateRandom0 (fst (getRandomInteger (sereneBoardGenerator blackboard) 2)))) (snd (getRandomInteger (sereneBoardGenerator blackboard) 2)), environment)
          where
            (blackboard, environment) = privateTempBoardEnv0
            privateRandom0 :: Integer -> String
            privateRandom0 0 = "safe"
            privateRandom0 1 = "z_warn"
            privateRandom0 _ = "xy_warn"
    boardEnvUpdate1 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate1 boardEnv = (updateBoardDdZAxisWarning blackboard (((boardDdOutput blackboard) == "z_warn") || ((boardDdZAxisWarning blackboard) && (not ((boardDdOutput blackboard) == "safe")))), environment)
      where
        (blackboard, environment) = boardEnv
    boardEnvUpdate2 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate2 boardEnv = (updateBoardDdXyAxisDegradation blackboard (((boardDdOutput blackboard) == "xy_warn") || ((boardDdXyAxisDegradation blackboard) && (not ((boardDdOutput blackboard) == "safe")))), environment)
      where
        (blackboard, environment) = boardEnv
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv = Failure
      where
        (blackboard, environment) = boardEnv
    preStatusBoardEnv = boardEnvUpdate2 . boardEnvUpdate1 . boardEnvUpdate0 $ (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) =  preStatusBoardEnv
    newFutureChanges = futureChanges
