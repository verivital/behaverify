module BTreeRtreach2bb where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionRtreach2bb :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionRtreach2bb _ nodeLocation _ _ _ _ oldBlackboard oldEnvironment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
  where
    boardEnvUpdate0 :: (BTreeBlackboard, BTreeEnvironment) -> (BTreeBlackboard, BTreeEnvironment)
    boardEnvUpdate0 boardEnv
      | not (True) = boardEnv
      | conditionRandomInteger == 0 = privateTempBoardEnv0
      | otherwise = privateBoardEnv
      where
        (conditionBlackboard, conditionEnvironment) = boardEnv
        (conditionRandomInteger, conditionRandomGenerator) = getRandomInteger (sereneEnvGenerator (snd boardEnv)) 1
        privateTempBoardEnv0 = (fst boardEnv, updateEnvGenerator (snd boardEnv) conditionRandomGenerator)
        privateTempBoardEnv1 = (updateLocalBoardReadSuccess nodeLocation (fst privateTempBoardEnv0) True, snd privateTempBoardEnv0)
        privateBoardEnv = privateTempBoardEnv3
        privateTempBoardEnv2 = (updateBoardRtreachLongTermWarning blackboard (((envRtreachResult environment) == "long") || ((envRtreachResult environment) == "short_long")), environment)
          where
            (blackboard, environment) = privateTempBoardEnv1
        privateTempBoardEnv3 = (updateBoardRtreachWarning blackboard (((envRtreachResult environment) == "short") || ((envRtreachResult environment) == "short_long")), environment)
          where
            (blackboard, environment) = privateTempBoardEnv2
    returnStatement :: (BTreeBlackboard, BTreeEnvironment) -> BTreeNodeStatus
    returnStatement boardEnv
      | (localBoardReadSuccess nodeLocation blackboard) = Success
      | otherwise = Running
      where
        (blackboard, environment) = boardEnv
    preStatusBoardEnv = boardEnvUpdate0 (oldBlackboard, oldEnvironment)
    returnStatus = returnStatement preStatusBoardEnv
    (newBlackboard, newEnvironment) =  preStatusBoardEnv
    newFutureChanges = futureChanges
