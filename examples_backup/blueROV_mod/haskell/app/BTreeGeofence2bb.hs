module BTreeGeofence2bb where
import BehaviorTreeCore
import BehaviorTreeBlackboard
import BehaviorTreeEnvironment
import SereneRandomizer
import SereneOperations



bTreeFunctionGeofence2bb :: [BTreeNode] -> TreeLocation -> TrueMemoryStatus -> [TrueMemoryStorage] -> PartialMemoryStatus -> [PartialMemoryStorage] -> BTreeBlackboard -> BTreeEnvironment -> FutureChanges -> BTreeNodeOutput
bTreeFunctionGeofence2bb _ nodeLocation _ _ _ _ oldBlackboard oldEnvironment futureChanges = (returnStatus, [], [], newBlackboard, newEnvironment, newFutureChanges)
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
        privateBoardEnv = privateTempBoardEnv2
        privateTempBoardEnv2 = (updateBoardBbGeofenceWarning blackboard ((boardBbGeofenceWarning blackboard) || (envBbGeofence environment)), environment)
          where
            (blackboard, environment) = privateTempBoardEnv1
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
